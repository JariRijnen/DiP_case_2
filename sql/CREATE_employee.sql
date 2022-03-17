CREATE TABLE IF NOT EXISTS employee
(
	employee_id 			SERIAL PRIMARY KEY,
	first_name				varchar(45),
	last_name				varchar(45),
	iata_code				varchar(3) REFERENCES iata(iata_code)
);
