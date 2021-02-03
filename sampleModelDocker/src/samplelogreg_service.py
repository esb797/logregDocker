# To do: - Add countnwords to the getPrediction

import sys
from flask import Flask, request, jsonify, Response, Blueprint, url_for, abort, g, make_response, render_template
import joblib
from applicationinsights import TelemetryClient
from applicationinsights.flask.ext import AppInsights
import json
import os
import datetime as dt
from functools import wraps
from pyinstrument import Profiler
import numpy as np 


# print("----------- beginning of the run --------", file=sys.stderr)

# printerr(os.getcwd())

app = Flask(__name__)

@app.before_request
def before_request():
	if "profile" in request.args:
		g.profiler = Profiler()
		g.profiler.start()

def printerr(msg):
	print(msg, file=sys.stderr, flush=True)

try:
	app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = os.environ['TELEMETRY_CLIENT']

	# log requests, traces and exceptions to the Application Insights service
	appinsights = AppInsights(app)
except:
	printerr("No appInsights instrumentation key found.")
environment = None
debug = None
tckey = None
tc = None
servicename = 'samplelogreg_service'


try:
	debugstr = os.environ['DEBUG']
	if(debugstr == "True"):
		debug = True
	if(debugstr == "False"):
		debug = False
except Exception as e:
	printerr("No debug found.")

try:
	tckey = os.environ['TELEMETRY_CLIENT']
	tc = TelemetryClient(tckey)
	printerr(tckey)
except Exception as e:
	printerr("No appInsights instrumentation key found.")

try:
	environment = os.environ['ENVIRONMENT']
except Exception as e:
	printerr("No indication of environment found.")

try:
	model = joblib.load("models/logregModel.pkl")
except Exception as e:
	raise

#----- Function to Check Environment Variables -----#
@app.route("/checkEnv", methods=["GET"])
def home():
	return(json.dumps({"service": servicename, "debug" : debug, "appinsightsInstrumentationKey": tckey, "environment": environment}))

#----- Main App ----#
@app.route("/predict", methods=['POST'])
def post():

	# - Parse Headers - #
	requestId = None
	sessionId = None


	try:
		requestId = request.headers.get('X-Request-Id')
	except Exception as e:
		printerr(e)

	try:
		sessionId = request.headers.get('X-Session-Id')
	except Exception as e:
		printerr(e)

	#- Main - #
	try:
		data = request.get_json(force=True)
	except Exception as e:
		raise

	try:
		pred = model.predict(data['data'])
	except Exception as e:
		raise 

	return jsonify(pred.tolist())

#-- Healthcheck Route --#
@app.route("/", methods=["GET"])
def get():
	# Health check to test models are loaded
	return jsonify({'status':'ok'})

@app.after_request
def after_request(response):
	if not hasattr(g, "profiler"):
		return response
	g.profiler.stop()
	output_html = g.profiler.output_html()
	return make_response(output_html)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=debug, use_reloader=True)
