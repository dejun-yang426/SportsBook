import sqlite3
from sqlite3 import Error
from collections import namedtuple

class Sport():
  def __init__(self, id, name, slug, active):
    self.Id = id
    self.Name = name
    self.Slug = slug
    self.Active = active

class Event():
  def __init__(self, id, name, slug, active, type, sport_id, status, scheduled_start, actual_start):
    self.Id = id
    self.Name = name
    self.Slug = slug
    self.Active = active
    self.Type = type
    self.Sport_Id = sport_id
    self.Status = status
    self.Scheduled_Start = scheduled_start
    self.Actual_Start = actual_start

class Selection():
  def __init__(self, id, name, event_id, price, active, outcome):
    self.Id = id
    self.Name = name
    self.Event_Id = event_id
    self.Price = price
    self.Active = active
    self.Outcome = outcome

class DbClass():
  SPORTS_TABLE_NAME = 'sports'
  EVENTS_TABLE_NAME = 'events'
  SELECTIONS_TABLE_NAME = 'selections'
  SPORTS_TABLE_CREATE_SQL = """CREATE TABLE IF NOT EXISTS sports (
	                               Id INTEGER PRIMARY KEY,
	                               Name NVARCHAR (255) NOT NULL,
                                   Slug NVARCHAR (255) NOT NULL,
                                   Active BOOLEAN DEFAULT 0);"""
  EVENTS_TABLE_CREATE_SQL = """CREATE TABLE IF NOT EXISTS events (
	                               Id INTEGER PRIMARY KEY,
	                               Name NVARCHAR (255) NOT NULL,
                                   Slug NVARCHAR (255) NOT NULL,
                                   Active BOOLEAN DEFAULT 0,
                                   Type tinyint DEFAULT 1,
                                   -- Type: 1 = Preplay; 2 = Inplay
                                   Sport_Id INTEGER not NULL,
                                   Status tinyint DEFAULT 1,
                                   -- Status: 1 = Pending; 2 = Started; 3 = Ended; 4 = Cancelled
                                   Scheduled_Start DATE NOT NULL,
                                   Actual_Start DATE,
                                   FOREIGN KEY (Sport_Id) REFERENCES sports (Id)); """
  SELECTIONS_TABLE_CREATE_SQL = """CREATE TABLE IF NOT EXISTS selections (
	                               Id INTEGER PRIMARY KEY,
	                               Name NVARCHAR (255) NOT NULL,
                                   Event_Id INTEGER NOT NULL,
                                   Price DECIMAL (6, 2) NOT NULL,
                                   Active BOOLEAN DEFAULT 0,
                                   Outcome tinyint DEFAULT 1,
	                               -- Outcome: 1 = Unsettled; 2 = Void; 3 = Lost; 4 = Win
                                   FOREIGN KEY (Event_Id) REFERENCES events (Id)); """
  SPORTS_TABLE_EXIST_QUERY_SQL = """SELECT name FROM sqlite_master WHERE type='table' AND name='sports'; """
  EVENTS_TABLE_EXIST_QUERY_SQL = """SELECT name FROM sqlite_master WHERE type='table' AND name='events'; """
  SELECTIONS_TABLE_EXIST_QUERY_SQL = """SELECT name FROM sqlite_master WHERE type='table' AND name='selections'; """

  def __init__(self, db_file):
    self.db_file = db_file
    self.conn = None

  def connection(self):
    try:
      self.conn = sqlite3.connect(self.db_file)
      if not self.check_table_exist(DbClass.SPORTS_TABLE_EXIST_QUERY_SQL):
        self.create_table(DbClass.SPORTS_TABLE_CREATE_SQL)
      if not self.check_table_exist(DbClass.EVENTS_TABLE_EXIST_QUERY_SQL):
        self.create_table(DbClass.EVENTS_TABLE_CREATE_SQL)
      if not self.check_table_exist(DbClass.SELECTIONS_TABLE_EXIST_QUERY_SQL):
        self.create_table(DbClass.SELECTIONS_TABLE_CREATE_SQL)
    except Error as e:
      print(e)

  def check_table_exist(self, table_exist_query_sql):
    isExist = False
    try:
      if self.conn is not None:
        cur = self.conn.cursor()
        list_table = cur.execute(table_exist_query_sql).fetchall()
        if len(list_table) != 0:
          isExist = True
    except Error as e:
      print(e)

    return isExist

  def create_table(self, create_sql):
    try:
      if self.conn is not None:
        cur = self.conn.cursor()
        cur.execute(create_sql)
    except Error as e:
      print(e)

  def get_sports(self):
    try:
      if self.conn is not None:
        sql = "SELECT * FROM sports"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
      else:
        raise RuntimeError("database not connected!")
    except Error as e:
      print(e)

    return None

  def get_events(self):
    try:
      if self.conn is not None:
        sql = "SELECT * FROM events"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
      else:
        raise RuntimeError("database not connected!")
    except Error as e:
      print(e)

    return None

  def get_selections(self):
    try:
      if self.conn is not None:
        sql = "SELECT * FROM selections"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
      else:
        raise RuntimeError("database not connected!")
    except Error as e:
      print(e)

    return None

  def check_table_entry_exist(self, table_name, and_filters):
    isExist = False
    id = 0
    try:
      if self.conn is not None:
        para_list = []
        sql = "SELECT * from {} WHERE ".format(table_name)
        i = 0
        for k,v in and_filters.items():
          if i == 0:
            sql += "{} = ?".format(k)
            para_list.append(v)
          else:
            sql += " AND {} = ?".format(k)
            para_list.append(v)
          i += 1
        cur = self.conn.cursor()
        cur.execute(sql, para_list)
        row = cur.fetchone()
        if row is not None:
          isExist = True
          id = row[0]
      else:
        raise RuntimeError("database not connected!")
    except Error as e:
      print(e)

    return (isExist, id)

  def insert_sport(self, sport):
    id = 0
    try:
      if self.conn is not None:
        add_filters = {}
        add_filters['Name'] = sport.Name
        isExist, id = self.check_table_entry_exist("sports", add_filters)
        if not isExist:
          sql = "INSERT INTO sports "
          names = "(Name, Slug"
          values = " VALUES(?,?"
          para_list = [sport.Name, sport.Slug]

          if sport.Active is not None:
            names += ", Active"
            values += ",?"
            para_list.append(sport.Active)

          names += ")"
          values += ")"
          sql += names + values

          cur = self.conn.cursor()
          cur.execute(sql, para_list)
          self.conn.commit()
          id = cur.lastrowid
      else:
        raise RuntimeError("database not connected!")
    except Error as e:
      print(e)

    return id

  def insert_event(self, event):
    id = 0
    try:
      if self.conn is not None:
        add_filters = {}
        add_filters['Name'] = event.Name
        add_filters['Sport_Id'] = event.Sport_Id
        isExist, id = self.check_table_entry_exist("events", add_filters)
        if not isExist:
          sql = "INSERT INTO events "
          names = "(Name, Slug"
          values = " VALUES(?,?"
          para_list = [event.Name, event.Slug]

          if event.Active is not None:
            names += ", Active"
            values += ",?"
            para_list.append(event.Active)
          if event.Type is not None:
            names += ", Type"
            values += ",?"
            para_list.append(event.Type)

          names += ", Sport_Id"
          values += ",?"
          para_list.append(event.Sport_Id)

          if event.Status is not None:
            names += ", Status"
            values += ",?"
            para_list.append(event.Status)

          names += ", Scheduled_Start"
          values += ",?"
          para_list.append(event.Scheduled_Start)

          if event.Actual_Start is not None:
            names += ", Actual_Start"
            values += ",?"
            para_list.append(event.Actual_Start)

          names += ")"
          values += ")"
          sql += names + values

          cur = self.conn.cursor()
          cur.execute(sql, para_list)
          self.conn.commit()
          id = cur.lastrowid
          self.set_sport_active_value(event.Sport_Id)
      else:
        raise RuntimeError("database not connected!")
    except Error as e:
      print(e)

    return id

  def insert_selection(self, selection):
    id = 0
    try:
      if self.conn is not None:
        add_filters = {}
        add_filters['Name'] = selection.Name
        add_filters['Event_Id'] = selection.Event_Id
        isExist, id = self.check_table_entry_exist("selections", add_filters)
        if not isExist:
          sql = "INSERT INTO selections "
          names = "(Name, Event_Id, Price"
          values = " VALUES(?,?,?"
          para_list = [selection.Name, selection.Event_Id, selection.Price]

          if selection.Active is not None:
            names += ", Active"
            values += ",?"
            para_list.append(selection.Active)
          if selection.Outcome is not None:
            names += ", Outcome"
            values += ",?"
            para_list.append(selection.Outcome)

          names += ")"
          values += ")"
          sql += names + values

          cur = self.conn.cursor()
          cur.execute(sql, para_list)
          self.conn.commit()
          id = cur.lastrowid

          self.set_event_active_value(selection.Event_Id)
      else:
        raise RuntimeError("database not connected!")
    except Error as e:
      print(e)

    return id

  def update_sport(self, sport):
    isSuccess = False
    try:
      if self.conn is not None:
        para_list = []
        sql = "UPDATE sports SET"
        if sport.Name is not None:
          para_list.append(sport.Name)
          sql += " Name = ?"
        if sport.Slug is not None:
          para_list.append(sport.Slug)
          if sql[-3:] != "SET":
            sql += ","
          sql += " Slug = ?"
        if sport.Active is not None:
          para_list.append(sport.Active)
          if sql[-3:] != "SET":
            sql += ","
          sql += " Active = ?"

        if sql[-3:] != "SET":
          sql += " Where Id = ?"
          para_list.append(sport.Id)

          cur = self.conn.cursor()
          cur.execute(sql, para_list)
          self.conn.commit()

        isSuccess = True
      else:
        raise RuntimeError("database not connected!")
    except Error as e:
      print(e)

    return isSuccess

  def update_event(self, event):
    isSuccess = False
    try:
      if self.conn is not None:
        para_list = []
        sql = "UPDATE events SET"
        if event.Name is not None:
          para_list.append(event.Name)
          sql += " Name = ?"
        if event.Slug is not None:
          para_list.append(event.Slug)
          if sql[-3:] != "SET":
            sql += ","
          sql += " Slug = ?"
        if event.Active is not None:
          para_list.append(event.Active)
          if sql[-3:] != "SET":
            sql += ","
          sql += " Active = ?"
        if event.Type is not None:
          para_list.append(event.Type)
          if sql[-3:] != "SET":
            sql += ","
          sql += " Type = ?"
        if event.Sport_Id is not None:
          para_list.append(event.Sport_Id)
          if sql[-3:] != "SET":
            sql += ","
          sql += " Sport_id = ?"
        if event.Status is not None:
          para_list.append(event.Status)
          if sql[-3:] != "SET":
            sql += ","
          sql += " Status = ?"
        if event.Scheduled_Start is not None:
          para_list.append(event.Scheduled_Start)
          if sql[-3:] != "SET":
            sql += ","
          sql += " Scheduled_Start = ?"
        if event.Actual_Start is not None:
          para_list.append(event.Actual_Start)
          if sql[-3:] != "SET":
            sql += ","
          sql += " Actual_Start = ?"

        if sql[-3:] != "SET":
          sql += " Where Id = ?"
          para_list.append(event.Id)

          cur = self.conn.cursor()
          cur.execute(sql, para_list)
          self.conn.commit()

          if event.Active is not None:
            isSuccess = self.set_sport_active_value(event.Sport_Id)
          else:
            isSuccess = True
        else:
          isSuccess = True
      else:
        raise RuntimeError("database not connected!")
    except Error as e:
      print(e)

    return isSuccess

  def update_selection(self, selection):
    isSuccess = False
    try:
      if self.conn is not None:
        para_list = []
        sql = "UPDATE selections SET"
        if selection.Name is not None:
          para_list.append(selection.Name)
          sql += " Name = ?"
        if selection.Event_Id is not None:
          para_list.append(selection.Event_Id)
          if sql[-3:] != "SET":
            sql += ","
          sql += " Event_Id = ?"
        if selection.Price is not None:
          para_list.append(selection.Price)
          if sql[-3:] != "SET":
            sql += ","
          sql += " Price = ?"
        if selection.Outcome is not None:
          para_list.append(selection.Outcome)
          if sql[-3:] != "SET":
            sql += ","
          sql += " Outcome = ?"

        if sql[-3:] != "SET":
          sql += " Where Id = ?"
          para_list.append(selection.Id)

          cur = self.conn.cursor()
          cur.execute(sql, para_list)
          self.conn.commit()

          if selection.Active is not None:
            isSuccess = self.set_event_active_value(selection.Event_Id)
          else:
            isSuccess = True
        else:
          isSuccess = True
      else:
        raise RuntimeError("database not connected!")
    except Error as e:
      print(e)

    return isSuccess

  def set_event_active_value(self, event_id):
    isSuccess = False
    try:
      if self.conn is not None:
        sql = "SELECT COUNT(Active) from selections WHERE Active = ? and Event_Id = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (1, event_id))
        count = cur.fetchone()[0]

        event_active = 0
        if count != 0:
          event_active = 1

        event = Event(event_id, None, None, event_active, None, None, None, None, None)
        isSuccess = self.update_event(event)
      else:
        raise RuntimeError("database not connected!")
    except Error as e:
      print(e)

    return isSuccess

  def set_sport_active_value(self, sport_id):
    isSuccess = False
    try:
      if self.conn is not None:
        sql = "SELECT COUNT(Active) from events WHERE Active = ? and Sport_Id = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (1, sport_id))
        count = cur.fetchone()[0]
        sport_active = 0
        if count != 0:
          sport_active = 1

        sport = Sport(sport_id, None, None, sport_active)
        isSuccess = self.update_sport(sport)
      else:
        raise RuntimeError("database not connected!")
    except Error as e:
      print(e)

    return isSuccess

  def disconnection(self):
    if self.conn:
      self.conn.close()