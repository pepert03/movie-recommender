Movie Recommender
=================

## Introduction
Install the following packages:
```
pip install -r requirements.txt
```
The `data` folder contains the following files:
* `tmdb_movies_data.csv`: dataset with 10,000 movies from Tmdb

## ETL
Run the `etl.py` file to clean up the dataset. Generates a clean csv `movies.csv`, needed by the main program.

## Movie Recommender
Run `main.py` to start the program. The program will ask you to enter a movie title. It will then recommend 10 movies similar to the one you entered.

**Note**: There are only movies available until 2017.

