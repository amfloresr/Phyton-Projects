DROP DATABASE SALES;
CREATE DATABASE IF NOT EXISTS Sales;
USE Sales;

CREATE TABLE orders(
	order_id 			INT AUTO_INCREMENT PRIMARY KEY,
    customer_id 		INT,
	shop_id 			INT,
    placement_date 		DATETIME,
    order_status 		ENUM("INCOMPLETE","COMPLETED") DEFAULT "INCOMPLETE",
    bill_img 			BLOB,
	full_order_price 	FLOAT
    );

CREATE TABLE customers(
	customer_id 	INT AUTO_INCREMENT PRIMARY KEY,
    first_name		VARCHAR(255),
    second_name		VARCHAR(255),
    phone_number	INT UNIQUE KEY,
    email_address	VARCHAR(255) UNIQUE KEY,
    number_of_orders INT
);

CREATE TABLE shops(
	shop_id			INT AUTO_INCREMENT PRIMARY KEY,
    shop_name 		VARCHAR(255) UNIQUE KEY,
    shop_webpage 	VARCHAR(255) UNIQUE KEY
    );
    
CREATE TABLE shipping(
	order_id	  	INT AUTO_INCREMENT PRIMARY KEY,
    tracking_id	    VARCHAR(255) UNIQUE KEY,
    carrier_id 		INT,
    transport 		ENUM("aéreo", "marítimo") DEFAULT "aéreo",
    rating 			FLOAT,
    weight			INT,
    shipping_status	ENUM("On Way to Miami", "Delayed","Missing","Received at Miami", "On way to Honduras", "Received at Honduras")
    );
    
CREATE TABLE local_shipping(
	order_id 			 	INT AUTO_INCREMENT PRIMARY KEY,
    local_tracking 			VARCHAR(255) UNIQUE KEY,
    tracking_id				VARCHAR(255) UNIQUE KEY,
    local_carrier_id 		INT DEFAULT 1,
    local_shipping_status 	ENUM("On the way to client", "Received by client", "Delayed","Missing")
    );

CREATE TABLE carriers(
	carrier_id		INT AUTO_INCREMENT PRIMARY KEY,
    carrier_name 	VARCHAR(255),
    carrier_webpage VARCHAR(255)
    );

CREATE TABLE local_carrier(
	local_carrier_id 		INT AUTO_INCREMENT PRIMARY KEY,
    local_carrier_name 		VARCHAR(255),
    local_carrier_address 	VARCHAR(255),
    local_carrier_phone 	INT
    );

CREATE TABLE products(
	order_id 		INT AUTO_INCREMENT PRIMARY KEY,
    shop_id 		INT,
    product_name 	VARCHAR(255),
    product_url 	VARCHAR(255)
    );

CREATE TABLE payments(
	order_id 				INT AUTO_INCREMENT PRIMARY KEY,
    half_order_price		FLOAT,
    half_payment_status 	ENUM("Pending", "Completed") DEFAULT "Pending", 
    full_order_price 		FLOAT,
    order_payment_date 		DATETIME,
    full_payment_status 	ENUM("Pending", "Completed") DEFAULT "Pending",
    tracking_id 			VARCHAR(255) UNIQUE KEY,
    dolar_exchange			FLOAT DEFAULT 25.02,
    flete					INT DEFAULT 85,
    shipping_subtotal 		FLOAT,
    shipping_taxes 			FLOAT Default 0.15,
    shipping_total 			FLOAT,
	shipping_payment_date 	DATETIME,
    shipping_payment_status	ENUM("Pending", "Completed") DEFAULT "Pending",
    local_tracking 			VARCHAR(255),
    local_shipping_total	FLOAT,
    LS_payment_status 		ENUM("Pending", "Completed"),
	LS_payment_date 		DATETIME
    );
    
ALTER TABLE orders ADD FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE;

ALTER TABLE orders ADD FOREIGN KEY (shop_id) REFERENCES shops(shop_id);

-- ALTER TABLE shipping ADD FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE;

ALTER TABLE shipping ADD FOREIGN KEY (carrier_id) REFERENCES carriers(carrier_id);

-- ALTER TABLE local_shipping ADD FOREIGN KEY (order_id) REFERENCES orders(order_id);

ALTER TABLE local_shipping ADD FOREIGN KEY (tracking_id) REFERENCES shipping(tracking_id);

ALTER TABLE local_shipping ADD FOREIGN KEY (local_carrier_id) REFERENCES local_carrier(local_carrier_id);

ALTER TABLE payments ADD FOREIGN KEY (tracking_id) REFERENCES shipping(tracking_id);

ALTER TABLE payments ADD FOREIGN KEY (local_tracking) REFERENCES local_shipping(local_tracking);

ALTER TABLE products ADD FOREIGN KEY (shop_id) REFERENCES shops(shop_id);
