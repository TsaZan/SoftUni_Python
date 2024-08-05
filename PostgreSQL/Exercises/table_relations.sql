create table products
(
    product_name VARCHAR(100)
);
insert into products
values ('Broccoli'),
       ('Shampoo'),
       ('Toothpaste'),
       ('Candy');

alter table products
    add column id serial primary key;

alter table products
    drop constraint
        products_pkey;


create table passports
(
    id          integer generated always as identity (start with 100 increment by 1) primary key,
    nationality varchar(50)
);

insert into passports(nationality)
values ('N34FG21B'),
       ('K65LO4R7'),
       ('ZE657QP2');

create table people
(
    id          serial primary key,
    first_name  varchar(50),
    salary      numeric(10, 2),
    passport_id integer,

    constraint fk_people_passport
        foreign key (passport_id)
            references passports (id)

);


insert into people(first_name, salary, passport_id)
values ('Roberto', 43300.0000, 101),
       ('Tom', 56100.0000, 102),
       ('Yana', 60200.0000, 100);


create table manufacturers
(
    id   serial primary key,
    name varchar(50)
);

create table models
(
    id              integer generated always as identity (start with 1000 increment by 1) primary key,
    model_name      varchar(50),
    manufacturer_id int,

    constraint fk_models_manufacturers
        foreign key (manufacturer_id)
            references manufacturers (id)

);
create table production_years
(
    id              integer generated always as identity primary key,
    established_on  date,
    manufacturer_id int,

    constraint fk_year_manufacturers
        foreign key (manufacturer_id)
            references manufacturers (id)
);

insert into manufacturers(name)
values ('BMW'),
       ('Tesla'),
       ('Lada');

INSERT INTO models(model_name, manufacturer_id)
VALUES ('X1', 1),
       ('i6', 1),
       ('Model S', 2),
       ('Model X', 2),
       ('Model 3', 2),
       ('Nova', 3);


INSERT INTO production_years(established_on, manufacturer_id)
VALUES ('1916-03-01', 1),
       ('2003-01-01', 2),
       ('1966-05-01', 3);


create table customers
(
    id   integer generated always as identity primary key,
    name varchar(30),
    date date
);

create table photos
(
    id          serial primary key,
    url         varchar(30),
    place       varchar(30),
    customer_id int,

    constraint fk_phtos_customers
        foreign key (customer_id)
            references customers (id)

);

INSERT INTO customers(name, date)
VALUES ('Bella', '2022-03-25'),
       ('Philip', '2022-07-05');


INSERT INTO photos(url, place, customer_id)
VALUES ('bella_1111.com', 'National Theatre', 1),
       ('bella_1112.com', 'Largo', 1),
       ('bella_1113.com', 'The View Restaurant', 1),
       ('philip_1121.com', 'Old Town', 2),
       ('philip_1122.com', 'Rowing Canal', 2),
       ('philip_1123.com', 'Roman Theater', 2);

create table students
(
    id           integer generated always as identity primary key,
    student_name varchar(50)
);

create table exams
(
    id        integer generated always as identity (start with 101 increment by 1) primary key,
    exam_name varchar(50)
);

create table study_halls
(
    id              integer generated always as identity primary key,
    study_hall_name varchar(50),
    exam_id         int,
    constraint fk_halls_exams
        foreign key (exam_id)
            references exams (id)
);

create table students_exams
(
    student_id int,
    exam_id    int,

    constraint fk_studentex_students
        foreign key (student_id)
            references students (id),
    constraint fk_studentex_exams
        foreign key (exam_id)
            references exams (id)
);

INSERT INTO students(student_name)
VALUES ('Mila'),
       ('Toni'),
       ('Ron');


INSERT INTO exams(exam_name)
VALUES ('Python Advanced'),
       ('Python OOP'),
       ('PostgreSQL');


INSERT INTO study_halls(study_hall_name, exam_id)
VALUES ('Open Source Hall', 102),
       ('Inspiration Hall', 101),
       ('Creative Hall', 103),
       ('Masterclass Hall', 103),
       ('Information Security Hall', 103);


INSERT INTO students_exams(student_id, exam_id)
VALUES (1, 101),
       (1, 102),
       (2, 101),
       (3, 103),
       (2, 102),
       (2, 103);


CREATE TABLE item_types
(
    id             SERIAL PRIMARY KEY,
    item_type_name VARCHAR(50)
);


CREATE TABLE items
(
    id           SERIAL PRIMARY KEY,
    item_name    VARCHAR(50),
    item_type_id INT,

    CONSTRAINT fk_items_item_types
        FOREIGN KEY (item_type_id)
            REFERENCES item_types (id)
);


CREATE TABLE cities
(
    id        SERIAL PRIMARY KEY,
    city_name VARCHAR(50)
);


CREATE TABLE customers
(
    id            SERIAL PRIMARY KEY,
    customer_name VARCHAR(50),
    birthday      DATE,
    city_id       INT,

    CONSTRAINT fk_customers_cities
        FOREIGN KEY (city_id)
            REFERENCES cities (id)
);


CREATE TABLE orders
(
    id          SERIAL PRIMARY KEY,
    customer_id INT,

    CONSTRAINT fk_orders_customers
        FOREIGN KEY (customer_id)
            REFERENCES customers (id)
);


CREATE TABLE order_items
(
    order_id INT,
    item_id  INT,

    CONSTRAINT fk_order_items_orders
        FOREIGN KEY (order_id)
            REFERENCES orders (id),

    CONSTRAINT fk_order_items_items
        FOREIGN KEY (item_id)
            REFERENCES items (id)
);

alter table countries
    add constraint pk_contries_continents
        foreign key(continent_code)
            references continents(continent_code)
            on delete cascade ,
    add constraint pk_countries_cur
        foreign key(currency_code)
            references currencies(currency_code)
            on delete cascade ;

alter table countries_rivers
    add constraint pk_contriv_contries
        foreign key(country_code)
            references countries(country_code)
            on update cascade ,
    add constraint pk_countries_rivers
        foreign key(river_id)
            references rivers(id)
            on update cascade ;


create table customers(
    id serial primary key ,
    customer_name varchar(100)
);
create table contacts(
    id           serial primary key,
    contact_name varchar(100),
    phone        varchar(100),
    email        varchar(50),
    customer_id  int,
    constraint fk_contacts_customers
        foreign key(customer_id)
            references customers(id)
            on delete set null
            on update cascade
);

insert into customers(customer_name)
values ('BlueBird Inc'),
       ('Dolphin LLC');

insert into contacts(contact_name, phone, email, customer_id)
values ('John Doe',	'(408)-111-1234','john.doe@bluebird.dev',1),
       ('Jane Doe','(408)-111-1235','jane.doe@bluebird.dev',1),
       ('David Wright','(408)-222-1234','david.wright@dolphin.dev',2);

DELETE
FROM customers
WHERE id = 1;