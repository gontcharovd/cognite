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

