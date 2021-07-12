#!/usr/bin/env python
from db_table import db_table
import sys

schema = db_table("agenda", {"id": "integer PRIMARY KEY", "date": "string NOT NULL", "time_start": "string NOT NULL", 
                         "time_end": "string NOT NULL", "session": "string NOT NULL", "title": "string NOT NULL",
                         "location": "string", "description": "string", "speakers": "string"})

# parse command line arguments
column = sys.argv[1]
val = sys.argv[2]

rows = []

total_rows = schema.select()
number_total_rows = len(total_rows)

# select rows that contain the specific speaker
if column == "speakers":
	all_rows = schema.select()
	for row in all_rows:
		all_speakers = row['speakers'].split("; ")
		if val in all_speakers:
			rows.append(row)
else:
	rows = schema.select(where = {column:val})

remove_dup = []

for row in rows:

	# skip first subsession to remove duplicates
	if row['id'] in remove_dup:
		continue
	else:
		# print first matched session
		first_row_id = row['id']
		print(row)

		# loop to check if more subsessions
		while True:

			if row['id'] == number_total_rows:
				break

			# if this is a subsession, break loop because no more subsession in a subsession
			if row['session'] == "Sub":
				break

			# increment id and use id to select those subsessions
			first_row_id = first_row_id + 1
			sub_rows = schema.select(where = {"id":first_row_id})

			# check if more subsessions, if no more then break
			if sub_rows[0]['session'] == "Sub":
				# append first subsession to avoid duplicates
				remove_dup.append(sub_rows[0]['id'])
				print(sub_rows)

				if sub_rows[0]['id'] == number_total_rows:
					break
				else:
					continue
			else:
				break

schema.close()