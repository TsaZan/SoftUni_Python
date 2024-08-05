select count(*)
from wizard_deposits;


select sum(deposit_amount)
from wizard_deposits;

select round(avg(magic_wand_size), 3)
from wizard_deposits;

select min(deposit_charge)
from wizard_deposits;

select max(age)
from wizard_deposits;

select deposit_group, sum(deposit_interest) as deposit_interest
from wizard_deposits
group by deposit_group
order by deposit_interest desc;

select deposit_group, sum(deposit_interest) as deposit_interest
from wizard_deposits
group by deposit_group
order by deposit_interest desc;

select deposit_group, is_deposit_expired, floor(avg(deposit_interest)) as deposit_interest
from wizard_deposits
where deposit_start_date > '1985-01-01'
group by deposit_group, is_deposit_expired
order by deposit_group desc, is_deposit_expired;

select last_name, count(notes) as notes
from wizard_deposits
where notes like '%Dumbledore%'
group by last_name;

create or replace view view_wizard_deposits_with_expiration_date_before_1983_08_17
as
select concat(first_name, ' ', last_name) as wizard_name,
       deposit_start_date                 as start_date,
       deposit_expiration_date            as expiration_date,
       deposit_amount                     as amount
from wizard_deposits
where deposit_expiration_date <= '1983-08-17'
group by wizard_name, start_date, expiration_date, amount
order by expiration_date asc;


select magic_wand_creator, max(deposit_amount) as max_sum
from wizard_deposits
where deposit_amount not between 20000 and 40000
group by magic_wand_creator
order by max_sum desc
limit 3;




select case
when age between 11 and 20 then '[11-20]'
when age between 21 and 30 then '[21-30]'
when age between 31 and 40 then '[31-40]'
when age between 41 and 50 then '[41-50]'
when age between 51 and 60 then '[51-60]'
when age >= 61 then '[61+]'
end as "agegroup",
count(*)
from wizard_deposits
group by agegroup
order by agegroup;

select
    count(case department_id when 1 then 1 end)  as "Engineering",
    count(case department_id when 2 then 1 end)  as "Tool Design",
    count(case department_id when 3 then 1 end)  as "Sales",
    count(case department_id when 4 then 1 end)  as "Marketing",
    count(case department_id when 5 then 1 end)  as "Purchasing",
    count(case department_id when 6 then 1 end)  as "Research and Development",
        count(case department_id when 7 then 1 end)  as "Production "
from employees;


update employees
set salary = CASE
    when hire_date < '2015-01-16' then salary + 2500
     when hire_date < '2020-03-04' then salary + 1500
    else salary
END,
    job_title = CASE
    when hire_date < '2015-01-16' then concat('Senior ', job_title)
    when hire_date < '2020-03-04' then concat('Mid-', job_title)
    ELSE job_title
end;

select job_title, CASE
    when avg(salary) > 45800 then  'Good'
    when avg(salary) between 27500 and 45800 then 'Medium'
    when avg(salary) < 27500 then 'Need Improvement'
END as category
from employees
group by job_title
order by category asc , job_title;


select project_name,
       case
           when start_date is null and end_date is null then 'Ready for development'
           when start_date is not null and end_date is null then 'In Progress'
           else 'Done'
        end

    FROM projects
WHERE project_name LIKE '%Mountain%';

select department_id, count(*),
       case
           when avg(salary) > 50000 then 'Above average'
           when avg(salary) <= 50000 then 'Below average'
    end as salary_level
FROM employees
group by department_id
HAVING avg(salary) > 30000
order by department_id;