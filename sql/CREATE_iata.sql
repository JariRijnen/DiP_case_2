CREATE TABLE IF NOT EXISTS iata
(
	iata_code		varchar(3) PRIMARY KEY,
	city_id			smallint REFERENCES city(city_id)
);
