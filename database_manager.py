import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

class DatabaseManager:
    def __init__(self, user, password, host, database):
        self.config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database
        }
        self.engine = None

    def connect(self):
        try:
            self.engine = create_engine(f"mysql+pymysql://{self.config['user']}:{self.config['password']}@{self.config['host']}/{self.config['database']}")
            print("Conexión exitosa a la base de datos")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")

    def query(self, sql):
        try:
            return pd.read_sql(sql, con=self.engine)
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return pd.DataFrame()

    def export_to_excel(self, df, filename):
        try:
            df.to_excel(filename, index=False)
            print(f"Datos exportados a {filename}")
        except Exception as e:
            print(f"Error al exportar a Excel: {e}")

    def visualize_data(self, df):
        try:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.axis('tight')
            ax.axis('off')
            table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(12)
            table.scale(1.2, 1.2)
            plt.show()
        except Exception as e:
            print(f"Error al visualizar los datos: {e}")

    def calculate_earnings(self):
        try:
            # Realizar consultas
            authors = self.query('SELECT * FROM authors')
            titleauthor = self.query('SELECT * FROM titleauthor')
            titles = self.query('SELECT * FROM titles')
            sales = self.query('SELECT * FROM sales')

            # Ganancias por autor
            df_authors = authors.merge(titleauthor, on='au_id').merge(titles, on='title_id').merge(sales, on='title_id')
            df_authors['total_earnings'] = df_authors['qty'] * df_authors['price'] * (df_authors['royaltyper'] / 100)
            df_authors = df_authors.groupby(['au_id', 'au_lname', 'au_fname'])['total_earnings'].sum().reset_index()
            df_authors['author_name'] = df_authors['au_lname'] + ' ' + df_authors['au_fname']

            # Total de ganancias de ventas
            sales_titles = sales.merge(titles, on='title_id')
            total_sales_earnings = (sales_titles['qty'] * sales_titles['price']).sum()

            # Ganancias totales por autor
            total_earnings_authors = df_authors['total_earnings'].sum()

            # Calcular ganancias de la editorial
            total_earnings_editorial = total_sales_earnings - total_earnings_authors

            # Crear un DataFrame para la fila adicional
            additional_row = pd.DataFrame({
                'au_id': [None],
                'au_lname': [None],
                'au_fname': [None],
                'total_earnings': [total_earnings_editorial],
                'author_name': ['Ganancia de editorial']
            })

            # Concatenar DataFrames
            df_final = pd.concat([df_authors, additional_row], ignore_index=True)

            # Ordenar el DataFrame según la lógica especificada
            df_final['order'] = df_final['author_name'].apply(lambda x: 1 if x == 'Ganancia de editorial' else 2)
            df_final = df_final.sort_values(by=['order', 'total_earnings'], ascending=[True, False]).drop(columns=['order'])

            # Mostrar primeras 10 filas
            print(df_final.head(10))

            # Exportar a Excel
            self.export_to_excel(df_final, 'ConsultaMatriz.xlsx')

            # Visualizar datos
            self.visualize_data(df_final)

        except Exception as e:
            print(f"Error al calcular ganancias: {e}")
