CREATE TABLE IF NOT EXISTS flight
(
	journey_id			int REFERENCES journey(journey_id),
	iata_departure		varchar(3) NOT NULL,
	iata_arrival 		varchar(3) NOT NULL,
	airline_code		varchar(2),
	flight_number   	smallint NOT NULL,
	UNIQUE (journey_id, iata_arrival, iata_departure, airline_code, flight_number)
);
