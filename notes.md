## Compressor pressure visualization

Get data from 7 PT-sensors.
Query data for all 7 sensors.
Write to postgres database.
Visualize sensor data with R Shiny.


## Project Readme

Write how your design choices guaranteed DAG atomicity and idempotency

# TO
Check if the timezone in the DB is UTC


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
