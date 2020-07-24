library(shiny)
library(shinydashboard)

APP_DIR <- '/home/gontcharovd/code/personal_projects/cognite/app'

source(file.path(APP_DIR, "functions.R"))
source(file.path(APP_DIR, "modules", "date_selection.R"))
source(file.path(APP_DIR, "modules", "sensor_selection.R"))
source(file.path(APP_DIR, "modules", "query_data.R"))

ui <- dashboardPage(
  dashboardHeader(),
  dashboardSidebar(
    date_range_ui("date_selection"),
    sensor_select_ui("sensor_selection")
  ),
  dashboardBody(
    box(tableOutput('sensor_data')),
    box(textOutput('text'))
  )
)

server <- function(input, output) {
  dates <- callModule(get_dates, "date_selection")
  output$text <- renderText(dates())
  sensors <- callModule(get_sensors, "sensor_selection")
  output$sensors <- renderText(sensors())
  sensor_data <- callModule(
    get_sensor_data,
    "query_data",
    dates = dates,
    sensors = sensors
  )
  output$sensor_data <- renderTable(head(sensor_data(), 30))
}

shinyApp(ui, server)
