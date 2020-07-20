library(DBI)


con <- DBI::dbConnect(
   RPostgres::Postgres(),
   dbname = "postgres",
   host = "/var/run/postgresql",
   user = "postgres",
   port = 5432
)

pg <- dbDriver("PostgreSQL")

con <- DBI::dbConnect(
   odbc::odbc(),
   driver = "PostgreSQL UNICODE",
   dbname = "cognite",
   host = "localhost",
   user = "cognite",
   db_port = 5432,
   db_password = "cognite"
)

con <- dbConnect(odbc::odbc(), "PostgreSQL ANSI")

con <- dbConnect(RPostgres::Postgres())
