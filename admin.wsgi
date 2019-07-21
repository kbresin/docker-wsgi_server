#import cStringIO
#import os
import json
import sqlite3

def application(environ, start_response):
	headers = []
	headers.append(('Content-Type', 'text/json'))
	json_response = dict()
	json_response['error_code'] = 0
	http_status = '200 OK'
	sqlite_file = '/db/fileshare_auth_db.sqlite'    # name of the sqlite database file


	input = environ['wsgi.input']

#	output = cStringIO.StringIO()

#	print >> output, "PID: %s" % os.getpid()
#	print >> output, "UID: %s" % os.getuid()
#	print >> output, "GID: %s" % os.getgid()
#	print >> output
#	print >> output, "Input: %s" % input

# IP check
# HTTP_X_FORWARDED_FOR: '38.77.32.191'
# environ['HTTP_X_REAL_IP']
# src_ip_header = 'HTTP_X_REAL_IP'
# content_length = environ.get('CONTENT_LENGTH', '0')
# if content_length > 2:
# json_post_data = input.read(content_length)

#	keys = environ.keys()
#	keys.sort()
#	for key in keys:
#		print >> output, '%s: %s' % (key, repr(environ[key]))
#		print >> output

	src_ip_header = 'HTTP_X_REAL_IP'
	src_ip = ''
	if src_ip_header in environ and environ['HTTP_X_REAL_IP'] != '':
		src_ip = environ['HTTP_X_REAL_IP']
		json_response['src_ip'] = src_ip
#		print >> output, "src_ip = %s" % src_ip
	else:
#		print >> output, 'Invalid Request A'
		json_response['error_code'] = 1
		http_status = '400 Bad Request'

	json_vals = dict()
	secret_key = 'secret'
	content_length = int(environ.get('CONTENT_LENGTH', '0'))
	if content_length > 2:
		post_input = input.read(content_length)
		try:
			json_vals = json.loads(post_input)
			if secret_key not in json_vals or json_vals[secret_key] == '':
				# no secret defined in submitted json
				json_response['error_code'] = 2
				http_status = '400 Bad Request'
		except ValueError:
			# failed to decode JSON
			json_response['error_code'] = 3
			http_status = '400 Bad Request'
	else:
		# content length 0
		json_response['error_code'] = 4
		http_status = '400 Bad Request'

	if json_response['error_code'] == 0:
		conn = sqlite3.connect(sqlite_file)
		c = conn.cursor()

		check_admin_query = 'SELECT * FROM admin_auth WHERE src_ip= ? and shared_secret = ? LIMIT 1'
		c.execute(check_admin_query, [src_ip, json_vals[secret_key]])
		id_exists = c.fetchone()
		if id_exists:
			json_response['auth_ok'] = 1
		else:
			json_response['error_code'] = 5
			http_status = '403 Forbidden'

	if json_response['error_code'] != 0:
		headers.append(('X-Error-Code', str(json_response['error_code'])))

	write = start_response(http_status, headers)
	return [json.dumps(json_response)]
