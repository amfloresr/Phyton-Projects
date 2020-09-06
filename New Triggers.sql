use sales;
-- ---------------------------------------------------------------------------------------------------
							-- TRIGEGERS ON THE ORDERS TABLE

				-- Auto set the date                            
-- Set the creation date of the order
CREATE TRIGGER placement_date_orders BEFORE INSERT ON orders
FOR EACH ROW
    SET new.placement_date = now();                            
    
				-- Creates a record into shipping  with the same order_id
CREATE TRIGGER shipping_entry AFTER INSERT ON orders
FOR EACH ROW
INSERT INTO shipping 
VALUES();
				-- Creates a record into payments with the same order_id
CREATE TRIGGER payments_entry AFTER INSERT ON orders
FOR EACH ROW
INSERT INTO payments (half_order_price, full_order_price, tracking_id)
VALUES(0.5*(SELECT full_order_price from orders where order_id=last_insert_id()),
(SELECT full_order_price from orders where order_id=last_insert_id()),
(SELECT tracking_id from shipping where shipping.order_id=order_id=last_insert_id()));
				-- Creates a record into products with the same order_id
CREATE TRIGGER product_entry AFTER INSERT ON orders
FOR EACH ROW
INSERT INTO products 
VALUES();

				-- Creates a record into local_shipping with the same order_id
CREATE TRIGGER local_shipping_entry AFTER INSERT ON orders
FOR EACH ROW
INSERT INTO local_shipping
VALUES();
-- ---------------------------------------------------------------------------------------------------
							-- TRIGGERS ON THE SHIPPING TABLE

				-- auto sets the rate on the shipping table
CREATE TRIGGER shipping_rate BEFORE INSERT ON shipping
FOR EACH ROW
-- Set the rate based on the transportation
SET new.rating= IF(new.transport="aéreo" , 4.7, 1.5);
