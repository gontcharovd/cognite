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
    title = config$dashboard$title,
    tags$li(
    shinyWidgets::dropdownButton(
        shiny::includeMarkdown("input/app_text.md"),
        icon = icon("info"),
        circle = FALSE,
        size = "lg",
        label = "About",
        width = "20vmax",
        right = TRUE
      ),
      class= "dropdown"
    )
  ),
  shinydashboard::dashboardSidebar(disable = TRUE),
  shinydashboard::dashboardBody(
    dashboardthemes::shinyDashboardThemes(theme = config$dashboard$theme),
    shiny::column(
      shinydashboard::box(
        shinyWidgets::dropdownButton(
          date_range_ui("date_selection", config = config),
          circle = FALSE,
          size = "lg",
          label = "Date range",
          icon = icon("calendar")
        ),
      tags$br(),
        dygraphs::dygraphOutput(
          "pressure_dygraph",
          height = config$dygraph$height,
          width = config$dygraph$width
        ),
        height = config$dygraph$box$height,
        width = config$dygraph$box$width
      ),
      width = config$columns$left$width
    ),
    shiny::column(
      shinydashboard::box(
        div(
          shiny::imageOutput("flowsheet", height = "100%", width = "100%"),
          style = "height: 48vmin; width: 48vmin;"
        ),
        sensor_select_ui("sensor_selection", config = config),
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
