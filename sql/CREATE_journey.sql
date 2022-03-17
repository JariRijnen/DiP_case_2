CREATE TYPE direction AS ENUM ('return', 'outward');
CREATE TYPE preference AS ENUM ('cheapest', 'fastest');

CREATE TABLE IF NOT EXISTS journey
(
	journey_id			SERIAL PRIMARY KEY,
	employee_id			smallint REFERENCES employee(employee_id),
	criteria	 		preference NOT NULL,
	direction			direction NOT NULL,
	number_of_flights	smallint NOT NULL,
	duration 			interval NOT NULL,
	price				float,
	departure_time  	timestamp NOT NULL,
	arrival_time		timestamp NOT NULL,
	insert_date 		timestamp NOT NULL,
	CONSTRAINT unique_journey UNIQUE (employee_id, criteria, direction,
										 departure_time, arrival_time)
);
