use stubhub;

create table aggregated_prices_dec02 as
(
select round(avg(t.price),2) as avg_price, round(std(t.price),2) as price_stdev, min(t.price) as min_price, max(t.price) as max_price, convert(substring_index(t.section,' ',-1),unsigned) as section_number, t.event_id, datediff(e.date, t.query_time) as days_out, count(price) as count, e.away_team as away_team, e.home_team as home_team
from available_tickets_new t 
join events e 
on e.event_id = t.event_id 
group by t.event_id, convert(substring_index(t.section,' ',-1),unsigned), datediff(e.date, t.query_time)
);