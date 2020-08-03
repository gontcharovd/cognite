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
    shiny::fluidRow(
      shinydashboard::box(
        shiny::HTML("&nbsp;"),
        dygraphs::dygraphOutput("pressure_dygraph"),
        width = NULL,
        solidHeader = TRUE
      ),
    ),
    shiny::fluidRow(
      shinydashboard::box(
        title = "Legend",
        shiny::textOutput("dygraph_legend"), width = 4
      ),
      shinydashboard::box(
        title = "Flowsheet",
        shiny::imageOutput("flowsheet")
      )
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
  output$flowsheet <- renderImage({flowsheet_list}, deleteFile = FALSE)
}

shiny::shinyApp(ui, server)
