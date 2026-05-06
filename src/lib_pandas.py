import pandas as pd

#serie = pd.Series([1,4,9], index=['A', 'B', 'C'])
#print (serie)

#data ={"nombre": ["Juan", "Ana", "Pedro"], "edad": [25, 30, 35], }

# df no es una variable sino un objeto de tipo DataFrame, es una tabla de datos con filas y columnas, similar a una hoja de cálculo o una base de datos.
#df = pd.DataFrame(data)

#imprime la primera fila del DataFrame (imprime la fila que tiene el indice 0)
#print(df.loc[0]) 

#imprime la primera y la tercera fila del DataFrame (imprime las filas que tienen los indices 0 y 2)
#print(df.loc[[0,2]])

#lee un archivo csv y lo convierte en un DataFrame
df = pd.read_csv(r"src/data.csv") 
print(df.head()) #imprime las primeras 5 filas del DataFrame, si le pone la cantidad de filas que quiere imprimir, por ejemplo df.head(3) imprime las primeras 3 filas del DataFrame
print(df.tail()) #imprime las ultimas 5 filas del DataFrame, si le pone la cantidad de filas que quiere imprimir, por ejemplo df.tail(3) imprime las ultimas 3 filas del DataFrame
print(df.describe()) 