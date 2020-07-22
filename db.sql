CREATE TABLE Users (
    UserId int NOT NULL AUTO_INCREMENT,
    Username varchar(255) NOT NULL UNIQUE,
    Password varchar(255) NOT NULL,
    Name varchar(255) NOT NULL,
    Email varchar(255) NOT NULL UNIQUE,
    Token varchar(255) UNIQUE,
    ImagePath varchar(255),
    PRIMARY KEY (UserId)
); 


CREATE TABLE Contacts (
    ContactId int NOT NULL AUTO_INCREMENT,
    user_id integer NOT NULL,
    ContactName varchar(255) NOT NULL,
    ContactPhone char(14) NOT NULL,
    PRIMARY KEY (ContactId),
    FOREIGN KEY (user_id) REFERENCES Users(UserId)
);

INSERT INTO Users (Username, Password) VALUES (eder, dd); 

SELECT * FROM Contacts WHERE user_id = (SELECT UserId FROM Users WHERE Username = "eder");

INSERT INTO `Contacts` (`user_id`, `ContactName`, `ContactPhone`) VALUES ('6', 'Pedro', '333422323');