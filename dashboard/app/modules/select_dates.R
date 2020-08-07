# Shiny module that outputs date selection UI and selected dates.

# Return a date range selector that find the database min and max date.
#
# Args:
#   id (character) used to specify the Shiny module namespace
# Returns:
#   Shiny dateRangeInput
date_range_ui <- function(id, config = config) {
  ns <- shiny::NS(id)
  query_min <- "SELECT MIN(timestamp) FROM compressor_pressure;"
  query_max <- "SELECT MAX(timestamp) FROM compressor_pressure;"
  # execute_query sourced from functions.R
  date_min <- as.Date(execute_query(query_min)$min)
  date_max <- as.Date(execute_query(query_max)$max)
  date_range_input <- shiny::dateRangeInput(
      ns("date_range"),
      label = h4(config$dates$label),
      separator = config$dates$separator,
      language = config$dates$language,
      weekstart = config$dates$weekstart,
      start = date_max - lubridate::days(config$dates$start_offset_days),
      end = date_max,
      min = date_min,
      max = date_max
    )
  return(date_range_input)
}

# Shiny module server function for date selection.
#
# Args
#   input: selected dates from `date_range_ui`
#   output: not used
#   session not used
# Returns:
#   (character) vector of two selected dates
get_dates <- function(input, output, session) {
  date_range <- reactive({
    as.character(input$date_range)
  })
  return(date_range)
}
