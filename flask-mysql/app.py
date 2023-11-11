#!/usr/bin/python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db import username, host, password

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}/flask_mysql'
db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(debug=True)
    