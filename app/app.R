app_dir <- file.path(
  "/",
  "home",
  "gontcharovd",
  "code",
  "personal_projects",
  "cognite",
  "app"
)
source_files <- c(
  file.path(app_dir, "functions.R"),
  file.path(app_dir, "modules", "date_selection.R"),
  file.path(app_dir, "modules", "sensor_selection.R"),
  file.path(app_dir, "modules", "query_data.R"),
  file.path(app_dir, "modules", "create_dygraph.R"),
  file.path(app_dir, "modules", "create_flowsheet.R")
)
sapply(source_files, source)

ui <- shinydashboard::dashboardPage(
  shinydashboard::dashboardHeader(),
  shinydashboard::dashboardSidebar(
    date_range_ui("date_selection"),
    sensor_select_ui("sensor_selection")
  ),
  shinydashboard::dashboardBody(
    shiny::column(
      shinydashboard::box(
        shiny::HTML("&nbsp;"),
        dygraphs::dygraphOutput("pressure_dygraph"),
        width = NULL,
        height = 500,
        solidHeader = TRUE
      ),
      shinydashboard::box(
        title = "Legend",
        shiny::textOutput("dygraph_legend")
      ), width = 9
    ),
    shiny::column(
      shinydashboard::box(
        title = "Flowsheet",
        shiny::imageOutput("flowsheet"),
        width = 300,
        height = 500
      ), width = 3
    )
  )
)

server <- function(input, output) {
  config <- jsonlite::read_json(
    file.path(app_dir, "input", "config.json")
  )
  dates <- shiny::callModule(get_dates, "date_selection")
  sensors <- shiny::callModule(get_sensors, "sensor_selection")
  sensor_data <- shiny::callModule(
    get_sensor_data,
    "query_data",
    dates = dates,
    sensors = sensors
  )
  pressure_dygraph <- shiny::callModule(
    get_pressure_dygraph,
    "pressure_dygraph",
    sensor_data = sensor_data,
    config = config
  )
  output$pressure_dygraph <- dygraphs::renderDygraph(pressure_dygraph())
  flowsheet_list <- shiny::callModule(
    get_flowsheet_list,
    "flowsheet",
    sensors = sensors,
    config = config
  )
  output$flowsheet <- renderImage({flowsheet_list()}, deleteFile = TRUE)
}

shiny::shinyApp(ui, server)
