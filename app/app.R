library(shiny)
library(shinydashboard)

APP_DIR <- '/home/gontcharovd/code/personal_projects/cognite/app'

source(file.path(APP_DIR, "functions.R"))
source(file.path(APP_DIR, "modules", "date_selection.R"))
source(file.path(APP_DIR, "modules", "sensor_selection.R"))
source(file.path(APP_DIR, "modules", "query_data.R"))
source(file.path(APP_DIR, "modules", "create_dygraph.R"))

ui <- dashboardPage(
  dashboardHeader(),
  dashboardSidebar(
    date_range_ui("date_selection"),
    sensor_select_ui("sensor_selection")
  ),
  dashboardBody(
    fluidRow(
      box(HTML('&nbsp;') , dygraphOutput('pressure_dygraph'), width = NULL, solidHeader = TRUE),
    ),
    fluidRow(
      box(title = "Legend", textOutput("dygraph_legend"), width = 4),
      box(textOutput('dates')),
      box(textOutput('sensors'))
    )
  )
)

server <- function(input, output) {
  config <- jsonlite::rea
  dates <- callModule(get_dates, "date_selection")
  output$dates <- renderText(dates())
  sensors <- callModule(get_sensors, "sensor_selection")
  output$sensors <- renderText(sensors())
  sensor_data <- callModule(
    get_sensor_data,
    "query_data",
    dates = dates,
    sensors = sensors
  )
  pressure_dygraph <- callModule(
    get_pressure_dygraph,
    "pressure_dygraph",
    sensor_data = sensor_data
  )
  output$pressure_dygraph <- renderDygraph(pressure_dygraph())
}

shinyApp(ui, server)
