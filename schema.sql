-- Active: 1747297103967@@127.0.0.1@3306@plant_db
CREATE DATABASE plant_db;
USE plant_db;
CREATE TABLE plants(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR (255) NOT NULL,
species VARCHAR(255),
last_watered DATE,
water_frequency INT COMMENT 'days',
sunlight_requirements VARCHAR(50),
photo_url VARCHAR(512)
);

SHOW DATABASES;
