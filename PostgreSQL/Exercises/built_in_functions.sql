create view view_river_info
as
  SELECT
  concat('The river', ' ', river_name, ' ', 'flows into the', ' ', outflow, ' ', 'and is', ' ', length, ' ',
              'kilometers long.')
  AS "River Information"
FROM rivers
ORDER BY river_name;

create view view_continents_countries_currencies_details
as
SELECT concat(cont.continent_name, ': ', cont.continent_code) AS continent_details,
       concat_ws(' - ', c.country_name, c.capital, c.area_in_sq_km,'km2')  AS "country_information",
       concat(curr.description,' ', '(', curr.currency_code,')') AS currencies
FROM continents as cont,
     countries as c,
     currencies as curr
WHERE c.continent_code = cont.continent_code and c.currency_code = curr.currency_code
ORDER BY "country_information", currencies;

alter table countries
add column capital_code text;
update countries
set capital_code = substring(capital,1,2);


select substring(description, 5)
from currencies;

select (regexp_match("River Information",'[0-9]{1,4}'))[1] as river_length
from view_river_info;

select replace(mountain_range, 'a', '@') as replace_a,
       replace(mountain_range, 'A','$') as replace_A
from mountains;

select capital,
       translate(capital, 'áãåçéíñóú','aaaceinou') as translated_name
from countries;


select continent_name,
    trim(continent_name) as trim
from continents;

select continent_name,
    trim( trailing from continent_name) as trim
from continents;

select
    ltrim(peak_name, 'M') AS "left_trim",
    rtrim(peak_name,'m') as "right_trim"
from peaks;


select
    concat(m.mountain_range, ' ', peak_name) as mountain_information,
    char_length(concat(m.mountain_range, ' ', peak_name)) as characters_length,
    bit_length(concat(m.mountain_range, ' ', peak_name)) as bits_of_a_tring

from mountains as m, peaks as p
where p.mountain_id = m.id;

select
    population,
length(CAST(population as varchar))
from countries;


select
peak_name,
left(peak_name, 4) as positive_left,
left(peak_name, -4) as negative_left
from peaks;





