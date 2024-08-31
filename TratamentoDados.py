import pandas as pd

pokemonCsv = pd.read_csv('file.csv')

#Removendo valores nulos e NaN
pokemonCsv = pokemonCsv.dropna()

pokemonCsv.to_csv('pokemonSemDadosNulos.csv', index=False)