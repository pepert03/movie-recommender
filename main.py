import os
import pandas as pd
import re
import sys


movies = pd.read_csv('./data/movies.csv', sep=',', encoding='utf-8')
movies = movies.fillna(0)

def limpiar_pantalla():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1 
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def buscar_pelicula(pelicula):
    id = -1
    posibles = []
    for i in range(len(movies)):
        a = movies['title'][i].lower()
        if pelicula == a:
            posibles.append((i, 10))
        else:
            b = re.split(' |,|:|;|\.|-', a)
            p = re.split(' |,|:|;|\.|-', pelicula)
            n = 0
            for palabra in p:
                if palabra in b:
                    n += 1
            n -= levenshtein(pelicula, a)
            if n != 0:
                posibles.append((i,n))

    if len(posibles) > 0:
        print('Results:')
        posibles.sort(key=lambda x: x[1], reverse=True)
        for i in range(10):
            print(i+1,'"{}" by'.format(movies['title'][posibles[i][0]]), "\033[3m" +movies['director'][posibles[i][0]]+"\033[0m")
            if i == len(posibles)-1:
                break
        try:
            opcion = input('> ')
            id = posibles[int(opcion)-1][0]
        except:
            id = -1
    
    return id

def recomendacion(id):
    recomendaciones = [(-1,0)]

    generos1 = re.split('|', movies['genres'][id])
    director1 = re.split('|', movies['director'][id])
    cast1 = re.split('|', movies['cast'][id])
    keywords1 = re.split('|', movies['keywords'][id])
    companies1 = re.split('|', movies['companies'][id])

    for i in range(len(movies)):
        similitud = 0
        if id != i:
            # Genres
            if movies['genres'][i]:
                generos2 = re.split('|', movies['genres'][i])
                for genero in generos1:
                    if genero in generos2:
                        similitud += 3
                generos2 = re.split('|', movies['genres'][i])
            # Director
            if movies['director'][i]:
                director2 = re.split('|', movies['director'][i])
                for director in director1:
                    if director in director2:
                        similitud += 5
            # Cast
            if movies['cast'][i]:
                cast2 = re.split('|', movies['cast'][i])
                for actor in cast1:
                    if actor in cast2:
                        similitud += 2
            # Keywords
            if movies['keywords'][i]:
                keywords2 = re.split('|', movies['keywords'][i])
                for keyword in keywords1:
                    if keyword in keywords2:
                        similitud += 2
            # Score
            similitud += movies['score'][i]/2
            recomendaciones.append((i,similitud))
            # Companies
            if movies['companies'][i]:
                companies2 = re.split('|', movies['companies'][i])
                for company in companies1:
                    if company in companies2:
                        similitud += 1


    recomendaciones.sort(key=lambda x: x[1], reverse=True)
    return recomendaciones[:10]

def info_pelicula(id):
    limpiar_pantalla()
    print(movies['title'][id])
    print('Director:',movies['director'][id])
    print('Cast:',movies['cast'][id])
    print('Companies:',movies['companies'][id])
    print('Genres:',movies['genres'][id])
    print('Score:',movies['score'][id])
    
def main():
    while True:
        limpiar_pantalla()
        pelicula = input('Search: ')
        pelicula = pelicula.lower()
        id = buscar_pelicula(pelicula)
        try:
            if id != -1:
                info_pelicula(id)
                input('See recommendations')

                limpiar_pantalla()
                recomendaciones = recomendacion(id)
                print('Recommendations:')
                for i in range(10):
                    print(i+1,movies['title'][recomendaciones[i][0]])
                    if i == len(recomendaciones)-1:
                        break
                n = input('> ')
                id = recomendaciones[int(n)-1][0]
                info_pelicula(id)
                pelicula = input('> ')
            else:
                limpiar_pantalla()
                print('No results found')
                pelicula = input('> ')
        except:
            limpiar_pantalla()
            print('Invalid option')
            pelicula = input('> ')
        if pelicula == 'exit':
            break

if __name__ == "__main__":
    main()
