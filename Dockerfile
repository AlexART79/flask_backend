FROM python

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

# create db structure based on model
RUN python init_db.py

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]