# This test ensures that the timestamp timezone corresponds to UTC
# in the PostgreSQL databse as well as the R Shiny app

library(testthat)

APP_DIR <- '/home/gontcharovd/code/personal_projects/cognite/app'

source(file.path(APP_DIR, "functions.R"))

print("sup")

# context("timezone")
# test_that(
#   "Get 1m pressure values for sensor 23-PT-92532 between
#   '2020-07-12 14:00:00 UTC' and '2020-07-12 14:10:00 UTC' from two sources:
#   1) from Cognite Python SDK
#   2) from the PostgreSQL database
#   Test that the pressure of the same timestamp are equal in both sources
#    ", {
#   data_cognite_sdk <- read.csv("app/test/data.csv", sep = ",", dec = ".")
  
  query_test  <- "
    SELECT
      timestamp
      , pressure
    FROM
      compressor_pressure
    WHERE
      sensor_name = '23-PT-92532' AND
      timestamp BETWEEN '2020-07-12 10:00:00' AND '2020-07-12 19:10:00';
  "
  data_postgresql  <- execute_query(query_test)
  print(data_postgresql)

#   execute_query("SHOW TIMEZONE;")

  
      # timestamp BETWEEN timezone('UTC', '2020-07-12 12:00:00') AND 
      # timezone('UTC', '2020-07-12 12:10:00');
