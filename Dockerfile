FROM python:3.7
ADD . /myapp
WORKDIR /myapp
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python manage.py runserver
