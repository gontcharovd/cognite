# https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php
# https://shiny.rstudio.com/articles/images.html

get_flowsheet_list <- function(input, output, session, sensors, config) {
  image_path <- config$flowsheet$image_path
  image <- magick::image_read(image_path)
  image_draw <- magick::image_draw(image)
  graphics::rect(53, 36, 820, 590, border = "red", lty = "solid", lwd = 5)
  dev.off()
  tmpfile <- magick::image_write(
    image_draw,
    tempfile(fileext = ".png", tmpdir = config$flowsheet$tmpdir),
    format = "png"
  )
  flowsheet_list <- list(
    src = tmpfile,
    alt = config$flowsheet$alt,
    height = config$flowsheet$height,
    width = config$flowsheet$width
  )
  return(flowsheet_list)
}
