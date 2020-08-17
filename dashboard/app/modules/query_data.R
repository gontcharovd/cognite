# Shiny module that queries the PostgreSQL database.

# Shiny module server function that queries and returns sensor data.
#
# Args:
#   input: not used
#   output: not used
#   session: not used
#   dates (character, reactive): vector of date strings
#   sensors (character, reactive): vector of sensor names
# Returns:
#   (data.table): the queried sensor data
get_sensor_data <- function(input, output, session, dates, sensors) {
  sensor_data <- reactive({
    sensor_data <- NULL
    if (length(sensors()) > 0 & dates()[1] <= dates()[2]) {
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
          add_quotes(paste(dates()[2], "23:59:59")), ";
        "
      )
      # execute_query sourced from functions.R
      sensor_data <- execute_query(query_data)
      data.table::setDT(sensor_data)
    }
    sensor_data
  })
  return(sensor_data)
}
