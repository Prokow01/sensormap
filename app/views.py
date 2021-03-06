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


@app.route('/retrieveTest')
def retrieveTest():
	return render_template("AjaxTest.html")

@app.route('/getInfoPane/<int:sensorId>')
def getContent(sensorId):
	e = mongo.db.sensor_data.find({"sensorId" : sensorId})
	return render_template("infoWindow.html", content=e)

@app.route('/testInfoPane/<int:sensorId>')
def testContent(sensorId):
	e = mongo.db.sensor_data.find({"sensorId" : sensorId})
	return render_template("testDataTable.html", content=e)

@app.route('/updateWindowPane/<int:sensorId>')
def updatePane(sensorId):
	e = mongo.db.sensors_generic.find({"_id": sensorId})
	return render_template("info-pane.html", content = e)
