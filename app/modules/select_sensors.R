# Shiny module that outputs sensor selection UI and selected sensors.

# Select a number of sensors by name.
#
# Args:
#   id (character): used to specify the Shiny module namespace
# Returns:
#   Shiny selectizeInput
sensor_select_ui <- function(id) {
  ns <- shiny::NS(id)
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
