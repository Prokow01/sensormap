from flask import render_template, jsonify, request
from app import mongo
from app import app
from bson import Binary, Code, json_util
from bson.json_util import dumps, loads



@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')
	
@app.route('/map')
def map_render():
	return render_template('map-tool.html')

@app.route('/sensor_search', methods=['POST', 'GET'])
def sensor_search():
	return db_test()

@app.route('/findSensors', methods=['POST', 'GET'])
def findSensors():
	cursor = mongo.db.sensors_generic.find()
	
	records = dict((record['_id'], record) for record in cursor)
		#I DON'T know why this works... thank you stackoverflow
	
	return jsonify(records)
	#returns basic list of sensors and their respective locations

@app.route('/test')
def test():
	latitudes = ['40.033782', '40.033950', '40.034807', '40.034965', 
	'40.035252', '40.035737', '40.036000', '40.036875', '40.037027', 
	'40.037852',  '40.037799']
	
	longitudes = ['-75.339226', '-75.339194', '-75.339939', '-75.339902', 
	'-75.339663', '-75.340902', '-75.341535', '-75.341857', '-75.342764', 
	'-75.342544', '-75.342088']
	
	path_coords = {'userID' : '0001', 'latitudes' : latitudes, 'longitudes' : longitudes}
	
	return jsonify(path_coords)


def db_test():
	e = mongo.db.sensors_generic.find()
	g = mongo.db.regions.find()
	t = "cursor"
	return render_template('redirect_under_construction.html', data=e, type=t)

@app.route('/component/test', methods=['POST', 'GET'])
def render_component():
	q = request.args['comp']
	result = q + ".html"
	return render_template(result)
