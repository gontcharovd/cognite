**Data**

Data is obtained from [Cognite Open Industrial Data](https://openindustrialdata.com/about/).
It originates from the first-stage compressor on Aker BP’s Valhall oil platform in the North Sea.
The app allows to visualize one-minute pressure readings of seven sensors situated around the compressor.

**Features**

* select a date range up to 60 days ago
* select two sensors
* inspect the pressure difference
* the flowsheet highlights the sensor location

<br>

**Technology**

This application is developed in R and Shiny and is deployed on a virtual machine on Google Cloud.
The data is queried from a PostgreSQL database. Every day at midnight, new pressure readings are
written to the database through a data pipeline built with Apache Airflow. 

***

Distributed under the MIT License <br>
Copyright (c) 2020 [Denis Gontcharov](https://gontcharov.be)
