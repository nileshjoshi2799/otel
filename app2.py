# These are the necessary import declarations
from opentelemetry import trace
from opentelemetry import metrics

from random import randint
from flask import Flask, request
import logging

# Acquire a tracer
tracer = trace.get_tracer("diceroller.tracer")
# Acquire a meter.
meter = metrics.get_meter("diceroller.meter")

# Now create a counter instrument to make measurements with
span_counter = meter.create_counter(
    "terraform_span_count",
    description="the number of times span has been created",
)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/ritm")
def ritm():
    # This creates a new span that's the child of the current one
    with tracer.start_as_current_span("ritm") as ritm_span:
        user = request.args.get('user', default = None, type = str)
        result = str(get_rand())
        ritm_span.set_attribute("terra_span", result)
        ritm_span.set_attribute("terra_version", '1.0')
        # This adds 1 to the counter for the given roll value
        span_counter.add(1, {"span_value": result})
        if user:
            logger.warn("{} has called the flow {}", user, result)
        else:
            logger.warn("Anonymous system has called the flow: %s", result)
        return result

def get_rand():
    return randint(1, 100)