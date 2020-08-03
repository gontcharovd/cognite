# https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php
# https://shiny.rstudio.com/articles/images.html

get_flowsheet_list <- function(input, output, session, sensors, config) {
  # for each selected sensor, draw a rectangle
  image_path <- config$flowsheet$image_path
  outfile <- tempfile(
    fileext = ".png"
    # tmpdir = config$flowsheet$tmpdir
  )
  png(outfile)
  image <- magick::image_read(image_path)
  image_draw <- magick::image_draw(image)
  graphics::rect(53, 36, 820, 590, border = "red", lty = "solid", lwd = 5)
  dev.off()
  magick::image_browse(image_draw)
  flowsheet_list <- list(
    src = outfile,
    alt = config$flowsheet$alt,
    height = config$flowsheet$height,
    width = config$flowsheet$width
  )
  return(flowsheet_list)
}

# x, y
# 53, 36
# 82, 59

# dev.off()

# image_browse(image)

# image_browse(image_draw)
