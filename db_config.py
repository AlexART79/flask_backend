import os

db_user = os.environ['DB_USER'] if 'DB_USER' in os.environ.keys() else 'root'
db_password = os.environ['DB_PASSWORD'] if 'DB_PASSWORD' in os.environ.keys() else '12345'
db_host = "{}:3306".format(os.environ['DB_HOST'] if 'DB_HOST' in os.environ.keys() else '127.0.0.1')
db_name = os.environ['DB_NAME'] if 'DB_NAME' in os.environ.keys() else 'todo'
