# Monitoring sensor data

Designing an automated data processing and visualization workflow

![](https://akerbp.com/wp-content/uploads/2016/09/1455710061745.jpg)

## Objective

Cognite AS, a Norwegian software company, recently launched the [Open Industrial Data Project](https://openindustrialdata.com/about/).
It composes a live stream of real industrial data from Aker BP's Valhall oil platform in the North Sea.
The data comes from the first stage compressor and consists of:

* timeseries
* maintenance history
* process and instrumentation diagrams

The first stage compressor (23-KA-9101) is an electrically-driven, fixed-speed centrifugal compressor which receives gas from the separators at approximately 3 barg pressure.
The gas is compressed to approximately 12 barg and flows through a pair of discharge coolers (23-HA-9114/9115) before entering the second stage of compression.

> "What is the typical difference between the input and output pressure of the compressor?"

The objective is to calculate and visualize the pressure difference across the compressor at any point in time within the last 90 days.
Pressure measurements from seven sensors installed around the compressor is available at a one-minute frequency.
Every day new data is loaded and old date is deleted.

## Solution

An application was developed that allows to calculate and visualize the pressure difference between any two sensors.
In addition, the location of selected sensors is highlighted in a flowchart.

This exercise serves to demonstrate how a reliable data processing architecture based on microservices can be built using open-source technology.

## How to use the app

The application is hosted on [Google Cloud Platform](https://cloud.google.com/) and the complete code is published on [GitHub](https://github.com/gontcharovd/cognite).
Give the app a try by navigatying to the address `35.195.26.178:3838` with your web browser.

## Architecture

The data is made available through the [Cognite Python SDK](https://cognite-docs.readthedocs-hosted.com/projects/cognite-sdk-python/en/latest/). 
The architecture is composed of three components: the data pipeline, database and the dashboard.

All components are hosted on an E2-Medium VM instance on Google Cloud Platform.
The data pipeline and dashboard are deployed as separate microservices in two Docker containers. 
The database runs directly on the virtual machine.

### Data pipeline

The data pipeline is defined as a Directed Acyclic Graph or DAG defined in [Apache Airflow](https://airflow.apache.org/) and is executed daily at midnight UTC.
The graph consists of four consecutive steps:

1. A new batch of daily data is queried through the Cognite Python SDK
2. The data is written to a PostgreSQL database
3. Data older than 90 days is deleted
4. Disk space occupied by the deleted data is released

### Database

The [PostgreSQL](https://www.postgresql.org/) relational database serves the dashboard with up to 90 days of sensor data.
Data is stored in [tidy (long) format](https://vita.had.co.nz/papers/tidy-data.pdf) in a single table with a composite primary key:


```sql
CREATE TABLE compressor_pressure (
  timestamp TIMESTAMPTZ NOT NULL,
  asset_id BIGINT NOT NULL,
  sensor_name VARCHAR (25) NOT NULL,
  pressure REAL,
  PRIMARY KEY (timestamp, asset_id)
);
```

### Dashboard

The dashboard consists of a [Shiny Dashboard](https://rstudio.github.io/shinydashboard/) served by four [Shiny modules](https://shiny.rstudio.com/articles/modules.html).
A JSON file allows to configure the entire app.

```json
{
  "dashboard": {
    "theme": "flat_red",
    "title": "Pressure dashboard"
  },
  "columns": {
    "left": {
      "width": 9
    },
    "right": {
      "width": 3
    }
  },
  "dropdown": {
    "info": {
      "icon": "info",
      "circle": "FALSE",
      "size": "lg",
      "label": "About",
      "width": "20vmax",
      "right": "TRUE"
   },
```
Care was taken to design the dashboard to support a wide range of screen sizes.

## Documentation

[Full documentation.](https://github.com/gontcharovd/cognite/wiki)

## License

Distributed under the MIT License <br>
Copyright (c) 2020 [Denis Gontcharov](https://gontcharov.dev)

---
