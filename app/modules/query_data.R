library(shiny)

APP_DIR <- '/home/gontcharovd/code/personal_projects/cognite/app'
source(file.path(APP_DIR, "functions.R"))

#' Shiny module server function that queries and returns sensor data.
#' @param input not used
#' @param output not used
#' @param session not used
#' @return the selected dates
get_sensor_data <- function(input, output, session, dates, sensors) {
  sensor_data <- reactive({
    sensor_data <- NULL
    if (length(sensors()) > 0) {
      query_data  <- paste0("
        SELECT 
          timestamp
          , asset_id
          , sensor_name
          , pressure
        FROM
          compressor_pressure
        WHERE
          sensor_name IN (", add_quotes(sensors()), ") AND
          timestamp BETWEEN ", add_quotes(dates()[1]), " AND ",
          add_quotes(dates()[2]), ";
        "
      )
      sensor_data <- execute_query(query_data)
      data.table::setDT(sensor_data)
    }
    sensor_data
  })
  return(sensor_data)
}


