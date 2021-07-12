#!/usr/bin/env python
from db_table import db_table
import xlrd
import sys

wrkbk = xlrd.open_workbook("agenda.xls")
wrksheet = wrkbk.sheet_by_name("Agenda")
row = [x for x in wrksheet.row_values(15)]

schema = db_table("agenda", {"id": "integer PRIMARY KEY", "date": "string NOT NULL", "time_start": "string NOT NULL", 
                             "time_end": "string NOT NULL", "session": "string NOT NULL", "title": "string NOT NULL",
                             "location": "string", "description": "string", "speakers": "string"})

id = 1

for row_num in range(15, wrksheet.nrows):

  # get all column values and remove any leading or trailing whitespaces for data cleaning
  row_vals = [col.strip() for col in wrksheet.row_values(row_num)]
  
  # escape ' character to insert into database
  if "'" in row_vals[4]:
    row_vals[4] = row_vals[4].replace("'", "''")
  if "'" in row_vals[6]:
    row_vals[6] = row_vals[6].replace("'", "''")
  if "'" in row_vals[7]:
    row_vals[7] = row_vals[7].replace("'", "''")

  schema.insert({"id": id,
                "date": row_vals[0],
                "time_start": row_vals[1],
                "time_end": row_vals[2],
                "session": row_vals[3],
                "title": row_vals[4],
                "location": row_vals[5], 
                "description": row_vals[6],
                "speakers": row_vals[7]})
  
  id = id + 1

schema.close()