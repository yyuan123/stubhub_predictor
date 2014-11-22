select round(avg(t.price),2) as avg_price, round(std(t.price),2) as price_stdev, min(t.price) as min_price, max(t.price) as max_price, t.section_number, t.event_id, datediff(e.date, t.query_time) as days_out, count(price) as count, e.away_team as away_team, e.home_team as home_team
from test_tickets_2 t 
join test_events e 
on e.event_id = t.event_id 
group by t.event_id, t.section_number, datediff(e.date, t.query_time);

create table aggregated_prices_nov21 as
(
select round(avg(t.price),2) as avg_price, round(std(t.price),2) as price_stdev, min(t.price) as min_price, max(t.price) as max_price, t.section_number, t.event_id, datediff(e.date, t.query_time) as days_out, count(price) as count, e.away_team as away_team, e.home_team as home_team
from available_tickets t 
join events e 
on e.event_id = t.event_id 
group by t.event_id, t.section_number, datediff(e.date, t.query_time)
);

create table aggregated_prices_nov21_section_cat as
(
select round(avg(t.price),2) as avg_price, round(std(t.price),2) as price_stdev, min(t.price) as min_price, max(t.price) as max_price, t.section_category, t.event_id, datediff(e.date, t.query_time) as days_out, count(price) as count, e.away_team as away_team, e.home_team as home_team
from available_tickets t 
join events e 
on e.event_id = t.event_id 
group by t.event_id, t.section_category, datediff(e.date, t.query_time)
);