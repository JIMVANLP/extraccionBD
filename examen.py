import pandas as pd
from sqlalchemy import create_engine
import tabulate

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
    RecentYears AS (
        SELECT DISTINCT
            YEAR(OrderDate) AS OrderYear
        FROM Orders
        ORDER BY OrderYear DESC
        LIMIT 3
    ),
    CategoryProductSales AS (
        SELECT
            c.CategoryName,
            p.ProductName,
            YEAR(o.OrderDate) AS OrderYear,
            SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS TotalEarnings,
            cust.CompanyName AS CustomerName,
            SUM(od.Quantity) AS TotalQuantity
        FROM `Order Details` od
        JOIN Orders o ON od.OrderID = o.OrderID
        JOIN Products p ON od.ProductID = p.ProductID
        JOIN Categories c ON p.CategoryID = c.CategoryID
        JOIN Customers cust ON o.CustomerID = cust.CustomerID
        WHERE YEAR(o.OrderDate) IN (SELECT OrderYear FROM RecentYears)
        GROUP BY c.CategoryName, p.ProductName, YEAR(o.OrderDate), cust.CompanyName
    ),
    TopProductByCategoryYear AS (
        SELECT
            CategoryName,
            OrderYear,
            ProductName,
            TotalEarnings,
            CustomerName,
            TotalQuantity,
            ROW_NUMBER() OVER (PARTITION BY CategoryName, OrderYear ORDER BY TotalEarnings DESC) AS rn
        FROM CategoryProductSales
    ),
    SalesWithCustomers AS (
        SELECT
            CategoryName,
            OrderYear,
            ProductName,
            TotalEarnings,
            MAX(CustomerName) AS MostBuyingCustomer,
            MIN(CustomerName) AS LeastBuyingCustomer,
            ROW_NUMBER() OVER (PARTITION BY CategoryName, OrderYear ORDER BY TotalEarnings DESC) AS rn
        FROM CategoryProductSales
        GROUP BY CategoryName, OrderYear, ProductName, TotalEarnings
    )
SELECT
    CategoryName,
    MAX(
        CASE
            WHEN OrderYear = (SELECT OrderYear FROM RecentYears ORDER BY OrderYear DESC LIMIT 1 OFFSET 0)
            AND rn = 1 THEN CONCAT(OrderYear, ': ', ProductName, ' ($', TotalEarnings, ') Cliente más comprador: ', MostBuyingCustomer, ' - Cliente menos comprador: ', LeastBuyingCustomer)
        END
    ) AS `Ultimo año`,
    MAX(
        CASE
            WHEN OrderYear = (SELECT OrderYear FROM RecentYears ORDER BY OrderYear DESC LIMIT 1 OFFSET 1)
            AND rn = 1 THEN CONCAT(OrderYear, ': ', ProductName, ' ($', TotalEarnings, ') Cliente más comprador: ', MostBuyingCustomer, ' - Cliente menos comprador: ', LeastBuyingCustomer)
        END
    ) AS `Penultimo año`,
    MAX(
        CASE
            WHEN OrderYear = (SELECT OrderYear FROM RecentYears ORDER BY OrderYear DESC LIMIT 1 OFFSET 2)
            AND rn = 1 THEN CONCAT(OrderYear, ': ', ProductName, ' ($', TotalEarnings, ') Cliente más comprador: ', MostBuyingCustomer, ' - Cliente menos comprador: ', LeastBuyingCustomer)
        END
    ) AS `Antepenultimo año`
FROM SalesWithCustomers
GROUP BY CategoryName;
"""

# Cadena de conexión
cadena_conexion = f'{database_tipo}://{usuario}:{contraseña}@{host}:{puerto}/{nombre_bd}'

# Crear el motor
motor = create_engine(cadena_conexion)

try:
    # Leer la consulta
    df = pd.read_sql_query(query, motor)

    # Ajuste de ancho de columna
    pd.set_option('display.max_colwidth', 30)  # Limita el ancho de las columnas
    pd.set_option('display.max_columns', 10)   # Limita el número de columnas mostradas

    # Mostrar el resultado usando tabulate con formato compacto
    print(tabulate.tabulate(df, headers='keys', tablefmt='pipe', numalign="right", stralign="left"))

    # Crear un archivo CSV
    df.to_csv('categorias_productos_clientes.csv', index=False)
    print("Archivo 'categorias_productos_clientes.csv' creado exitosamente.")
except Exception as e:
    print(f"Error: {e}")
