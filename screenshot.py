from playwright.sync_api import sync_playwright
from pathlib import Path

url = "https://ibrahiemmohamed24.github.io/nbghost/"
desktop = Path.home() / "Desktop"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(1500)  # let the hero load animation finish

    total_height = page.evaluate("document.body.scrollHeight")
    step = max(total_height - 900, 0) / 4

    for i in range(5):
        page.evaluate(f"window.scrollTo(0, {int(step * i)})")
        page.wait_for_timeout(700)  # let counters/animations trigger
        page.screenshot(path=str(desktop / f"{i + 1}.png"))

    browser.close()

print("Done: 5 screenshots saved to Desktop")

