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

INSERT INTO `flight` VALUES
('FL1', 'AL1', 'Delhi', 'Mumbai', '2024-12-14 10:00:00', '2024-12-14 12:00:00', 180, 5000.00),
('FL2', 'AL1', 'Mumbai', 'Bangalore', '2024-12-14 14:00:00', '2024-12-14 16:00:00', 180, 4500.00),
('FL3', 'AL2', 'Bangalore', 'Delhi', '2024-12-14 18:00:00', '2024-12-14 20:30:00', 160, 6000.00),
('FL4', 'AL1', 'Delhi', 'London', '2024-12-15 08:00:00', '2024-12-15 14:00:00', 200, 15000.00), -- Premium flight
('FL5', 'AL1', 'Mumbai', 'New York', '2024-12-16 06:00:00', '2024-12-16 18:00:00', 200, 20000.00), -- Premium flight
('FL6', 'AL1', 'Mumbai', 'Bangalore', '2024-11-25 14:00:00', '2024-11-21 16:00:00', 180, 4500.00),
('FL7', 'AL1', 'Mumbai', 'Bangalore', '2024-11-20 14:00:00', '2024-11-21 16:00:00', 180, 4500.00);

INSERT INTO `food_menu` VALUES 
('F1', 'Veg Meal', 300.00),
('F2', 'Non-Veg Meal', 350.00),
('F3', 'Snacks', 150.00),
('F4', 'Beverages', 100.00);

INSERT INTO `booking` VALUES
('B1', 'P_1', 'FL1', '2024-12-01', 5000.00, 'Confirmed', 'AL1'),
('B2', 'P_2', 'FL2', '2024-12-02', 4500.00, 'Pending', 'AL1'),
('B3', 'P_3', 'FL3', '2024-12-03', 6000.00, 'Confirmed', 'AL2');

INSERT INTO `passenger_details` VALUES
('D1', 'B1', 'Akash', '12A', 'Veg'),
('D2', 'B2', 'Bob Brown', '14B', 'Non-Veg'),
('D3', 'B3', 'Charlie Davis', '16C', 'Veg');

INSERT INTO `luggage` VALUES
('L1', 'B1', 15.00, 'Checked', 'Handle with care', '2024-12-14 08:00:00', 'FD1'),
('L2', 'B2', 20.00, 'Checked', 'Fragile', '2024-12-14 12:00:00', 'FD2'),
('L3', 'B3', 10.00, 'Carry-on', NULL, '2024-12-14 16:00:00', 'FD1');

INSERT INTO `booking_food` VALUES
('B1', 'F1', 1),
('B2', 'F2', 2),
('B3', 'F3', 3);

-- 1. Nested Query: Get flights with higher than average price
CREATE VIEW expensive_flights AS
SELECT f.*, a.airline_name, 
       CONCAT(ROUND((f.price / (SELECT AVG(price) FROM flight)) * 100 - 100, 1), '%') as price_above_avg
FROM flight f
JOIN airline a ON f.airline_id = a.airline_id
WHERE f.price > (SELECT AVG(price) FROM flight);

-- 2. Join Query: Get comprehensive booking details
CREATE OR REPLACE VIEW booking_full_details AS
SELECT 
    b.booking_id,
    p.name as passenger_name,
    f.flight_id,
    a.airline_name,
    f.origin,
    f.destination,
    f.departure_time,
    pd.seat_number,
    pd.meal_preference,
    GROUP_CONCAT(CONCAT(fm.food_name, ' (', bf.quantity, ')')) as food_orders,
    b.total_price,
    b.status
FROM booking b
JOIN passenger p ON b.passenger_id = p.passenger_id
JOIN flight f ON b.flight_id = f.flight_id
JOIN airline a ON b.airline_id = a.airline_id
JOIN passenger_details pd ON b.booking_id = pd.booking_id
LEFT JOIN booking_food bf ON b.booking_id = bf.booking_id
LEFT JOIN food_menu fm ON bf.food_id = fm.food_id
GROUP BY b.booking_id, p.name, f.flight_id, a.airline_name, f.origin, f.destination, f.departure_time, pd.seat_number, pd.meal_preference, b.total_price, b.status;

-- 3. Aggregate Query: Get airline performance metrics
CREATE VIEW airline_metrics AS
SELECT 
    a.airline_id,
    a.airline_name,
    COUNT(DISTINCT f.flight_id) as total_flights,
    COUNT(DISTINCT b.booking_id) as total_bookings,
    ROUND(AVG(f.price), 2) as avg_ticket_price,
    SUM(b.total_price) as total_revenue,
    ROUND(COUNT(b.booking_id) * 100.0 / COUNT(DISTINCT f.flight_id), 1) as bookings_per_flight
FROM airline a
LEFT JOIN flight f ON a.airline_id = f.airline_id
LEFT JOIN booking b ON f.flight_id = b.flight_id
GROUP BY a.airline_id;

-- 4. Procedure: Calculate and update flight delays
DELIMITER //
CREATE PROCEDURE UpdateFlightDelays()
BEGIN
    UPDATE flight f
    SET f.status = CASE 
        WHEN TIMESTAMPDIFF(MINUTE, f.departure_time, NOW()) > 30 AND f.departure_time < NOW() THEN 'Delayed'
        WHEN f.departure_time > NOW() THEN 'On Time'
        ELSE 'Departed'
    END
    WHERE f.departure_time >= CURDATE();
END //
DELIMITER ;

-- 5. Function: Calculate booking price with dynamic discount
DELIMITER //
CREATE FUNCTION CalculateDiscountedPrice(
    base_price DECIMAL(8,2),
    booking_date DATE,
    flight_date DATETIME
) 
RETURNS DECIMAL(8,2)
DETERMINISTIC
BEGIN
    DECLARE final_price DECIMAL(8,2);
    DECLARE days_until_flight INT;
    
    SET days_until_flight = DATEDIFF(flight_date, booking_date);
    
    IF days_until_flight > 10 THEN
        SET final_price = base_price * 0.9; -- 10% early bird discount
    ELSEIF days_until_flight < 2 THEN
        SET final_price = base_price * 1.2; -- 20% last minute markup
    ELSE
        SET final_price = base_price;
    END IF;
    
    RETURN final_price;
END //
DELIMITER ;

-- 6. Trigger: Automatically update flight capacity after booking
DELIMITER //
CREATE TRIGGER after_booking_insert
AFTER INSERT ON booking
FOR EACH ROW
BEGIN
    UPDATE flight f
    SET f.capacity = f.capacity - 1
    WHERE f.flight_id = NEW.flight_id
    AND f.capacity > 0;
END //
DELIMITER ;

-- Add status column to flight table
ALTER TABLE flight ADD COLUMN status VARCHAR(20) DEFAULT 'On Time';