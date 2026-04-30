
CREATE TABLE HistoricalItems (
                                 IDNumber INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                 Name VARCHAR(50) NOT NULL,
                                 Category VARCHAR(20) NOT NULL,
                                 Description VARCHAR(1000),
                                 Date DATE
);
CREATE TABLE ItemsImages (
                             IDNumber INTEGER NOT NULL,
                             ImagePath VARCHAR(100) NOT NULL,
                             FOREIGN KEY (IDNumber) REFERENCES HistoricalItems(IDNumber),
                             PRIMARY KEY (IDNumber, ImagePath)
);
