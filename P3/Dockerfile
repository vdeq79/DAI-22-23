FROM python:3.10-alpine
WORKDIR /app  
COPY . /app
RUN pip install -r requirements.txt
RUN pip install django-crispy-forms
RUN pip install django-allauth
RUN pip install django-bootstrap4