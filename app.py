#  import for flask
from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

database_file = open('db.txt', 'U')
db_host = database_file.readline().strip() #URL and port
dbname = database_file.readline().strip()
user = database_file.readline().strip()
password = database_file.readline().strip()
database_file.close()
app.config['MONGO_DBNAME'] = dbname
app.config['MONGO_URI'] = 'mongodb://' + user + ':' + password + '@' + db_host + '/' + dbname
app.config['MONGO_CONNECT'] = False

mongo = PyMongo()
with app.app_context():
	mongo.init_app(app)

import json

#Copy from StackOverflow-----------------------------
from os import path
import os

extra_dirs = ['static','templates']
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)
#app.run(extra_files=extra_files)
#End copy-----------------------------------------------

#  import for generating session key
from os import urandom
app.secret_key = urandom(24)


#  import for ship-building funcitons
import random as r
from math import floor


#Session ID based on timing
import time

#Look into how to prevent caching of game pages - we're using GET for most of this, it would look OK to cache to the client end.

# 
# 
# 	Function to build the ships to play the game.  The ships are generated on the index page, so the player must not skip this step!
# 
# 

def build_ships():
	
	ships = []

	#Central clustering uniform
	#ship_masses = []
	#for i in range(3):
	#	ship_masses.append(round(r.random(),2))
	#r.shuffle(ship_masses)
	
	#Outward-tending spaced dist.
	#ship_masses = []
	#mid_mass = round(r.random(),2)
	#ship_masses.append(round(r.random() * (1 - mid_mass),2) + mid_mass)
	#ship_masses.append(round(r.random() * mid_mass,2))
	#ship_masses.append(mid_mass)
	#r.shuffle(ship_masses)
	
	#Common to both options
	#loot = 10 + 30 * max(0,min(1,r.gauss(ship_mass, 0.1)))
	#targets = []
	#for i in range(3):
	#	targets.append(max(0,min(1,r.gauss(ship_mass, 0.1))))
	#targets.sort()
	#min_risk = targets[0]
	#target = targets[1]
	#max_risk = targets[2]
	
	SMALL_CI = 0.1
	MED_CI = 0.3
	LG_CI = 0.6
	
	for j in range(3):

		# Somewhere to store the random numbers
		rands = []

		# Somewhere to store the ship information
		ship = {}
		ship['number'] = j
		# # get random numbers for the max/min values of uncertainty
		# for i in range(2):
			# rands.append(round(r.random(),2))
			# #The range could stand to be a bit narrower.

		# rands.sort()
	
		# # push min/max values of risk to the ship
		# ship['min'] = rands[0]
		# ship['max'] = rands[1]

		# # push margin of error and median of min/max risk values to the ship
		# ship['plus_minus'] = round((ship['max'] - ship['min'])/2,2)
		# ship['median'] = round(ship['min'] + ship['plus_minus'], 2)

		# ship['target'] = r.gauss(ship['median'], ship['plus_minus']/2)
		# if ship['target'] > ship['max']:
			# ship['target'] = ship['max']
		# elif ship['target'] < ship['min']:
			# ship['target'] = ship['min']
		
		target = round(r.random(),2)
		ship['target'] = target
		
		range_size = r.choice([SMALL_CI,MED_CI,LG_CI]) + r.choice([-0.03,-0.02,-0.02,-0.01,-0.01,-0.01,0,0.01,0.01,0.01,0.02,0.02,0.03])
		
		shift = r.random()
		range_shift = - (range_size * shift)
		
		range_min = target + range_shift
		range_max = target + range_size + range_shift
		
		if range_min < 0:
			range_max = range_max - range_min
			range_min = 0
		if range_max > 1:
			range_min = range_min - (range_max - 1)
			range_max = 1
		
		ship['min'] = round(range_min,2)
		ship['max'] = round(range_max,2)
		
		ship['plus_minus'] = round((ship['max'] - ship['min'])/2,2)
		ship['median'] = round(ship['min'] + ship['plus_minus'], 2)

		# determine the type of ship based on the median value
		if ship['median'] <= 0.25:
			ship['type'] = "Sloop"
		elif ship['median'] <= 0.5:
			ship['type'] = "Cutter"
		elif ship['median'] <= 0.75:
			ship['type'] = "Schooner"
		else:
			ship['type'] = "Frigate"
		# ships.append(ship)

		# randomly pick reward for defeating the ship, and assign nationality based on this
		ship['reward'] = int(round(r.random()*40 + 10))
		if ship['reward'] <= 20:
			ship['nationality'] = "British"
		elif ship['reward'] <= 30:
			ship['nationality'] = "French"
		elif ship['reward'] <= 40:
			ship['nationality'] = "Dutch"
		else:
			ship['nationality'] = "Spanish"

		# determine semantic risk 
		if ship['min'] <= 0.15:
			ship['lower_semantic_risk'] = "Well below average"
		elif ship['min'] <= 0.30:
			ship['lower_semantic_risk'] = "Below average"
		elif ship['min'] <= 0.45:
			ship['lower_semantic_risk'] = "Slightly below average"
		elif ship['min'] <= 0.55:
			ship['lower_semantic_risk'] = "Average"
		elif ship['min'] <= 0.70:
			ship['lower_semantic_risk'] = "Slightly above average"
		elif ship['min'] <= 0.85:
			ship['lower_semantic_risk'] = "Above average"
		else:
			ship['lower_semantic_risk'] = "Well above average"


		if ship['max'] <= 0.15:
			ship['upper_semantic_risk'] = "Well below average"
		elif ship['max'] <= 0.30:
			ship['upper_semantic_risk'] = "Below average"
		elif ship['max'] <= 0.45:
			ship['upper_semantic_risk'] = "Slightly below average"
		elif ship['max'] <= 0.55:
			ship['upper_semantic_risk'] = "Average"
		elif ship['max'] <= 0.70:
			ship['upper_semantic_risk'] = "Slightly above average"
		elif ship['max'] <= 0.85:
			ship['upper_semantic_risk'] = "Above average"
		else:
			ship['upper_semantic_risk'] = "Well above average"


		if ship['median'] <= 0.15:
			ship['median_semantic_risk'] = "Well below average"
		elif ship['median'] <= 0.30:
			ship['median_semantic_risk'] = "Below average"
		elif ship['median'] <= 0.45:
			ship['median_semantic_risk'] = "Slightly below average"
		elif ship['median'] <= 0.55:
			ship['median_semantic_risk'] = "Average"
		elif ship['median'] <= 0.70:
			ship['median_semantic_risk'] = "Slightly above average"
		elif ship['median'] <= 0.85:
			ship['median_semantic_risk'] = "Above average"
		else:
			ship['median_semantic_risk'] = "Well above average"

		ship['allocated'] = 0	
		#  in case we need to remind that there is 30 doubloons to spend
		# add each ship to the list of ships
		ships.append(ship)


	return ships

