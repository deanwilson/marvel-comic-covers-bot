#!/usr/bin/env python3
import sqlite3
import os.path

from sys import exit

database = "comic_covers.db"

if os.path.isfile(database):
  print(f"A database already exists at {database}")
  exit(1)

create_comics_table = """
  CREATE TABLE comics (
    id integer PRIMARY KEY,
    comic_id integer NOT NULL,
    timestamp DATE DEFAULT (datetime('now','localtime'))
  );
"""

conn = sqlite3.connect(database)

try:
  c = conn.cursor()
  c.execute(create_comics_table)

  conn.commit()

  conn.close()
except Exception as e:
  print("Exception thrown: " + str(e))
  exit(1)
