DROP DATABASE railroad_nakhod;
CREATE DATABASE railroad_nakhod;
USE railroad_nakhod;

CREATE TABLE user_role (
    id INT AUTO_INCREMENT,
    name VARCHAR(50),
    PRIMARY KEY (id)
);

CREATE TABLE user (
    id INT AUTO_INCREMENT,
    name VARCHAR(50),
    email VARCHAR(50),
    password_hash CHAR(60),
    user_role_id INT,
    confirmed_email BOOLEAN DEFAULT FALSE,
    confirm_email_token VARCHAR(50),
    reset_password_token VARCHAR(50),
    PRIMARY KEY (id),
    FOREIGN KEY (user_role_id)
        REFERENCES user_role(id)
        ON DELETE SET NULL
);

CREATE TABLE train (
    id INT AUTO_INCREMENT,
    name VARCHAR(50),
    PRIMARY KEY (id)
);

CREATE TABLE station (
    id INT AUTO_INCREMENT,
    name VARCHAR(50), 
    PRIMARY KEY (id)
);

CREATE TABLE trip (
    id INT AUTO_INCREMENT,
    train_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (train_id)
        REFERENCES train(id)
        ON DELETE SET NULL
);

CREATE TABLE trip_station (
    id INT AUTO_INCREMENT,
    trip_id INT,
    station_id INT,
    num INT,
    time_arr DATETIME,
    time_dep DATETIME,
    price INT,
    PRIMARY KEY (id),
    FOREIGN KEY (trip_id)
        REFERENCES trip(id)
        ON DELETE SET NULL,
    FOREIGN KEY (station_id)
        REFERENCES station(id)
        ON DELETE SET NULL
);

CREATE TABLE carriage_type (
    id INT AUTO_INCREMENT,
    name VARCHAR(50),
    price_mod INT,
    PRIMARY KEY (id)
);

CREATE TABLE carriage (
    id INT AUTO_INCREMENT,
    num INT,
    train_id INT,
    carriage_type_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (train_id)
        REFERENCES train(id)
        ON DELETE SET NULL,
    FOREIGN KEY (carriage_type_id)
        REFERENCES carriage_type(id)
        ON DELETE SET NULL
);

CREATE TABLE seat (
    id INT AUTO_INCREMENT,
    num INT,
    carriage_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (carriage_id)
        REFERENCES carriage(id)
        ON DELETE SET NULL
);

CREATE TABLE ticket (
    id INT AUTO_INCREMENT,
    user_id INT,
    seat_id INT,
    trip_station_start_id INT,
    trip_station_end_id INT,
    token VARCHAR(50),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id)
        REFERENCES user(id)
        ON DELETE SET NULL,
    FOREIGN KEY (seat_id)
        REFERENCES seat(id)
        ON DELETE SET NULL,
    FOREIGN KEY (trip_station_start_id)
        REFERENCES trip_station(id)
        ON DELETE SET NULL,
    FOREIGN KEY (trip_station_end_id)
        REFERENCES trip_station(id)
        ON DELETE SET NULL
);





INSERT INTO user_role (
    name
)
VALUES (
    'admin'
),
(
    'client'
);

INSERT INTO user (
    name,
    email,
    password_hash,
    user_role_id,
    confirmed_email
)
VALUES (
    'admin',
    'admin@admin.com',
    '$2a$12$1VrvxyQGSU0dPyCvYP1R2.ES5odC9BcRdrcUYMY.U6Axt.TJre.sa',
    (SELECT id FROM user_role WHERE name = 'admin'),
    TRUE
),
(
    'Oleksii',
    'alexey.nakhod@gmail.com',
    '$2a$12$V1vo5iRM33tdkeRw4scmbuGeq1Sl4W8ugGNn9xkhnELjKN2GLcZUK',
    (SELECT id FROM user_role WHERE name = 'client'),
    TRUE
);

INSERT INTO train (
    name
)
VALUES (
    '100T'
),
(
    '200T'
),
(
    '300T'
);

INSERT INTO carriage_type (
    name,
    price_mod
)
VALUES (
    '1st class',
    3
),
(
    '2nd class',
    2
),
(
    '3rd class',
    1
);