# 
# 	Function to determine the game mode presented to the player
# 
def game_mode():
	game_mode = floor(r.random() * 4)
	if game_mode > 3:
		game_mode = 3
	return game_mode

# 
# 	Function to determine if the player wins
# 
def calculate_victories(allocation):

	for i, ship in enumerate(session['ships']):
		roll = round(r.random(),2)
		ship['player_roll'] = roll
		ship['allocated'] = int(allocation[i])
		if roll >= (ship['target'] - (int(allocation[i])/100.0)):
			ship['victory'] = 1
			ship['outcome'] = 'victory'
			session['ships_data']['total_reward'] += ship['reward']
		else:
			ship['victory'] = 0	
			ship['outcome'] = 'defeat'

#
#	Function to help make the dialogue more interesting
#
def dial_log():
	session['dial_log'] = r.random()

# 
# 
# 	Functions to return pages
# 
# 



# 
# 	index/landing page
# 
@app.route('/')
def index():
	if session.has_key('ethics_accept') and session['ethics_accept'] == True:
		#print "ETHICS TRUE"
		if not session.has_key('db_id'):
			#print "KEY FALSE"
			session['db_id'] = str(int(time.time() * 1000)) + str(r.randint(100,999)) #Let us hope that we don't need more than a few sessions per second... ...or that we operate in an environment where time.time has millisecond resolution. Just in case, add a 3-digit random number to the end.
			session['game_number'] = 0
			session['game_stage'] = 0
			session['surveyed'] = False
			session['decision_conf'] = False
			dial_log()
		session['ships'] = build_ships()
		session['game_mode'] = game_mode()
		session['ships_data'] = {}
		session['ships_data']['resources_allocated'] = 0
		session['ships_data']['total_reward'] = 0
		session['ships_data']['reminder'] = 0
		return render_template('index.html', ships = session['ships'], gameMode = session['game_mode'])
	else:
		session['ethics_accept'] = False
		return render_template('index.html')

	#else:
	#	return redirect(url_for('ethics') + "?accept=0")

