select title from books
where substring(title, 1, 3) = 'The'
order by id;

select replace(title, 'The', '***') as title
from books
where substring(title, 1, 3) = 'The'
order by id;

select id, (side * height)/2 as area from triangles
order by id;

select
    title,
    trunc(cost, 3) as modified_price
from books
order by id;

select first_name,
       last_name,
       extract(year from born) as year
from authors;

select
       last_name as "Last Name",
       to_char(born, 'DD (Dy) Mon YYYY') as "Date of Birth"
from authors;

select
       title
from books
WHERE title like '%Harry Potter%'
order by id;

update countries
set iso_code = upper(left(country_name,3))
where iso_code is null;


update countries
set country_code = lower(reverse(country_code))
returning *;


select
    concat(elevation, ' ', repeat('-',3), repeat('>',2), ' ',peak_name)
from peaks
where elevation >= 4884;


create table bookings_calculation
as select booked_for
       from bookings
where apartment_id = 93;

alter table bookings_calculation
add column multiplication NUMERIC,
ADD COLUMN modulo NUMERIC;

update bookings_calculation
set multiplication = booked_for * 50,
    modulo = booked_for % 50;