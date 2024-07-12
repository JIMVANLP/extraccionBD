import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Configura tus detalles de conexión
username = 'root'
password = ''
host = 'localhost'
port = '3306'
database = 'northwind'

# Crear la cadena de conexión
connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

# Crear el motor de SQLAlchemy
engine = create_engine(connection_string)

# Especifica tu consulta SQL
query = '''
WITH employeeTerritories AS (
   SELECT 
      et.EmployeeID, 
      MAX(t.RegionID) AS RegionID
   FROM 
      employeeterritories et 
      INNER JOIN Territories t ON t.TerritoryID = et.TerritoryID
   GROUP BY et.EmployeeID
), TotalSales AS (
   SELECT
      YEAR(O.OrderDate) AS _year,
      R.RegionDescription,
      C.CustomerID,
      C.CompanyName,
      SUM(OD.Quantity * OD.UnitPrice) AS TotalSpent
   FROM 
      Orders O
      INNER JOIN `Order Details` OD ON O.OrderID = OD.OrderID
      INNER JOIN Customers C ON O.CustomerID = C.CustomerID
      INNER JOIN employeeTerritories ER ON O.EmployeeID = ER.EmployeeID
      INNER JOIN Region R ON ER.RegionID = R.RegionID
   GROUP BY 
      YEAR(O.OrderDate), R.RegionDescription, C.CustomerID, C.CompanyName
), Ranking AS (
    SELECT
      _year,
      RegionDescription,
      CustomerID,
      CompanyName,
      TotalSpent,
      RANK() OVER (PARTITION BY _year, RegionDescription ORDER BY TotalSpent DESC) AS Rk
    FROM TotalSales
)
SELECT 
   RegionDescription,
   _year,
   CustomerID,   
   CompanyName,
   TotalSpent
FROM 
   Ranking
WHERE 
   Rk = 1
ORDER BY 
_year,
RegionDescription;
'''

# Ejecuta la consulta y obtiene los datos en un DataFrame
df = pd.read_sql(query, engine)

# Configurar matplotlib para crear la tabla
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('tight')
ax.axis('off')

# Crear la tabla
table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

# Ajustar el tamaño de las celdas
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.2)

# Mostrar la tabla
plt.show()
