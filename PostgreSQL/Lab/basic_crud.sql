select id, first_name ||' '|| last_name as "Full Name", job_title from employees;

select id, first_name ||' '|| last_name as "Full Name", job_title, salary from employees WHERE SALARY > 1000 ;

select id, first_name, last_name, job_title, department_id, salary
from employees WHERE salary >= 1000 and department_id = 4;

insert into employees(first_name, last_name, job_title, department_id, salary)
values ('Samantha', 'Young', 'Housekeeping', 4, 900),
       ('Roger', 'Palmer', 'Waiter', 3, 928.33);
select * from employees;

update employees set salary = salary + 100 where job_title = 'Manager';
select * from employees where job_title = 'Manager';


delete from employees where department_id = 2 or department_id= 1;
select * from employees;



CREATE VIEW top_paid_employee AS
SELECT id, first_name, last_name, job_title, department_id, salary
FROM employees
WHERE salary = (SELECT max(salary) FROM employees);
SELECT * FROM top_paid_employee;



