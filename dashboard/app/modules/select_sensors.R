# Shiny module that outputs sensor selection UI and selected sensors.

# Select a number of sensors by name.
#
# Args:
#   id (character): used to specify the Shiny module namespace
#   config (list): config.json file data
# Returns:
#   Shiny selectizeInput
sensor_select_ui <- function(id, config) {
  ns <- shiny::NS(id)
  query_sensors <- "
    SELECT DISTINCT
      sensor_name
    FROM
      compressor_pressure
    ORDER BY
      sensor_name;
    "
  # execute_query sourced from functions.R
  sensor_choices <- execute_query(query_sensors)$sensor_name
  picker_input <- shinyWidgets::pickerInput(
      ns("selectize"),
      label = h4(config$sensors$label),
      # hard-coded variables below should not be changed
      # max one sensor for each of two groups to calculate
      # a valid pressure diff
      choices = list( Choice = sensor_choices),
      multiple = TRUE,
      options =  list("max-options-group" = 2)
  )
  return(picker_input)
}

# Shiny module server function for date selection.
#
# Args:
#   input: sensors returned by `sensor_select_ui`
#   output: not used
#   session: not used
# Returns:
#   (character): vector of two dates
get_sensors <- function(input, output, session) {
  selected_sensors <- reactive({
    input$selectize
  })
  return(selected_sensors)
}
