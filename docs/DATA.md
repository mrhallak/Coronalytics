# Data

## Data Source
The data fetched is from Johns Hopkins University's (JHU) [COVID-19 github repository][1].


## Database Schema
For the table containing the records in PostgreSQL, I've designed this schema for the data:

```sql
create table daily_reports
(
	province varchar,
	country varchar,
	last_update timestamp,
	confirmed int,
	deaths int,
	recovered int,
	latitude decimal(8,6),
	longitude decimal(9,6)
);
```

The choice of the underlying data types for the longitude and latitude columns are based upon this [Stack Overflow question][2].

[1]: https://github.com/CSSEGISandData/COVID-19
[2]: https://stackoverflow.com/questions/1196415/what-datatype-to-use-when-storing-latitude-and-longitude-data-in-sql-databases