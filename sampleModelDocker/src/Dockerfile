FROM python:3.7
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


RUN mkdir models
COPY models ./models

COPY samplelogreg_service.py ./


RUN find . -name \*.pyc -delete

EXPOSE 5000

RUN ls
RUN pwd
CMD ["python", "./samplelogreg_service.py"]
