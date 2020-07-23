library(shiny)
library(shinydashboard)

APP_DIR <- '/home/gontcharovd/code/personal_projects/cognite/app'

source(file.path(APP_DIR, "functions.R"))
source(file.path(APP_DIR, "modules", "date_selection.R"))

ui <- dashboardPage(
  dashboardHeader(),
  dashboardSidebar(
    date_range_ui("date_selection")
  ),
  dashboardBody(
    textOutput('text')
  )
)

server <- function(input, output) {
  dates <- callModule(get_dates, "date_selection")
  output$text <- renderText(dates())
}

shinyApp(ui, server)
