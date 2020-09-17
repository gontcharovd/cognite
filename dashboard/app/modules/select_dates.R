# Return a list with the min and max date in the database.
get_min_max_date <- function() {
  query_min <- "SELECT MIN(timestamp) FROM compressor_pressure;"
  query_max <- "SELECT MAX(timestamp) FROM compressor_pressure;"
  date_min <- as.Date(execute_query(query_min)$min)
  date_max <- as.Date(execute_query(query_max)$max)
  dates <- list("min" = date_min, "max" = date_max)
  return(dates)
}

# Shiny module that outputs date selection UI and selected dates.

# Return a date range selector that find the database min and max date.
#
# Args:
#   id (character) used to specify the Shiny module namespace
# Returns:
#   Shiny dateRangeInput
date_range_ui <- function(id, config = config) {
  ns <- shiny::NS(id)
  dates <- get_min_max_date()
  date_min <- dates[["min"]]
  date_max <- dates[["max"]]
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
get_dates <- function(input, output, session, config = config) {
  # update the date range every twelve hours with new data from the database
  update_date_range <- reactiveTimer(1000 * 60 * 60 * 12)
  observe({
    update_date_range()
    dates <- get_min_max_date()
    date_min <- dates[["min"]]
    date_max <- dates[["max"]]
    shiny::updateDateRangeInput(
      session,
      "date_range",
      start = date_max - lubridate::days(config$dates$start_offset_days),
      end = date_max,
      min = date_min,
      max = date_max
    )
  })
  date_range <- reactive({
    as.character(input$date_range)
  })
  return(date_range)
}
