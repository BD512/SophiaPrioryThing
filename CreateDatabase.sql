DROP TABLE HistoricalItems;
DROP TABLE ItemsImages;
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
INSERT INTO HistoricalItems (Name, Category, Description, Date)
VALUES ('Gold candle','Candle','It is a very pretty candle', '01/05/2026');
INSERT INTO HistoricalItems (Name, Category, Description, Date)
VALUES ('White cloth', 'Cloth', 'Nice cloth', '17th century');


