-- sets up the sql dev environment

-- create the development database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- creates the dev user
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- grant the user all privileges on dev db
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- grant db user on the performance_schema db
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- commit all privilege changes
FLUSH PRIVILEGES;
