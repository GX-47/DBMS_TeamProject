CREATE TABLE IF NOT EXISTS FlightLogs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(255),
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE TRIGGER flight_insert_trigger
AFTER INSERT ON Flight
FOR EACH ROW
BEGIN
    INSERT INTO FlightLogs (message) VALUES (CONCAT('New flight added with ID ', NEW.Flight_ID));
END //
DELIMITER ;