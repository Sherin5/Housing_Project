from crypt import methods
from flask import Flask
from housing.logger import logging
from housing.exception import HousingException
import os, sys
app=Flask(__name__)

@app.route('/', methods= ['POST', 'GET'])
def index():
    try:
        raise Exception("We are testing our exception module")
    except Exception as e:
        housing = HousingException(e,sys)
        logging.info(housing.error_message) 

    logging.info(" We are testing the loggging module")
    return "CI CD Pipeline completed"

if __name__=="__main__":
    app.run(debug=True, port=5002)
