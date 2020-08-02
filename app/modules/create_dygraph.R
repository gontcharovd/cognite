library(shiny)
library(xts)
library(dygraphs)
library(magrittr)

#' Shiny module server function that:
#' 1. creates a selectizeInput input to select variables to plot
#' 2. renders dygraphs for the selected variables
#'
#' @param input selected_vars (reactive)
#' @param output rendered_dygraphs (reactive), var_selection (reactive)
#' @param session environment containing the session's namespace
#' @param config a data.table containing dygraph configuration (non-reactive)
#' @param data a data.table with data for dygraphs (reactive)
#'
#' @return nothing
get_pressure_dygraph <- function(input, output, session, sensor_data, config) {
  pressure_dygraph  <- reactive({
    if (is.null(sensor_data())) {
        pressure_dygraph <- NULL
      } else {
      data_wide <- data.table::dcast(
        sensor_data(),
        timestamp ~ sensor_name,
        value.var = "pressure"
      )
      data_wide[, pressure_delta := ifelse(
          ncol(data_wide) == 2, 0, abs(data_wide[, 2] - data_wide[, 3])
        )
      ]
      time_series <- xts::xts(
        x = data_wide[, -"timestamp"],
        order.by = data_wide[, timestamp],
        tzone = "UTC"
      )
      pressure_dygraph <- create_dygraph(time_series, config)
    }
  })
  return(pressure_dygraph)
}

#' helper function that creates a dygraph using config data
#'
#' @param datetime the x-axis POSIXct variable for the dygraph
#' @param x the y-axis variable of the dygraph
#' @param config configuration read from the csv file for the plotted variable
#'
#' @return a dygraph object
create_dygraph <- function(time_series, config) {
  graph <- dygraph(time_series, main = NULL) %>%
    configure_dyseries(time_series, config) %>%
    dyRangeSelector(retainDateWindow = TRUE) %>%
    dyCrosshair(direction = "both") %>%
    dyLegend(
      labelsDiv = "dygraph_legend",
      labelsSeparateLines = TRUE,
      hideOnMouseOut = FALSE
    ) %>%
    dyRoller(rollPeriod = 1) %>%
    dyOptions(
      axisLineWidth = 1.5,
      # useDataTimezone = TRUE,
      fillGraph = FALSE,
      fillAlpha = 0.1,
      drawGrid = TRUE,
      rightGap = 40
    ) %>%
    dyAxis("y", label = "pressure [barg]")
  return(graph)
}


configure_dyseries <- function(dygraph, time_series, config) {
  for (sensor in setdiff(names(time_series), "timestamp")) {
    dygraph <- dygraph %>%
      dySeries(
        name = sensor,
        color = eval(
          substitute(
            config$sensors$sensor_name$color,
            list(sensor_name = sensor)
          )
        ),
        label = eval(
          substitute(
            config$sensors$sensor_name$label,
            list(sensor_name = sensor)
          )
        )
      )
  }
  return(dygraph)
}
