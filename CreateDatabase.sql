CREATE Table HistoricalItems (
                                 IDNumber INT NOT NULL PRIMARY KEY,
                                 Name VARCHAR(50) NOT NULL,
                                 Description VARCHAR(1000),
                                 Date DATE,
                                 ImagePath VARCHAR(200) NOT NULL
);
