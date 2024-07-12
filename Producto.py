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
WITH
    CTE_EmpRegion AS (
        SELECT et.EmployeeID, MAX(t.RegionID) AS RegionID
        FROM EmployeeTerritories et
        INNER JOIN Territories t ON t.TerritoryID = et.TerritoryID
        GROUP BY et.EmployeeID
    ),
    TotalCompras AS (
        SELECT
            C.CustomerID,
            C.CompanyName AS NombreCliente,
            R.RegionDescription,
            P.ProductName,
            YEAR(O.OrderDate) AS Año,
            SUM(OD.Quantity) AS TotalComprado
        FROM Orders O
        INNER JOIN `Order Details` OD ON O.OrderID = OD.OrderID
        INNER JOIN Customers C ON O.CustomerID = C.CustomerID
        INNER JOIN Products P ON OD.ProductID = P.ProductID
        INNER JOIN CTE_EmpRegion ER ON O.EmployeeID = ER.EmployeeID
        INNER JOIN Region R ON ER.RegionID = R.RegionID
        GROUP BY C.CustomerID, C.CompanyName, R.RegionDescription, P.ProductName, YEAR(O.OrderDate)
    ),
    Ranking AS (
        SELECT
            CustomerID,
            NombreCliente,
            RegionDescription,
            ProductName,
            Año,
            TotalComprado,
            RANK() OVER (PARTITION BY CustomerID, RegionDescription ORDER BY TotalComprado ASC) AS Rk
        FROM TotalCompras
    ),
    LeastPurchasedProducts AS (
        SELECT
            CustomerID,
            NombreCliente,
            RegionDescription,
            CONCAT(ProductName, ' (', Año, ')') AS Producto_Año
        FROM Ranking
        WHERE Rk = 1
    )
SELECT
    NombreCliente AS Cliente,
    MAX(CASE WHEN RegionDescription = 'Northern' THEN Producto_Año END) AS Northern,
    MAX(CASE WHEN RegionDescription = 'Southern' THEN Producto_Año END) AS Southern,
    MAX(CASE WHEN RegionDescription = 'Westerns' THEN Producto_Año END) AS Westerns,
    MAX(CASE WHEN RegionDescription = 'Eastern' THEN Producto_Año END) AS Eastern
FROM LeastPurchasedProducts
GROUP BY NombreCliente
ORDER BY NombreCliente;
"""

# Cadena de conexión
cadena_conexion = f'{database_tipo}://{usuario}:{contraseña}@{host}:{puerto}/{nombre_bd}'

# Crear el motor
motor = create_engine(cadena_conexion)

try:
    # Leer la consulta
    df = pd.read_sql_query(query, motor)

    # Ajuste de ancho de columna
    pd.set_option('display.max_colwidth', 20)  # Limita el ancho de las columnas
    pd.set_option('display.max_columns', 10)   # Limita el número de columnas mostradas

    # Mostrar el resultado usando tabulate con formato compacto
    print(tabulate.tabulate(df, headers='keys', tablefmt='pipe', numalign="right", stralign="left"))

    # Crear un archivo CSV
    df.to_csv('productos_menos_comprados_por_cliente_y_region.csv', index=False)
    print("Archivo 'productos_menos_comprados_por_cliente_y_region.csv' creado exitosamente.")
except Exception as e:
    print(f"Error: {e}")
