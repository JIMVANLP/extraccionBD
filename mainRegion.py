import pandas as pd
import tabulate
from sqlalchemy import create_engine

# Configuración de la conexión a la base de datos
database_tipo = 'mysql+pymysql'  # Usando pymysql como conector
usuario = 'root'
contraseña = ''
host = 'localhost'
puerto = 3306
nombre_bd = 'Northwind'

# Consulta SQL
query = """
SELECT 
    r.RegionDescription as region, 
    SUM(od.UnitPrice * od.Quantity) AS ganancias 
FROM Orders o 
JOIN `order details` od ON o.OrderID = od.OrderID 
JOIN Products p ON od.ProductID = p.ProductID 
JOIN Customers c ON o.CustomerID = c.CustomerID 
JOIN Employees e ON o.EmployeeID = e.EmployeeID 
JOIN EmployeeTerritories et ON e.EmployeeID = et.EmployeeID 
JOIN Territories t ON et.TerritoryID = t.TerritoryID 
JOIN Region r ON t.RegionID = r.RegionID 
GROUP BY r.RegionDescription;
"""

# Cadena de conexión
cadena_conexion = f'{database_tipo}://{usuario}:{contraseña}@{host}:{puerto}/{nombre_bd}'

# Crear el motor
motor = create_engine(cadena_conexion)

try:
    # Leer la consulta
    df = pd.read_sql_query(query, motor)

    # Darle formato a los datos
    df['ganancias'] = df['ganancias'].map('${:,.2f}'.format)

    # Mostrar el resultado usando tabulate
    print(tabulate.tabulate(df, headers='keys', tablefmt='pretty'))

    # Crear un archivo CSV
    df.to_csv('ganancias_por_region.csv', index=False)
    print("Archivo 'ganancias_por_region.csv' creado exitosamente.")
except Exception as e:
    print(f"Error: {e}")
