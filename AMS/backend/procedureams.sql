DELIMITER //
CREATE PROCEDURE update_food_stock(IN item_name VARCHAR(50), IN new_stock INT)
BEGIN
    UPDATE Food SET Stock = new_stock WHERE Item_name = item_name;
END //
DELIMITER ;
