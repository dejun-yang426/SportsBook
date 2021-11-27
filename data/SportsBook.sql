-- create tables
CREATE TABLE IF NOT EXISTS sports (
	Id INTEGER PRIMARY KEY,
	Name NVARCHAR (255) NOT NULL,
        Slug NVARCHAR (255) NOT NULL,
        Active BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS events (
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
        FOREIGN KEY (Sport_Id) REFERENCES sports (Id)
);

CREATE TABLE IF NOT EXISTS selections (
	Id INTEGER PRIMARY KEY,
	Name NVARCHAR (255) NOT NULL,
        Event_Id INTEGER NOT NULL,
        Price DECIMAL (6, 2) NOT NULL,
        Active BOOLEAN DEFAULT 0,
        Outcome tinyint DEFAULT 1,
	-- Outcome: 1 = Unsettled; 2 = Void; 3 = Lost; 4 = Win
        FOREIGN KEY (Event_Id) REFERENCES events (Id)
);