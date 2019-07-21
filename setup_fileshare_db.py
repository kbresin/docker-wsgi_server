#!/usr/bin/python

# docker run needs -e ADMIN_IP and -e ADMIN_SHARED_SECRET setup!

import sqlite3
import os

sqlite_file = 'fileshare_auth_db.sqlite'    # name of the sqlite database file
# check if the db exists yet
db_exists = os.path.exists(sqlite_file)

db_filesize = 0
if db_exists:
	db_filesize = os.stat(sqlite_file).st_size

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Initialize by creating the tables
if not db_exists or db_filesize == 0:
	# Creating a new SQLite table with 1 column
	c.execute('CREATE TABLE admin_auth (src_ip TEXT PRIMARY KEY, shared_secret TEXT)')
	c.execute('CREATE TABLE file_request_auth (auth_token TEXT PRIMARY KEY, user_id INTEGER, src_ip TEXT, file TEXT, timestamp INTEGER)')

	# Committing changes and closing the connection to the database file
	conn.commit()

	if os.environ['ADMIN_IP'] and os.environ['ADMIN_SHARED_SECRET']:
		try:
			# add rows
			insert_query = "INSERT INTO admin_auth(src_ip, shared_secret) VALUES (?, ?)"
			c.execute(insert_query, [ os.environ['ADMIN_IP'], os.environ['ADMIN_SHARED_SECRET'] ])
		except sqlite3.IntegrityError:
		   print('ERROR: ID already exists in PRIMARY KEY column {}')

conn.commit()
conn.close()
