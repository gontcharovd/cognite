# Shiny module that outputs an image with annotated sensors.

# Obtain a given coord for a given sensor from the config file.
#
# Args:
#   sensor (character): sensor name
#   coord (character): sensor key in config.json
#   config (list): config.json file data
# Returns:
#   (numeric): x, y or radius of a circle that highlights a sensor
get_coord <- function(sensor, coord, config) {
  coord <- eval(
    substitute(
      config$sensors$sensor_name$coord,
      list(sensor_name = sensor, coord = coord)
    )
  )
  return(coord)
}

# Assemble a list that can be rendered to an image.
#
# Args:
#   input: not used
#   output: not used
#   session: not used
#   sensors (character, reactive): selected sensors from `get_sensors` module
#   config (list): settings from the json config file
# Returns:
#   (list, reactive): list containing the annotated image
get_flowsheet_list <- function(input, output, session, sensors, config, app_dir) {
  image_path <- file.path(app_dir, "input", "compressor_flowsheet.png")
  tmpdir <- file.path(app_dir, "input")
  flowsheet_list <- reactive({
    image <- magick::image_read(image_path)
    image_draw <- magick::image_draw(image)
    if (length(sensors() > 0)) {
      x_coords <- sapply(sensors(), function(s) get_coord(s, "x", config))
      y_coords <- sapply(sensors(), function(s) get_coord(s, "y", config))
      radii <- sapply(sensors(), function(s) get_coord(s, "radius", config))
      colors <- sapply(sensors(), function(s) get_coord(s, "color", config))
      graphics::symbols(
        x_coords,
        y_coords,
        circles = radii,
        inches = FALSE,
        fg = colors,
        bg = colors,
        add = TRUE
      )
    }
    dev.off()
    tmpfile <- magick::image_write(
      image_draw,
      tempfile(fileext = ".png", tmpdir = tmpdir),
      format = "png"
    )
    flowsheet_list <- list(
      src = tmpfile,
      alt = config$flowsheet$alt,
      height = config$flowsheet$height,
      width = config$flowsheet$width
    )
    flowsheet_list
  })
  return(flowsheet_list)
}
