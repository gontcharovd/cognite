dotenv::load_dot_env()

con <- DBI::dbConnect(
   RPostgres::Postgres(),
   dbname = "cognite",
   host = "localhost",
   port = 5432,
   user = Sys.getenv("USER"),
   password = Sys.getenv("PWD") 
)

DBI::dbListTables(con)

query <- "select * from compressor_pressure order by timestamp desc limit 10;"
data <- DBI::dbGetQuery(con, query)
head(data)

sapply(data, class)
