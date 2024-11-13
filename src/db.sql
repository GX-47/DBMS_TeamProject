CREATE DATABASE IF NOT EXISTS `airline_system`;

USE `airline_system`;

CREATE TABLE `passenger` (
  `passenger_id` VARCHAR(10) NOT NULL,
  `phone` VARCHAR(15) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL check (email like '%@%'),
  `password` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`passenger_id`)
);

CREATE TABLE `airline` (
  `airline_id` VARCHAR(10) NOT NULL,
  `airline_name` VARCHAR(50) NOT NULL,
  `hub_location` VARCHAR(50) NOT NULL,
  `rating` DECIMAL(2,1) NOT NULL,
  `password` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`airline_id`)
);

CREATE TABLE `flight` (
  `flight_id` VARCHAR(10) NOT NULL,
  `airline_id` VARCHAR(10) NOT NULL,
  `origin` VARCHAR(50) NOT NULL,
  `destination` VARCHAR(50) NOT NULL,
  `departure_time` DATETIME NOT NULL,
  `arrival_time` DATETIME NOT NULL,
  `capacity` INT NOT NULL,
  `price` DECIMAL(8,2) NOT NULL,
  PRIMARY KEY (`flight_id`),
  FOREIGN KEY (`airline_id`) REFERENCES `airline`(`airline_id`) ON DELETE CASCADE
);

CREATE TABLE `booking` (
  `booking_id` VARCHAR(10) NOT NULL,
  `passenger_id` VARCHAR(10) NOT NULL,
  `flight_id` VARCHAR(10) NOT NULL,
  `booking_date` DATE NOT NULL,
  `total_price` DECIMAL(8,2) NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `airline_id` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`booking_id`),
  FOREIGN KEY (`passenger_id`) REFERENCES `passenger`(`passenger_id`) ON DELETE CASCADE,
  FOREIGN KEY (`flight_id`) REFERENCES `flight`(`flight_id`) ON DELETE CASCADE,
  FOREIGN KEY (`airline_id`) REFERENCES `airline`(`airline_id`) ON DELETE CASCADE
);

CREATE TABLE `passenger_details` (
  `detail_id` VARCHAR(20) NOT NULL,
  `booking_id` VARCHAR(10) NOT NULL,
  `passenger_name` VARCHAR(50) NOT NULL,
  `seat_number` VARCHAR(10) NOT NULL,
  `meal_preference` VARCHAR(20),
  PRIMARY KEY (`detail_id`),
  FOREIGN KEY (`booking_id`) REFERENCES `booking`(`booking_id`) ON DELETE CASCADE
);

CREATE TABLE `frontdesk_staff` (
  `staff_id` VARCHAR(10) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `password` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`staff_id`)
);

CREATE TABLE `analyst_staff` (
  `staff_id` VARCHAR(10) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `password` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`staff_id`)
);

