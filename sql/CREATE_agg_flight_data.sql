CREATE TABLE IF NOT EXISTS agg_flight_data
(
	employee_id			smallint REFERENCES employee(employee_id),
	criteria            preference,
    avg_price	 		float,
	min_price			float,
	avg_duration    	time,
	min_duration 		time,
	insert_date 		timestamp NOT NULL
);
