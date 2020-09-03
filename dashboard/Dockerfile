FROM rocker/r-base:3.6.3

RUN apt update 
RUN apt install -y libcurl4-openssl-dev libmagick++-dev libpq-dev unixodbc-dev

RUN R -e "install.packages('renv', version = '0.11.0')"

WORKDIR /home/dashboard 
COPY renv.lock renv.lock
RUN R -e "renv::restore()"

COPY app app

ENV APP_DIR=/home/dashboard/app

CMD R -e "shiny::runApp('app/app.R', host = '0.0.0.0', port = 3838)"
