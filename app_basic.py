from random import randint
from flask import Flask, request
import logging
import os
os.environ["FLASK_ENV"] = 'development'

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger= logging.getLogger(__name__)

@app.route("/ritm")
def e2e():
    ritm=request.args.get('ritm', default=None, type=str)
    result=str(b_exec())
    # if ritm:
    #     logger.info("%s has triggered e2e flow.. %s", ritm, result)

    # else:
    #     logger.warning("Unknown RITM number. Exec started..", result)

    return [result, __name__]

@app.route("/system")
def system():
    params=request.args.get('caller', default= "AWX", type=str)
    print(params)
    return request.args

def b_exec():
    return randint(1,100)