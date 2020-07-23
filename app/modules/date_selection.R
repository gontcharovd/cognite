library(shiny)

APP_DIR <- '/home/gontcharovd/code/personal_projects/cognite/app'
QUERY_MIN <- "SELECT MIN(timestamp) FROM compressor_pressure;"
QUERY_MAX <- "SELECT MAX(timestamp) FROM compressor_pressure;"

source(file.path(APP_DIR, "functions.R"))

#' Return a date range selector that find the database min and max date.
#' @param id (character) used to specify the Shiny module namespace
#' @return Shiny dateRangeInput
date_range_ui <- function(id) {
  ns <- NS(id)
  date_min <- as.Date(execute_query(QUERY_MIN)$min)
  date_max <- as.Date(execute_query(QUERY_MAX)$max)
  return(
    dateRangeInput(
      ns("date_range"),
      label = h4("Date"),
      separator = "from",
      language = "en",
      weekstart = 1,
      start = date_min,
      end = date_max,
      min = date_min,
      max = date_max
    )
  )
}

#' Shiny module server function for date selection.
#' @param input not used
#' @param output not used
#' @param session not used
#' @return the selected dates
get_dates <- function(input, output, session) {
  date_range <- reactive({input$date_range})
  return(date_range)
}

