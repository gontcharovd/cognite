# General functions used across the Shiny app.

#' Execute an SQL query.
#' @param query (character): PostgreSQL query to be executed
#' @return result (dataframe): the result of the query
execute_query <- function(query) {
  dotenv::load_dot_env()
  con <- DBI::dbConnect(
     RPostgres::Postgres(),
     dbname = "cognite",
     host = "localhost",
     port = 5432,
     user = Sys.getenv("USER"),
     password = Sys.getenv("PWD") 
  )
  result <- DBI::dbGetQuery(con, query)
  DBI::dbDisconnect(con)
  return(result)
}

#' Add single quotes around a string for SQL compatibility.
#' @param char (character): vector of strings to be quoted
#' @return char_quote (character): combined string
#' with added single quotes around each element
add_quotes <- function(char) {
  char_quote <- sapply(char, function(x)  paste0("'", x, "'"))
  char_combined <- paste(char_quote, collapse = ", ") 
  return(char_combined)
}
