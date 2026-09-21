FROM python:3.11-slim

RUN pip install --no-cache-dir nbclient nbformat ipykernel pandas numpy \
    && python -m ipykernel install --user

COPY runner.py /runner.py

ENTRYPOINT ["python", "/runner.py"]
