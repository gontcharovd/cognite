APP_DIR <- '/home/gontcharovd/code/personal_projects/cognite/app'
source(file.path(APP_DIR, "functions.R"))

dates <- c("2020-07-01", "2020-07-10")
sensors <- c("23-PT-92537", "23-PT-92535", "23-PT-92540")

query_data  <- paste0("
SELECT 
  timestamp
  , asset_id
  , sensor_name
  , pressure
FROM
  compressor_pressure
WHERE
  sensor_name IN (", add_quotes(sensors), ") AND
  timestamp BETWEEN ", add_quotes(dates[1]), " AND ", add_quotes(dates[2]), ";
"
)
data <- execute_query(query_data)
print(head(data))
