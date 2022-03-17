CREATE TYPE risk_level AS ENUM ('Unknown', 'Low', 'Medium', 'High', 'Extreme');

CREATE TABLE IF NOT EXISTS covid_info
(
	country_code			varchar(2) REFERENCES country(country_code),
	fully_vaccinated		float,
	test_required			varchar(3),
	vaccination_required	varchar(3),
	risk_level				risk_level,
	insert_date		 		timestamp NOT NULL,
	UNIQUE (country_code, fully_vaccinated, test_required, vaccination_required, risk_level)
);
