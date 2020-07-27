library(shiny)

APP_DIR <- '/home/gontcharovd/code/personal_projects/cognite/app'
source(file.path(APP_DIR, "functions.R"))

#' Select a number of sensors by name
#' @param id (character) used to specify the Shiny module namespace
#' @return Shiny selectizeInput
sensor_select_ui <- function(id) {
  ns <- NS(id)
  query_sensors <- "
    SELECT DISTINCT
      sensor_name
    FROM
      compressor_pressure
    ORDER BY
      sensor_name;
    "
  sensor_choices <- execute_query(query_sensors)$sensor_name
  return(
    shinyWidgets::pickerInput(
      ns("selectize"),
      label = h4("Sensors"),
      choices = list(
        First = sensor_choices,
        Second = sensor_choices
      ),
      multiple = TRUE,
      options =  list("max-options-group" = 1)
    )
  )
}

#' Shiny module server function for date selection.
#' @param input not used
#' @param output not used
#' @param session not used
#' @return the selected dates
get_sensors <- function(input, output, session) {
  selected_sensors <- reactive({input$selectize})
  return(selected_sensors)
}

