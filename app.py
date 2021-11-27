import os
from flask import Flask
from flask import request
from database import Sport, Event, Selection, DbClass
import json

app = Flask(__name__)

db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/SportsBook.db')

@app.route('/')
def index():
  return 'Server Works!'

@app.route('/sports', methods = ['GET'])
def sports_list():
  db = DbClass(db_file)
  db.connection()
  items = db.get_sports()
  db.disconnection()
  return json.dumps(items)

@app.route('/events', methods = ['GET'])
def events_list():
  db = DbClass(db_file)
  db.connection()
  items = db.get_events()
  db.disconnection()
  return json.dumps(items)

@app.route('/selections', methods = ['GET'])
def selections_list():
  db = DbClass(db_file)
  db.connection()
  items = db.get_selections()
  db.disconnection()
  return json.dumps(items)

@app.route('/sports', methods = ['POST'])
def add_sport():
  # To test it use Postman, using query string to pass the variables for the time being
  name = request.args.get('name')
  slug = request.args.get('slug')
  active = request.args.get('active')

  # variables validation should be already done by form

  sport = Sport(0, name, slug, active)
  db = DbClass(db_file)
  db.connection()
  id = db.insert_sport(sport)
  db.disconnection()
  return "sport id is {}. 0 means failed".format(id)

@app.route('/events', methods = ['POST'])
def add_event():
  # To test it use Postman, using query string to pass the variables for the time being
  name = request.args.get('name')
  slug = request.args.get('slug')
  active = request.args.get('active')
  type = request.args.get('type')
  sport_id = request.args.get('sport_id')
  status = request.args.get('status')
  scheduled_start = request.args.get('scheduled_start')
  actual_start = request.args.get('actual_start')

  # variables validation should be already done by form

  event = Event(0, name, slug, active, type, sport_id, status, scheduled_start, actual_start)
  db = DbClass(db_file)
  db.connection()
  id = db.insert_event(event)
  db.disconnection()
  return "event id is {}. 0 means failed".format(id)

@app.route('/selections', methods = ['POST'])
def add_selection():
  # To test it use Postman, using query string to pass the variables for the time being
  name = request.args.get('name')
  price = request.args.get('price')
  active = request.args.get('active')
  event_id = request.args.get('event_id')
  outcome = request.args.get('outcome')

  # variables validation should be already done by form

  event = Selection(0, name, price, active, event_id, outcome)
  db = DbClass(db_file)
  db.connection()
  id = db.insert_selection(event)
  db.disconnection()
  return "selection id is {}. 0 means failed".format(id)

@app.route('/sports/<id>', methods = ['PUT'])
def update_sport(id):
  # To test it use Postman, using query string to pass the variables for the time being
  name = request.args.get('name')
  slug = request.args.get('slug')
  active = request.args.get('active')

  sport = Sport(id, name, slug, active)
  db = DbClass(db_file)
  db.connection()
  isSuccess = db.update_sport(sport)
  db.disconnection()
  return "Updated sport id of {} is {}".format(id, isSuccess)

@app.route('/events/<id>', methods = ['PUT'])
def update_event(id):
  # To test it use Postman, using query string to pass the variables for the time being
  name = request.args.get('name')
  slug = request.args.get('slug')
  active = request.args.get('active')
  type = request.args.get('type')
  sport_id = request.args.get('sport_id')
  status = request.args.get('status')
  scheduled_start = request.args.get('scheduled_start')
  actual_start = request.args.get('actual_start')

  event = Event(id, name, slug, active, type, sport_id, status, scheduled_start, actual_start)
  db = DbClass(db_file)
  db.connection()
  isSuccess = db.update_event(event)
  db.disconnection()
  return "Update event id of {} is {}".format(id, isSuccess)

@app.route('/selections/<id>', methods = ['PUT'])
def update_selection(id):
  # To test it use Postman, using query string to pass the variables for the time being
  name = request.args.get('name')
  price = request.args.get('price')
  active = request.args.get('active')
  event_id = request.args.get('event_id')
  outcome = request.args.get('outcome')

  event = Selection(id, name, event_id, price, active, outcome)
  db = DbClass(db_file)
  db.connection()
  isSuccess = db.update_selection(event)
  db.disconnection()
  return "Update selection id of {} is {}".format(id, isSuccess)



