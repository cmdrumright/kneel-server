-- Kneel Diamonds Database setup
-- Run this block if you already have a database and need to re-create it
DELETE FROM Metals;
DELETE FROM Styles;
DELETE FROM Sizes;
DELETE FROM Orders;
DROP TABLE IF EXISTS Metals;
DROP TABLE IF EXISTS Styles;
DROP TABLE IF EXISTS Sizes;
DROP TABLE IF EXISTS Orders;
-- End block
-- Run this block to create the tables and seed them with some initial data
CREATE TABLE `Metals` (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`metal` NVARCHAR(160) NOT NULL,
	`price` NUMERIC(5, 2) NOT NULL
);
CREATE TABLE `Styles` (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`style` NVARCHAR(160) NOT NULL,
	`price` NUMERIC(5, 2) NOT NULL
);
CREATE TABLE `Sizes` (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`carets` NVARCHAR(160) NOT NULL,
	`price` NUMERIC(5, 2) NOT NULL
);
CREATE TABLE `Orders` (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`metal_id` INTEGER NOT NULL,
	`style_id` INTEGER NOT NULL,
	`size_id` INTEGER NOT NULL,
	FOREIGN KEY(`style_id`) REFERENCES `Styles`(`id`),
	FOREIGN KEY(`metal_id`) REFERENCES `Metals`(`id`),
	FOREIGN KEY(`size_id`) REFERENCES `Sizes`(`id`)
);
-- End Block