CREATE TABLE `luggage` (
  `luggage_id` VARCHAR(10) NOT NULL,
  `booking_id` VARCHAR(10) NOT NULL,
  `weight` DECIMAL(5,2) NOT NULL,
  `category` VARCHAR(20) NOT NULL,
  `handling_instructions` VARCHAR(100),
  `check_in_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `staff_id` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`luggage_id`),
  FOREIGN KEY (`booking_id`) REFERENCES `booking`(`booking_id`) ON DELETE CASCADE,
  FOREIGN KEY (`staff_id`) REFERENCES `frontdesk_staff`(`staff_id`) ON DELETE CASCADE
);

CREATE TABLE `food_menu` (
  `food_id` VARCHAR(10) NOT NULL,
  `food_name` VARCHAR(50) NOT NULL,
  `price` DECIMAL(5,2) NOT NULL,
  PRIMARY KEY (`food_id`)
);

CREATE TABLE `booking_food` (
  `booking_id` VARCHAR(10) NOT NULL,
  `food_id` VARCHAR(10) NOT NULL,
  `quantity` INT NOT NULL,
  PRIMARY KEY (`booking_id`, `food_id`),
  FOREIGN KEY (`booking_id`) REFERENCES `booking`(`booking_id`) ON DELETE CASCADE,
  FOREIGN KEY (`food_id`) REFERENCES `food_menu`(`food_id`) ON DELETE CASCADE
);

CREATE TABLE `admin` (
  `admin_id` VARCHAR(10) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `password` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`admin_id`)
);

-- Stored procedure to confirm booking
DELIMITER //
CREATE PROCEDURE ConfirmBooking(IN passengerId VARCHAR(10))
BEGIN
    UPDATE `booking` SET 
        status = 'Confirmed'
    WHERE passenger_id = passengerId AND status = 'Pending';
END //
DELIMITER ;

-- Function to calculate total price with taxes
DELIMITER //
CREATE FUNCTION CalculateTotalPrice(base_price DECIMAL(8,2)) 
RETURNS DECIMAL(8,2) READS SQL DATA
BEGIN
    DECLARE total DECIMAL(8,2);
    -- Adding 18% tax
    SET total = base_price * 1.18;
    RETURN total;
END //
DELIMITER ;

-- Sample data
INSERT INTO `admin` VALUES 
('AD1', 'Admin', 'admin123');

INSERT INTO `passenger` VALUES 
('P_1', '9876543210', 'Akash', 'a@a.com', 'admin@123'),
('P_2', '8765432109', 'Bob Brown', 'bob@example.com', 'bob123'),
('P_3', '7654321098', 'Charlie Davis', 'charlie@example.com', 'charlie123');

INSERT INTO `airline` VALUES 
('AL1', 'Air India', 'Delhi', 4.2, 'airindia123'),
('AL2', 'IndiGo', 'Mumbai', 4.5, 'indigo123'),
('AL3', 'SpiceJet', 'Bangalore', 4.0, 'spice123');

INSERT INTO `frontdesk_staff` VALUES 
('FD1', 'John Doe', 'john@airline.com', 'front123'),
('FD2', 'Jane Smith', 'jane@airline.com', 'desk123');

INSERT INTO `analyst_staff` VALUES 
('AN1', 'Alice Johnson', 'alice@airline.com', 'analyst123'),
('AN2', 'Bob Williams', 'bob@airline.com', 'analysis456');

INSERT INTO `flight` VALUES
('FL1', 'AL1', 'Delhi', 'Mumbai', '2024-11-14 10:00:00', '2024-11-14 12:00:00', 180, 5000.00),
('FL2', 'AL1', 'Mumbai', 'Bangalore', '2024-11-14 14:00:00', '2024-11-14 16:00:00', 180, 4500.00),
('FL3', 'AL2', 'Bangalore', 'Delhi', '2024-11-14 18:00:00', '2024-11-14 20:30:00', 160, 6000.00);

INSERT INTO `food_menu` VALUES 
('F1', 'Veg Meal', 300.00),
('F2', 'Non-Veg Meal', 350.00),
('F3', 'Snacks', 150.00),
('F4', 'Beverages', 100.00);

INSERT INTO `booking` VALUES
('B1', 'P_1', 'FL1', '2024-11-01', 5000.00, 'Confirmed', 'AL1'),
('B2', 'P_2', 'FL2', '2024-11-02', 4500.00, 'Pending', 'AL1'),
('B3', 'P_3', 'FL3', '2024-11-03', 6000.00, 'Confirmed', 'AL2');

INSERT INTO `passenger_details` VALUES
('D1', 'B1', 'Akash', '12A', 'Veg'),
('D2', 'B2', 'Bob Brown', '14B', 'Non-Veg'),
('D3', 'B3', 'Charlie Davis', '16C', 'Veg');

INSERT INTO `luggage` VALUES
('L1', 'B1', 15.00, 'Checked', 'Handle with care', '2024-11-14 08:00:00', 'FD1'),
('L2', 'B2', 20.00, 'Checked', 'Fragile', '2024-11-14 12:00:00', 'FD2'),
('L3', 'B3', 10.00, 'Carry-on', NULL, '2024-11-14 16:00:00', 'FD1');

INSERT INTO `booking_food` VALUES
('B1', 'F1', 1),
('B2', 'F2', 2),
('B3', 'F3', 3);

