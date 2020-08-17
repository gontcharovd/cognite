# Shiny dashboard app
# This file sources `functions.R` and 5 Shiny modules

app_dir <- Sys.getenv("APP_DIR")

config_path <- file.path(app_dir, "input", "config.json")
config <- jsonlite::read_json(file.path(app_dir, "input", "config.json"))
 
source_files <- c(
  file.path(app_dir, "functions.R"),
  file.path(app_dir, "modules", "select_dates.R"),
  file.path(app_dir, "modules", "select_sensors.R"),
  file.path(app_dir, "modules", "query_data.R"),
  file.path(app_dir, "modules", "create_dygraph.R"),
  file.path(app_dir, "modules", "create_flowsheet.R")
)
sapply(source_files, source)

ui <- shinydashboard::dashboardPage(
  shinydashboard::dashboardHeader(
    title = tags$a(
      href="https://openindustrialdata.com/get-started/",
      tags$img(src = "logo.jpeg", height = 58)
    )
  ),
  shinydashboard::dashboardSidebar(disable=TRUE),
  shinydashboard::dashboardBody(
    dashboardthemes::shinyDashboardThemes(theme = config$dashboard$theme),
    shiny::column(
      shinydashboard::box(
        dygraphs::dygraphOutput(
          "pressure_dygraph",
          height = config$dygraph$height,
          width = config$dygraph$width
        ),
        title = config$dygraph$box$title,
        height = config$dygraph$box$height,
        width = config$dygraph$box$width
      ),
      width = config$columns$left$width
    ),
    shiny::column(
      shinydashboard::box(
        shiny::imageOutput("flowsheet"),
        title = config$flowsheet$box$title,
        height = config$flowsheet$box$height,
        width = config$flowsheet$box$width
      ),
      shinydashboard::box(
        shiny::textOutput("dygraph_legend"),
        title = config$legend$box$title,
        height = config$legend$box$height,
        width = config$legend$box$width
      ),
      shinydashboard::box(
        date_range_ui("date_selection", config = config),
        sensor_select_ui("sensor_selection", config = config),
        height = config$menu$box$height,
        width = config$menu$box$width
      ),
      width = config$columns$right$width
    )
  )
)

# Shiny server function.
#
# Args:
#   input: not used
#   output: passes rendered dygraph, flowsheet and legend to UI
server <- function(input, output) {
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
    config = config,
    app_dir = app_dir
  )
  output$flowsheet <- shiny::renderImage({
    flowsheet_list()}, deleteFile = TRUE
  )
}

shiny::shinyApp(ui, server)
