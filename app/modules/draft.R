config <- jsonlite::read_json(
  file.path(app_dir, "input", "config.json")
)
image_path <- config$flowsheet$image_path
image <- magick::image_read(image_path)
image_draw <- magick::image_draw(image)
x <- seq(0, 1000, 10) 
y <- rep(566, 101)
r <- rep(2, 101)
c <- rep("red", 101)
graphics::symbols(x, y, circles = r, inches = FALSE, add = TRUE, fg = c)
dev.off()
magick::image_browse(image_draw)
