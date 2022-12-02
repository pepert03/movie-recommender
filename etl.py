import pandas as pd

# id,imdb_id,popularity,budget,revenue,original_title,cast,homepage,director,tagline,keywords,overview,runtime,genres,production_companies,release_date,vote_count,vote_average,release_year,budget_adj,revenue_adj
df4 = pd.read_csv('./data/tmdb_movies_data.csv', sep=',', encoding='utf-8')

# Borrar columnas innecesarias
df4 = df4.drop(['id', 'imdb_id', 'revenue', 'homepage', 'tagline', 'overview', 'runtime', 'release_date', 'vote_count', 'release_year', 'budget_adj', 'revenue_adj'], axis=1)

# Renombrar columnas df4
df4 = df4.rename(columns={'original_title': 'title', 'production_companies': 'companies', 'vote_average': 'score'})

# Guardar df4 en csv
df4.to_csv('./data/movies.csv', sep=',', encoding='utf-8', index=False)