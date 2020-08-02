# https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php
# https://shiny.rstudio.com/articles/images.html

get_flowsheet <- function(input, output, session, config, image) {
  flowsheet <- shiny::reactive({
    list(
      src = image(),
      width = 400,
      height = 200,
      alt = "This is my flowsheet."
    )
  })
  return(flowsheet)
}

# x, y
# 53, 36
# 82, 59

# image_draw <- image_draw(image)
# rect(53, 36, 82, 59, border = "red", lty = "solid", lwd = 5)
# dev.off()

# image_browse(image)

# image_browse(image_draw)
