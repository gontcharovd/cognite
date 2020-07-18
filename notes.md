## Compressor pressure visualization

Get data from 7 PT-sensors.

Query data for all 7 sensors.

Write to postgres database.
 
Visualize sensor data with R Shiny.

## tests on data

Check if there are points that fall within `n` standard deviations of the mean. Check if values are repeated more than `n` times. Check if there are any NA values. 

DAD may become open source. 


## Project Readme

Write how your design choices guaranteed DAG atomicity and idempotency

# TODO

need to configure an Airflow directory for dags
how to pass secret environment variables?
postgres db fails on NaN pressure values
there is no primary key in the pressure table
currently duplicates can be written in the pressure table

