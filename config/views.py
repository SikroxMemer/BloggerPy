from flask import Flask , Blueprint

routes = Blueprint('App' , __name__)

@routes.route('/')
def main():
    ...