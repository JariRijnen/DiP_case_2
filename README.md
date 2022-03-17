# Project Case 2: Flight Tickets for DiP

### Date created
20-01-2022

### Description
Second case of data engineer traineeship by Jari Rijnen. In this project, flight tickets for DiP employees are searched using the Amadeus API and the results are stored in a PostgreSQL database.

### Input Data Sources used
- input_fil.csv
CSV file containing information about DiP employees: First name, Last name, favourite destination and IATA code.
- [Amadeus API](https://developers.amadeus.com/)
Flight searching API.
### Use
The database is set-up by running first
```
create_tables.py
insert_input_file.py
```

Create_tables.py sets up the PostgreSQL environment and tables, the insert_input_file.py fills the tables that can be filled on beforehand.

Then, by running
```
main.py
```
Flights are searched for for every employee and are saved in the database.

### Queries
The resulting database allows for many different queries and analysis. Examples can be found in [https://github.com/digital-power/DE_case2_Jari/blob/main/query_examples.ipynb](query_examples.ipynb).

### ER-Diagram

![ER-Diagram](https://github.com/digital-power/DE_case2_Jari/blob/main/pictures/ER-diagram.PNG?raw=true)

### Pipeline

![create_tables](https://github.com/digital-power/DE_case2_Jari/blob/main/pictures/create_tables.PNG?raw=true)

![flight-pipeline](https://github.com/digital-power/DE_case2_Jari/blob/main/pictures/flight-pipeline.PNG?raw=true)

### Credits
Thanks to [https://github.com/dennisdickmann-digital-power](https://github.com/dennisdickmann-digital-power), [https://github.com/sandervandorsten](https://github.com/sandervandorsten) and [https://github.com/timmolleman1](https://github.com/timmolleman1).
