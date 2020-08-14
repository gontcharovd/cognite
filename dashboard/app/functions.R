# General functions used across the Shiny app.

# Execute an SQL query.
#
# Args:
#   query (character): PostgreSQL query to be executed
# Returns:
#   (dataframe): the result of the query
execute_query <- function(query) {
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

# Add single quotes around a string for SQL compatibility.
#
# Args:
#   char (character): vector of strings to be quoted
# Returs:
#   (character): combined string with added single quotes around each element
add_quotes <- function(char) {
  char_quote <- sapply(char, function(x)  paste0("'", x, "'"))
  char_combined <- paste(char_quote, collapse = ", ")
  return(char_combined)
}
