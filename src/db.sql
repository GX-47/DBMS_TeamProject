-- File to create the database schema

-- Initial setup
DROP DATABASE IF EXISTS 'airline_management';
CREATE DATABASE 'airline_management';

USE 'airline_management';


-- Create tables
CREATE TABLE Passengers (
  Passenger_ID INT PRIMARY KEY,
  Name VARCHAR(100),
  Age INT,
  Gender VARCHAR(10)
);

CREATE TABLE Crew (
  Crew_ID INT PRIMARY KEY,
  Name VARCHAR(100),
  Salary DECIMAL(10, 2),
  Years_of_Service INT
);

CREATE TABLE Captain (
  Captain_ID INT PRIMARY KEY,
  Crew_ID INT,
  FOREIGN KEY (Crew_ID) REFERENCES Crew(Crew_ID)
);

CREATE TABLE Flights (
  Flight_ID INT PRIMARY KEY,
  Capacity INT,
  Model VARCHAR(50),
  Source VARCHAR(50),
  Destination VARCHAR(50),
  Departure DATETIME,
  Arrival DATETIME
);

CREATE TABLE Bookings (
  Booking_ID INT PRIMARY KEY,
  Passenger_ID INT,
  Flight_ID INT,
  Seat_no VARCHAR(10),
  Seat_type VARCHAR(20),
  FOREIGN KEY (Passenger_ID) REFERENCES Passengers(Passenger_ID),
  FOREIGN KEY (Flight_ID) REFERENCES Flights(Flight_ID)
);

CREATE TABLE Food (
  Item_ID INT PRIMARY KEY,
  Item_name VARCHAR(100),
  Cost DECIMAL(10, 2),
  Stock INT
);

CREATE TABLE Buys (
  Passenger_ID INT,
  Item_ID INT,
  PRIMARY KEY (Passenger_ID, Item_ID),
  FOREIGN KEY (Passenger_ID) REFERENCES Passengers(Passenger_ID),
  FOREIGN KEY (Item_ID) REFERENCES Food(Item_ID)
);

CREATE TABLE Serves (
  Crew_ID INT,
  Item_ID INT,
  PRIMARY KEY (Crew_ID, Item_ID),
  FOREIGN KEY (Crew_ID) REFERENCES Crew(Crew_ID),
  FOREIGN KEY (Item_ID) REFERENCES Food(Item_ID)
);

CREATE TABLE Luggage (
  Luggage_ID INT PRIMARY KEY,
  Passenger_ID INT,
  Type VARCHAR(50),
  FOREIGN KEY (Passenger_ID) REFERENCES Passengers(Passenger_ID)
);

CREATE TABLE Works_at (
  Crew_ID INT,
  Flight_ID INT,
  PRIMARY KEY (Crew_ID, Flight_ID),
  FOREIGN KEY (Crew_ID) REFERENCES Crew(Crew_ID),
  FOREIGN KEY (Flight_ID) REFERENCES Flights(Flight_ID)
);


-- Insert data
INSERT INTO Passengers (Passenger_ID, Name, Age, Gender) VALUES
(1, 'John Doe', 30, 'Male'),
(2, 'Jane Smith', 25, 'Female'),
(3, 'Alice Johnson', 28, 'Female');

INSERT INTO Crew (Crew_ID, Name, Salary, Years_of_Service) VALUES
(1, 'Michael Brown', 50000, 5),
(2, 'Sarah Davis', 55000, 7),
(3, 'David Wilson', 60000, 10);

INSERT INTO Captain (Captain_ID, Crew_ID) VALUES
(1, 3);

INSERT INTO Flights (Flight_ID, Capacity, Model, Source, Destination, Departure, Arrival) VALUES
(1, 180, 'Boeing 737', 'New York', 'Los Angeles', '2023-10-01 08:00:00', '2023-10-01 11:00:00'),
(2, 220, 'Airbus A320', 'Chicago', 'Miami', '2023-10-02 09:00:00', '2023-10-02 12:00:00');

INSERT INTO Bookings (Booking_ID, Passenger_ID, Flight_ID, Seat_no, Seat_type) VALUES
(1, 1, 1, '12A', 'Economy'),
(2, 2, 1, '12B', 'Economy'),
(3, 3, 2, '14C', 'Economy');

INSERT INTO Food (Item_ID, Item_name, Cost, Stock) VALUES
(1, 'Sandwich', 5.00, 50),
(2, 'Coffee', 3.00, 100),
(3, 'Juice', 4.00, 80);

INSERT INTO Buys (Passenger_ID, Item_ID) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO Serves (Crew_ID, Item_ID) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO Luggage (Luggage_ID, Passenger_ID, Type) VALUES
(1, 1, 'Checked'),
(2, 2, 'Carry-on'),
(3, 3, 'Checked');

INSERT INTO Works_at (Crew_ID, Flight_ID) VALUES
(1, 1),
(2, 1),
(3, 2);