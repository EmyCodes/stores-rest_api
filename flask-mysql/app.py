#!/usr/bin/python3.11

from sys import argv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://"root":19022002@localhost/5050'
db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(debug=True)