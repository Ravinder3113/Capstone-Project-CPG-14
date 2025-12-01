-- login: mysql -u root -p

CREATE DATABASE IF NOT EXISTS anpr_mysql
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'anpr_user'@'%' IDENTIFIED BY 'ANPR_STRONG_PASSWORD';
GRANT ALL PRIVILEGES ON anpr_mysql.* TO 'anpr_user'@'%';

USE anpr_mysql;

CREATE TABLE numberplate (

  id INT AUTO_INCREMENT PRIMARY KEY,
  plate VARCHAR(64) NOT NULL,
  timestamp DATETIME NULL,
  location VARCHAR(255) NULL,
  latitude DOUBLE NOT NULL,
  longitude DOUBLE NOT NULL,
  location_point POINT NOT NULL SRID 4326,
  inserted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  SPATIAL INDEX(location_point)
) ENGINE=InnoDB;
#drop table numberplate;
select * from numberplate;

SELECT id, plate
FROM numberplate
ORDER BY inserted_at DESC;

SELECT id,
       plate,
       DATE_FORMAT(`timestamp`, '%Y-%m-%d %H:%i:%s') AS timestamp_formatted
FROM numberplate
ORDER BY `timestamp` DESC;

SELECT id,
       plate,
       DATE_FORMAT(`timestamp`, '%Y-%m-%d %H:%i:%s') AS ts,
       `location`,
       ST_Y(location_point) AS latitude_from_point,
       ST_X(location_point) AS longitude_from_point,
       ST_AsText(location_point) AS location_wkt
FROM numberplate
ORDER BY `timestamp` DESC;

SELECT plate, COUNT(*) AS detections
FROM numberplate
GROUP BY plate
ORDER BY detections DESC;
