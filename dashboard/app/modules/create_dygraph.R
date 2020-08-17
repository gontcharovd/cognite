# Shiny module that creates a dygraph from reactive sensor_data.

library(magrittr)

# Shiny module server function that creates a dygraph from sensor data.
#
# Args:
#   input: not used
#   output: not used
#   session: not used
#   sensor_data (data.table, reactive): with data for dygraphs
#   config (list): dygraph configuration
# Returns:
#   (dygraph): graph with curves of selected sensor
get_pressure_dygraph <- function(input, output, session, sensor_data, config) {
  pressure_dygraph  <- shiny::reactive({
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

# Create and configure a dygraph.
#
# Args:
#   time_series (xts): pressure time series
#   config (list): settings froma  json config file
# Returns:
#   (dygraph): the configured dygraph
create_dygraph <- function(time_series, config) {
  graph <- dygraphs::dygraph(
      data = time_series,
      main = config$dygraph$main
    ) %>%
    configure_dyseries(time_series, config) %>%
    dygraphs::dyRangeSelector(
      retainDateWindow = as.logical(config$dygraph$retainDateWindow),
      fillColor = config$dygraph$fillcolor,
      strokeColor = config$dygraph$strokecolor,
      ) %>%
    dygraphs::dyCrosshair(direction = config$dygraph$direction) %>%
    dygraphs::dyLegend(
      width = config$legend$width,
      labelsDiv = "dygraph_legend",
      labelsSeparateLines = as.logical(config$dygraph$labelsSeparateLines),
      hideOnMouseOut = as.logical(config$dygraph$hideOnMouseOut)
    ) %>%
    dygraphs::dyRoller(rollPeriod = config$dygraph$rollPeriod) %>%
    dygraphs::dyOptions(
      axisLineWidth = config$dygraph$axisLineWidth,
      useDataTimezone = as.logical(config$dygraph$useDataTimezone),
      fillGraph = as.logical(config$dygraph$fillGraph),
      fillAlpha = config$dygraph$fillAlpha,
      drawGrid = as.logical(config$dygraph$drawGrid),
      rightGap = config$dygraph$rightGap
    ) %>%
    dygraphs::dyAxis("y", label = config$dygraph$y_label)
  return(graph)
}

# Configure dySeries from a config file.
#
# Args:
#   dygraph (dygraph): parent dygraph
#   time_series (xts): pressure time series
#   config (list): settings from the json config file
# Returns:
#   (dygraph): dygraph with configured dySeries
configure_dyseries <- function(dygraph, time_series, config) {
  for (sensor in setdiff(names(time_series), "timestamp")) {
    dygraph <- dygraph %>%
      dygraphs::dySeries(
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
