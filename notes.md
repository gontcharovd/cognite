## Compressor pressure visualization

Get data from 7 PT-sensors.
Query data for all 7 sensors.
Write to postgres database.
Visualize sensor data with R Shiny.


## Project Readme

Write how your design choices guaranteed DAG atomicity and idempotency

# TO DO
Check if the timezone in the DB is UTC: yes
Check if DAG should have start_date as Date instead of datetime: yes
Check that retrieving a UTC date from the database yields the same
value as the cognite client value of the same timestamp

## Dealing with timezones

Components:
1. Cognite SDK
2. PostgreSQL database
3. R session
4. Dygraph plot

Flow:

1. specify START and END as datetime() as UTC
2. obtain pd.DataFrame whose timestamp column is in UTC
3. write down this value in the SQL query
4. SET TIMEZONE='UTC'; to force PostgreSQL to assume this value as UTC
5. when querying data into R session specify UTC in query timezone('UTC', ...)
6. Check that the values loaded in the R session are correct after converting timezone to UTC


Can I assume that all times returned by the Cognite Python SDK are expressed
in the UTC timezone. 
because selecting:


```python
START = datetime(2020, 7, 12, 12, 0, 0, 0) 
END = datetime(2020, 7, 12, 12, 10, 0, 0) 
```
yields

Here the timestamp is in UTC
```
          timestamp  23-PT-92532
2020-07-12 12:00:00     2.573113
2020-07-12 12:01:00     2.602594
2020-07-12 12:02:00     2.541911
2020-07-12 12:03:00     2.489214
2020-07-12 12:04:00     2.467810
2020-07-12 12:05:00     2.460898
2020-07-12 12:06:00     2.446414
2020-07-12 12:07:00     2.484374
2020-07-12 12:08:00     2.464446
2020-07-12 12:09:00     2.499134
```
To get the same values from the Cognite Date Explorer I have to use the times
2020-07-12 14:00 and 2020-07-12 14:10 with granularity 1m

Here the timestamp is in CEST
```
timestamp,pi:160700
2020-07-12_14:00:00,2.5731125457820245
2020-07-12_14:01:00,2.6025941618066204
2020-07-12_14:02:00,2.5419112531498076
2020-07-12_14:03:00,2.489213689661579
2020-07-12_14:04:00,2.4678099095661086
2020-07-12_14:05:00,2.4608976917283067
2020-07-12_14:06:00,2.4464138049376634
2020-07-12_14:07:00,2.4843738435172504
2020-07-12_14:08:00,2.4644460236328425
2020-07-12_14:09:00,2.4991342074328324
2020-07-12_14:10:00,2.4626214533788198
```

It seems that the Cognite Data Explorer expects a timestamp with respect to 
the local time zone.
(CEST in my case, which is 2 hours ahead of UTC)



## R Shiny app components

* Select pressure curves dygraphs similar to TAV-HTS project
* Picture that highlights the selected sensors in color
* bar chart uptime of the compressor within selected dygraph interval
* relevant Apache Airflow logs and number of datapoints in the databas



## Airflow

postgres db fails on NaN pressure values
Check out why Airflow logging bumps into permission errors:
https://stackoverflow.com/questions/59412917/errno-13-permission-denied-when-airflow-tries-to-write-to-logs

## tests on data

Check if there are points that fall within `n` standard deviations of the mean. Check if values are repeated more than `n` times. Check if there are any NA values. 
