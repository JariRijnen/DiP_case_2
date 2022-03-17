CREATE TABLE IF NOT EXISTS city
(
	city_id					smallint PRIMARY KEY,
	city_name				varchar(45),
	country_code			varchar(2) REFERENCES country(country_code)
);
