CREATE TABLE  employees(
    id serial primary key not null ,
    first_name varchar(30),
    last_name varchar(50),
    hiring_date date default '2023-01-01',
    salary numeric(10,2),
    devices_number int
);
CREATE table departments(
    id serial primary key ,
    name varchar(30),
    code char(3),
    description text
);

create table issues(
    id serial primary key unique ,
    description varchar(150),
    date date,
    start timestamp
);


ALTER TABLE employees
    add column middle_name varchar(50);


alter table employees
    alter column salary set not null,
    alter column salary set default 0,
    alter column hiring_date set not null;


alter table employees
    alter column middle_name type varchar(100);

truncate issues;

drop table departments;
