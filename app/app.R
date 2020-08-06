# Shiny dashboard app
# This file sources `functions.R` and 5 Shiny modules

app_dir <- file.path(
  "/",
  "home",
  "gontcharovd",
  "code",
  "personal_projects",
  "cognite",
  "app"
)

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
  shinydashboard::dashboardHeader(),
  shinydashboard::dashboardSidebar(
    date_range_ui("date_selection", config = config),
    sensor_select_ui("sensor_selection", config = config)
  ),
  shinydashboard::dashboardBody(
    shiny::column(
      shinydashboard::box(
        dygraphs::dygraphOutput("pressure_dygraph"),
        title = config$dygraph$box$title,
        footer = config$dygraph$box$footer,
        height = config$dygraph$box$height,
        width = config$dygraph$box$width
      ),
      shinydashboard::box(
        shiny::textOutput("dygraph_legend"),
        title = config$legend$box$title,
        height = config$legend$box$height,
        width = config$legend$box$width
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
      width = config$columns$right$width
    )
  ), skin = config$dashboard$skin
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
    config = config
  )
  output$flowsheet <- shiny::renderImage({
    flowsheet_list()}, deleteFile = TRUE
  )
}

shiny::shinyApp(ui, server)
