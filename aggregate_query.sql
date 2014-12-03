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

create table amins_prices as
(
select sum(a.avg_price*a.count)/sum(a.count) as overall_avg_price, 
sum(a.count) as total_observations,
a.event_id, a.days_out, a.away_team, a.home_team, "Low" as "section_lmh" 
from aggregated_prices_nov21 a
where home_team = "Chicago Bulls" and section_number between 1 and 101
group by event_id, days_out
);

insert into amins_prices
(
select sum(a.avg_price*a.count)/sum(a.count) as overall_avg_price, 
sum(a.count) as total_observations,
a.event_id, a.days_out, a.away_team, a.home_team, "Med" as "section_lmh" 
from aggregated_prices_nov21 a
where home_team = "Chicago Bulls" and section_number between 101 and 202
group by event_id, days_out
);

insert into amins_prices
(
select sum(a.avg_price*a.count)/sum(a.count) as overall_avg_price, 
sum(a.count) as total_observations,
a.event_id, a.days_out, a.away_team, a.home_team, "High" as "section_lmh" 
from aggregated_prices_nov21 a
where home_team = "Toronto Raptors" and section_number between 101 and 122
group by event_id, days_out
);

insert into amins_prices
(
select sum(a.avg_price*a.count)/sum(a.count) as overall_avg_price, 
sum(a.count) as total_observations,
a.event_id, a.days_out, a.away_team, a.home_team, "High" as "section_lmh" 
from aggregated_prices_nov21 a
where home_team = "Utah Jazz" and section_number in (6,7,8)
group by event_id, days_out
);