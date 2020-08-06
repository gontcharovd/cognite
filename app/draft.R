config <- list(dygraph = list(title = "my box title"))

print(config)

ui <- shinydashboard::dashboardPage(
  shinydashboard::dashboardHeader(),
  shinydashboard::dashboardSidebar(),
  shinydashboard::dashboardBody(
    shinydashboard::box(title = config$dygraph$title)
  )
)


server <- function(input, output) {
  # do something
}

shiny::shinyApp(ui, server)
