FROM rocker/shiny:3.6.3

RUN apt update 
RUN apt install -y libcurl4-openssl-dev libmagick++-dev libpq-dev unixodbc-dev

RUN R -e "install.packages('renv', version = '0.11.0')"

WORKDIR /home/dashboard 
COPY renv.lock .
# RUN R -e "renv::init(bare = TRUE)"
RUN R -e "renv::restore()"

# it would be better to clone the app from GitHub
COPY app .

ENV APP_DIR=/home/dashboard/app

EXPOSE 3838 5432

# CMD R -e "shiny::runApp('app/app.R', host = '0.0.0.0', port = 3838)"
CMD tail -f /dev/null
