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
	`carets` NUMERIC(5, 2) NOT NULL,
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
INSERT INTO Metals
VALUES (null, 'Sterling Silver', 12.42);
INSERT INTO Metals
VALUES (null, '14K Gold', 736.4);
INSERT INTO Metals
VALUES (null, '24K Gold', 1258.9);
INSERT INTO Metals
VALUES (null, 'Platinum', 795.45);
INSERT INTO Metals
VALUES (null, 'Palladium', 1241);
INSERT INTO Styles
VALUES (null, 'Classic', 500);
INSERT INTO Styles
VALUES (null, 'Modern', 710);
INSERT INTO Styles
VALUES (null, 'Vintage', 965);
INSERT INTO Sizes
VALUES (null, 0.5, 405);
INSERT INTO Sizes
VALUES (null, 0.75, 782);
INSERT INTO Sizes
VALUES (null, 1, 1470);
INSERT INTO Sizes
VALUES (null, 1.5, 1997);
INSERT INTO Sizes
VALUES (null, 2, 3638);
INSERT INTO Orders
VALUES (null, 2, 2, 2);
INSERT INTO Orders
VALUES (null, 2, 3, 4);
INSERT INTO Orders
VALUES (null, 4, 1, 3);
-- End Block