@app.route('/ethics')
def ethics():
	if session.has_key('ethics_accept') and session['ethics_accept'] == True:
		return redirect(url_for('index'))
	else:
		if request.args.has_key('accept') and int(request.args['accept']) == 1:
				session['ethics_accept'] = True
				return redirect(url_for('index'))
		else:
			return render_template('ethics.html')
		
# 
# 	Map page
# 
@app.route('/map')
def map():
	if session.has_key('game_stage'):
		dial_log()
		session['game_stage'] = 10 #Increment in 10s, use intermediate values for reload resistance.
		return render_template('map.html', ships = session['ships'], gameMode = session['game_mode'], ships_data = session['ships_data'])
	else :
		return redirect(url_for('index'))

# 
# 	Resource allocation page
# 
@app.route('/risk')
def risk():
	#print session['game_stage']
	if session.has_key('game_stage'):
		if session['game_stage'] < 20:
			dial_log()
			session['game_stage'] = 20
			#print "Submitted game to db."
			submit_game_to_db(session['ships'], session['game_mode'], session['game_number'], session['db_id']) #Here, to collect data from abandoned-later games.
		#print session['game_stage']
		return render_template('risk.html', ships = session['ships'], gameMode = session['game_mode'], ships_data = session['ships_data'], reminder = False)
	else :
		return redirect(url_for('index'))


@app.route('/risk_reminder')
def risk_reminder():
	if session.has_key('game_stage'):
		dial_log()
		submit_event_to_db("REMINDER", True, request.args.get('time'), session['db_id'])
		return render_template('risk.html', ships = session['ships'], gameMode = session['game_mode'], ships_data = session['ships_data'], reminder = True)
	else :
		return redirect(url_for('index'))

@app.route('/decision_comfort')
def decision_comfort():
	if session.has_key('game_stage'):
		# check and see if they've spent all their money
		has_spent_all_money = request.args.get('sum') == '30'
		#print session['game_stage']
		#print request.args
		#print has_spent_all_money
		if has_spent_all_money:
			#print "SPENT"
			#print session['game_stage']
			#  if we don't do this next bit, they can mash refresh until they win!
			if session['game_stage'] < 25:
				#print "RESULT_TIME"
				session['game_stage'] = 25
				session['ships_data']['resources_allocated'] = 1
				
				allocation = [request.args.get('ship_1'), request.args.get('ship_2'), request.args.get('ship_3')]
				calculate_victories(allocation)

				submit_event_to_db("FINALISE", True, request.args.get('time'), session['db_id'])
				#Results are submitted away from generations, as the player may quit before getting a result.
				submit_result_to_db(session['ships'], session['game_number'], request.args.get('time'), session['db_id'])
				dial_log()
			return render_template('decision_check.html',ships = session['ships'], gameMode = session['game_mode'], ships_data = session['ships_data'])
		else:
			#print "remember to spend all your money"
			return redirect(url_for('risk_reminder') + '?time=' + request.args.get('time'))
	else:
		return redirect(url_for('index'))

@app.route('/decision_conf_submit', methods=['POST'])
def desc_conf_sub():
	#print "DESC CONF", session['game_stage']
	if session.has_key('game_stage') and session['game_stage'] == 25:
		session['decision_conf'] = True
		submit_confidence_to_db(request.form, session['game_number'], session['db_id'])
		return redirect(url_for('map_battle'))
	else:
		return redirect(url_for('risk'))
# 
# 	Map battle page
# 
@app.route('/map-battle', methods=['GET'])
def map_battle():
	if session.has_key('game_stage'):
		if (session['game_stage'] < 30):
			session['game_stage'] = 30
		#print session['ships_data']
		#print investments
		return render_template('map.html', ships = session['ships'], ships_data = session['ships_data'])
	else:
		return redirect(url_for('index'))

# 
# 	Play another round
# 
@app.route('/try_again')
def try_again():
	if session.has_key('game_stage') and session['game_stage'] == 30: #Don't let them reset their game too soon...
		session['game_number'] += 1
		session['game_stage'] = 0
		session['decision_conf'] = False
	return redirect(url_for('index'))

#
#	Recieve data
#
@app.route('/log_submit', methods=['POST'])
def recieve_event_data():
	if (session.has_key('game_stage')):
		if 20 <= session['game_stage'] < 30:
			#print request.is_json
			result = request.get_json()
			#print "Result: ", result
			#for evt in result:
				#print
				#print "Event: ", type(evt), evt
				#print
			submit_events_to_db(result, session['db_id'])
			#print "Logged event", result.get("event"), "; Game stage", session['game_stage']
		#else:
			#print "Someone hit BACK, this data is irrelevant..."
	return "4" #This should never be navigated to.

