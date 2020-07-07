CREATE TABLE Users (
    UserId int NOT NULL AUTO_INCREMENT,
    Username varchar(255) NOT NULL UNIQUE,
    Password varchar(255) NOT NULL,
    PRIMARY KEY (UserId)
); 


CREATE TABLE Contacts (
    ContactId int NOT NULL AUTO_INCREMENT,
    user_id integer NOT NULL,
    ContactName varchar(255) NOT NULL,
    ContactPhone char(10) NOT NULL,
    PRIMARY KEY (ContactId),
    FOREIGN KEY (user_id) REFERENCES Users(UserId)
);

