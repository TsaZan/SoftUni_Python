SELECT id,
       name,
       state,
       area
FROM cities;


SELECT concat(name, ' ', state) as cities_information,
       area                     as area_km2
FROM cities;

SELECT distinct name,
                area as area_km2
FROM cities
ORDER BY name DESC;


SELECT id,
       concat(first_name, ' ',
              last_name) as full_name,
       job_title

FROM employees
ORDER BY first_name
LIMIT 50;


SELECT id,
       concat(first_name, ' ', middle_name,
              ' ', last_name) as full_name,
       hire_date

FROM employees
ORDER BY hire_date asc
offset 9;


SELECT id,
       concat(number, ' ', street) as address,
       city_id

FROM addresses
WHERE id >= 20;


SELECT concat(number, ' ', street) as address,
       city_id

FROM addresses
WHERE city_id > 0
  and city_id % 2 = 0
ORDER BY city_id;


SELECT name,
       start_date,
       end_date

FROM projects
WHERE start_date >= '2016-06-01 07:00:00'
  and end_date < '2023-06-04 00:00:00'
ORDER BY start_date;


SELECT number,
       street

FROM addresses
WHERE (id between 50 and 100)
   or number < 1000;


SELECT employee_id,
       project_id
FROM employees_projects
where employee_id in (200, 250)
  and project_id not in (50, 100);


SELECT name,
       start_date
FROM projects
where name in ('Mountain', 'Road', 'Touring')
limit 20;



SELECT concat(first_name, ' ', last_name) as full_name,
       job_title,
       salary
FROM employees
where salary in (12500, 14000, 23600, 25000)
order by salary desc;


SELECT id,
       employees.first_name,
       employees.last_name
from employees
where middle_name is NULL
LIMIT 3;

Insert Into departments(department, manager_id)
values ('Finance', 3),
       ('Information Services', 42),
       ('Document Control', 90),
       ('Quality Assurance', 274),
       ('Facilities and Maintenance', 218),
       ('Shipping and Receiving', 85),
       ('Executive', 109);


create table company_chart as
select concat(employees.first_name, ' ', employees.last_name) as full_name,
       job_title,
       department_id,
       manager_id
from employees;


update projects
set end_date = start_date + Interval '5 months'
WHERE end_date is NULL;


update employees
set salary = salary + 1500, job_title = 'Senior ' || job_title
WHERE hire_date BETWEEN '1998-01-01' and '2000-01-05';


delete from
           addresses
where city_id in (5, 17, 20, 30);


create view
    view_company_chart
as select
       full_name,
       job_title
from
    company_chart
where
    manager_id = 184;


create view
    view_addresses
as select
       concat(e.first_name, ' ', e.last_name) as full_name,
       e.department_id,
       concat(a.number, ' ', a.street) as address
from
employees as e, addresses as a
where
    a.id = e.address_id
order by address;


alter view
    view_addresses
rename to view_employee_addresses_info;

drop view view_company_chart;

update projects
set name = UPPER(name);


create view view_initials
as select substring(first_name,1,2) as initial, last_name
from employees
order by last_name;


select
    name,
    start_date
from
    projects
where name like 'MOUNT%'
order by id;