@app.route('/survey')
def survey():
	if session.has_key('ethics_accept') and session['ethics_accept'] == True and not session['surveyed']:
		return render_template('survey.html')
	else:
		return redirect(url_for('index'))


@app.route('/submit_survey', methods=['POST'])
def submit_survey():
	if session.has_key('ethics_accept') and session['ethics_accept'] == True and (not session['surveyed']):
		#print "\nA\n"
		session['surveyed'] = True
		submit_survey_to_db(request.form, session['db_id'])
		return redirect(url_for('thank_you'))
	else:
		return redirect(url_for('index'))
		#print "B\n"

@app.route('/thank_you' )
def thank_you():
	if session.has_key('surveyed') and session['surveyed']:
		session['game_stage'] = 0
		session['decision_conf'] = False
		dial_log()
		return render_template('thankyou.html')
	else:
		return redirect(url_for('index'))

		

#Copy/paste and modify from db_interface module -----------------------------------
		

def submit_event_to_db(type, success, time, session_key):
	#print "EVENT:", type, success, str(time), session_key
	coll_events = mongo.db.events
	result = coll_events.insert_one(encode_event(type, success, time, session_key))

def encode_event(type, success, time, session_key):
	return {"event":type, 
			"success":success, 
			"timestamp":str(time), 
			"session":session_key}

def submit_events_to_db(events, session_key):
	encoded = []
	for evt in events:
		print evt
		encoded.append(encode_event(evt['event'], evt['success'], evt['time'], session_key))
	coll_events = mongo.db.events
	result = coll_events.insert_many(encoded)
	
#Merge with survey submission? There will now be a 1:1 correspondence. May require some shifting, but if we can drop the number of log events...
#Also, instead of logging events individually, could we pile them up and submit in bulk? We may be throwing out incomplete games in any case.
def submit_game_to_db(ships, game_mode, game_number, session_key):
	#print "GAME"
	coll_games = mongo.db.games
	result = coll_games.insert_one(
			{'ships':summarize_ships_generated(ships),
			'game_mode':game_mode,
			'game_number':game_number,
			'session':session_key})

def submit_result_to_db(ships, game_number, time, session_key):
	#print "RESULT"
	coll_results = mongo.db.results
	result = coll_results.insert_one(
			{'results':summarize_ships_battles(ships),
			'game_number':game_number, 
			'time':time,
			'session':session_key})
			
def submit_survey_to_db(form, session_key):
	#print "SURVEY"
	coll_surveys = mongo.db.surveys
	db_record = {} #Need to add a key, so it's best to just write out the dict again.
	db_record['session'] = session_key
	db_record['age-group'] = form['ageGroup']
	db_record['sex'] = form['sex']
	db_record['responsibility'] = form['responsibility']
	db_record['education'] = form['education']
	db_record['in-aus'] = (True if form.get('in-aus') else False)
	db_record['stats-training'] = (True if form.get('in-aus') else False)
	#for arg in form:
		#print arg, ":", form[arg]
	result = coll_surveys.insert_one(db_record)
	
def submit_confidence_to_db(form, game_number, session_key):
	coll_confs = mongo.db.confs
	db_record = {}
	db_record['conf'] = form['conf'] if form.get('conf') else 'NOCHOICE'
	db_record['session'] = session_key
	db_record['game_number'] = game_number
	result = coll_confs.insert_one(db_record)
	
def summarize_ships_generated(ships):	
	summaries = []
	for i, ship in enumerate(ships):
		summary = {}
		summary['number'] = ship['number']
		summary['min'] = ship['min']
		summary['target'] = ship['target']
		summary['max'] = ship['max']
		summary['reward'] = ship['reward']
		summaries.append(summary)
	return summaries

def summarize_ships_battles(ships):
	summaries = []
	for i, ship in enumerate(ships):
		summary = {}
		summary['player_roll'] = ship['player_roll']
		summary['allocated'] = ship['allocated']
		#summary[''] = ship['']
		summaries.append(summary)
	return summaries
		
#End C/P &M ---------------------------------------------------------------------
		
#
#	Leaving DB connections open after flask shutdown is a bad idea. But there's no global hook, so this is the next-best thing.
#
@app.teardown_appcontext
def teardown_db(exception):
	mongo.cx.close()
	
		
		
		
		
		
		
		
		
import os
if __name__ == '__main__':
	#print(extra_files)
	app.run(extra_files=extra_files, host="0.0.0.0", port=int(os.environ.get('PORT',80)))



# from project import main

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     main.app.run(host='0.0.0.0', port=port)
