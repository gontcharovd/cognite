FROM rocker/r-base:3.6.3

# needed for RPostgreSQL
RUN apt update 
RUN apt install -y libpq-dev
RUN apt install -y unixodbc-dev
RUN apt install -y libcurl4-openssl-dev

# I need to install the Postgres ODBC driver as well

ENV RENV_VERSION 0.11.0-23
RUN R -e "install.packages('remotes', repos = c(CRAN = 'https://cloud.r-project.org'))"
RUN R -e "remotes::install_github('rstudio/renv@${RENV_VERSION}')"

WORKDIR /home/dashboard 
COPY renv.lock .
RUN R -e 'renv::restore()'

COPY .Rprofile .
COPY app app

EXPOSE 5000

# CMD R -e 'shiny::runApp('app/app.R', port="5000")'

CMD tail -f /dev/null
