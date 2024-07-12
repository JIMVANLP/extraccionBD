import pandas as pd
import matplotlib.pyplot as plt

# Crear un DataFrame
data = {'Name': ['John', 'Anna', 'Peter', 'Linda'],
        'Age': [28, 24, 35, 32]}
df = pd.DataFrame(data)

# Mostrar el DataFrame
print(df)

# Seleccionar una columna
ages = df['Age']
print(ages)

# Filtrar filas donde la edad es mayor a 30
adults = df[df['Age'] > 30]
print(adults)



# Crear un gráfico de barras de las edades
df['Age'].plot(kind='bar')

# Etiquetas para el eje x
plt.xticks(range(len(df['Name'])), df['Name'])

# Etiquetas para los ejes
plt.xlabel('Name')
plt.ylabel('Age')

# Mostrar el gráfico
plt.show()