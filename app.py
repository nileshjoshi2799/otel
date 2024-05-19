from random import randint
from flask import Flask, request

from opentelemetry import trace
from opentelemetry import metrics

import logging

tracer = trace.get_tracer("e2e.tracer")
meter = metrics.get_meter("e2e.meter")

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

e2e_counter= meter.create_counter("e2e_count", "The count of the e2e workflows")

@app.route("/ritm")
def ritm():
    with tracer.start_as_current_span("Terra_span") as my_span:
        result = str(get_rand())
        my_span.set_attribute("Terra_span.value", result)
        my_span.set_attribute("Terra_span.version", 1.30)
        e2e_counter.add(1, {'e2e_value': result})
         
        system = request.args.get('system', default = None, type = str)
        
        if system:
            logger.warn("%s running module CreateAzureSubscription: %s", system, result)
        else:
            logger.warn("ExternalSystem running module CreateAzureSubscription: %s", result)
        return [result]

def get_rand():
    result = randint(1,100)
    return result