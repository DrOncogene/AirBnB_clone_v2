-- sets up the sql test environment

-- create the test database
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- creates the test user
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- grant the user all privileges on test db
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- grant db user on the performance_schema db
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- commit all privilege changes
FLUSH PRIVILEGES;