INSERT INTO carriage (
    num,
    train_id,
    carriage_type_id
)
VALUES (
    1,
    (SELECT id FROM train WHERE name = '100T'),
    (SELECT id FROM carriage_type WHERE name = '1st class')
),
(
    2,
    (SELECT id FROM train WHERE name = '100T'),
    (SELECT id FROM carriage_type WHERE name = '1st class')
),
(
    3,
    (SELECT id FROM train WHERE name = '100T'),
    (SELECT id FROM carriage_type WHERE name = '2nd class')
),
(
    4,
    (SELECT id FROM train WHERE name = '100T'),
    (SELECT id FROM carriage_type WHERE name = '2nd class')
),
(
    5,
    (SELECT id FROM train WHERE name = '100T'),
    (SELECT id FROM carriage_type WHERE name = '3rd class')
),
(
    6,
    (SELECT id FROM train WHERE name = '100T'),
    (SELECT id FROM carriage_type WHERE name = '3rd class')
);

INSERT INTO seat (
    num,
    carriage_id
)
VALUES (
    1,
    (SELECT id FROM carriage WHERE train_id = (SELECT id FROM train WHERE name = '100T') AND num = 1)
),
(
    2,
    (SELECT id FROM carriage WHERE train_id = (SELECT id FROM train WHERE name = '100T') AND num = 1)
),
(
    3,
    (SELECT id FROM carriage WHERE train_id = (SELECT id FROM train WHERE name = '100T') AND num = 1)
),
(
    4,
    (SELECT id FROM carriage WHERE train_id = (SELECT id FROM train WHERE name = '100T') AND num = 1)
),
(
    2,
    (SELECT id FROM carriage WHERE train_id = (SELECT id FROM train WHERE name = '100T') AND num = 2)
),
(
    1,
    (SELECT id FROM carriage WHERE train_id = (SELECT id FROM train WHERE name = '100T') AND num = 3)
),
(
    3,
    (SELECT id FROM carriage WHERE train_id = (SELECT id FROM train WHERE name = '100T') AND num = 3)
),
(
    4,
    (SELECT id FROM carriage WHERE train_id = (SELECT id FROM train WHERE name = '100T') AND num = 3)
);



INSERT INTO station (
    name
)
VALUES (
    'Kyiv'
),
(
    'Lviv'
),
(
    'Dnipro'
),
(
    'Kharkiv'
),
(
    'Zaporizhzhia'
),
(
    'Mykolaiv'
),
(
    'Odesa'
);

INSERT INTO trip (
    train_id
)
VALUES (
    (SELECT id FROM train WHERE name = '100T')
),
(
    (SELECT id FROM train WHERE name = '200T')
);

INSERT INTO trip_station (
    trip_id,
    num,
    station_id,
    time_arr,
    time_dep,
    price
)
VALUES (
    (SELECT id FROM trip WHERE train_id = (SELECT id FROM train WHERE name = '100T')),
    1,
    (SELECT id FROM station WHERE name = 'Kyiv'),
    '2023-03-27 12:30:00',
    '2023-03-27 13:00:00',
    0
),
(
    (SELECT id FROM trip WHERE train_id = (SELECT id FROM train WHERE name = '100T')),
    2,
    (SELECT id FROM station WHERE name = 'Dnipro'),
    '2023-03-27 16:00:00',
    '2023-03-27 16:30:00',
    40000
),
(
    (SELECT id FROM trip WHERE train_id = (SELECT id FROM train WHERE name = '100T')),
    3,
    (SELECT id FROM station WHERE name = 'Kharkiv'),
    '2023-03-27 19:00:00',
    '2023-03-27 19:00:00',
    70000
),
(
    (SELECT id FROM trip WHERE train_id = (SELECT id FROM train WHERE name = '200T')),
    1,
    (SELECT id FROM station WHERE name = 'Kyiv'),
    '2023-03-27 19:00:00',
    '2023-03-27 19:30:00',
    0
),
(
    (SELECT id FROM trip WHERE train_id = (SELECT id FROM train WHERE name = '200T')),
    2,
    (SELECT id FROM station WHERE name = 'Dnipro'),
    '2023-03-27 21:35:00',
    '2023-03-27 21:35:00',
    30000
);