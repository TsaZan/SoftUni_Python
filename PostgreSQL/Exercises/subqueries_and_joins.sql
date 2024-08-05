select concat(a.address,' ',address_2) as apartment_address, b.booked_for as nights
from apartments as a
join bookings as b
on a.booking_id = b.booking_id
order by a.apartment_id;


select a.name, a.country, b.booked_at::date
from apartments as a
left join bookings as b
on a.booking_id = b.booking_id
order by a.apartment_id
limit 10;


select booking_id, starts_at::date, apartment_id, concat(first_name, ' ', last_name) as customer_name
from customers as a
left join bookings as b
on a.customer_id = b.customer_id
order by customer_name
limit 10;


select b.booking_id, a.name as apartment_owner, a.apartment_id, concat(c.first_name, ' ', c.last_name) as customer_name
from bookings as b
    full join apartments as a
        on b.booking_id = a.booking_id
       full join customers as c
        on b.customer_id = c.customer_id
order by booking_id, apartment_owner, customer_name;


select b.booking_id, b.apartment_id, c.companion_full_name
from bookings as b
        join customers as c
       USING(customer_id)
where b.apartment_id is null
order by b.booking_id;


select b.apartment_id, b.booked_for, c.first_name, c.country
from bookings as b
      join customers as c
      on b.customer_id = c.customer_id
where c.job_type like 'Lead%';


select count(booking_id)
from bookings as b
      join customers as c
      on b.customer_id = c.customer_id
where c.last_name like 'Hahn';


select a.name, sum(b.booked_for)
from apartments as a
      join bookings as b
      on a.apartment_id = b.apartment_id
group by a.name
order by a.name;


select
    a.country,
    count(b.booking_id) as booking_count
from apartments as a
      join bookings as b
      on a.apartment_id = b.apartment_id
where b.booked_at > '2021-05-18 07:52:09.904+03' and b.booked_at < '2021-09-17 19:48:02.147+03'
group by a.country
order by booking_count desc;


select country_code, mountain_range, peak_name  , elevation
from mountains as m
join mountains_countries as mc
on m.id = mc.mountain_id
join peaks as p
on m.id = p.mountain_id
where elevation > 2835 and country_code = 'BG'
order by elevation desc;


select country_code, count(mountain_range) as mountain_range_count
from mountains as m
join mountains_countries as mc
on m.id = mc.mountain_id
where country_code =  'US' or country_code =  'RU' or country_code =  'BG'
group by country_code
order by mountain_range_count desc;


select country_name, river_name
from countries as c
full join countries_rivers as cr
on c.country_code = cr.country_code
full join rivers as r
on cr.river_id = r.id
where continent_code = 'AF'
order by country_name
Limit 5;


SELECT MIN(avg_area)
FROM (SELECT AVG(countries.area_in_sq_km) AS "avg_area"
FROM countries
GROUP BY continent_code) AS "min_average_area";


select count(*)
from  mountains_countries
full join countries
on mountains_countries.country_code = countries.country_code
where mountain_id is null;