import json
from bottle import route, run, template, os, request

@route('/call/<token>/<script>')
def index(token,script):
	if (canAccess(token)):
		if (os.system(scriptsPath + script)):
			return template('Sorry! Can\'t run that script: {{script}}. Check the script\'s name or its location.', script=script)
		else:
			return template('Hello! the script {{script}} was run.', script=script)
	else: 
		return template('Sorry! Can\'t run that script: {{script}}.', script=script)

def canAccess(token):
	remoteaddr = request.environ.get('REMOTE_ADDR')
	forwarded = request.environ.get('HTTP\_X\_FORWARDED_FOR')
	if (localToken == token ):
		if (len(whiteList) > 0):
			if ((remoteaddr in whiteList) or (forwarded in whiteList)):
				return True
			else:
				return False
		else:
			return True
	else:
		return False
		
try:
	with open('config.json', 'r') as f:
		config = json.load(f)
	try:
		localToken = config['token']
	except KeyError:
		print('The "token" config is missing. The app will close.')
		exit()
	try:
		scriptsPath = config['scriptsPath']
	except KeyError:
		print('The "scriptsPath" config is missing. The app will close.')
		exit()
	try:
		port = config['port']
	except KeyError:
		print('The "port" config is missing. The app will close.')
		exit()
	whiteList = config['whiteList']
	run(host='localhost', port=port)
except OSError as e:
    print('Couldn\'t lod file config.json. It must be located next to this script. The app will close;')