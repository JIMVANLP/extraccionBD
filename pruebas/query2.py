import pandas as pd
from sqlalchemy import create_engine

class DatabaseConnection:
    def _init_(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.engine = self.create_engine()

    def create_engine(self):
        try:
            return create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}")
        except Exception as e:
            print(f"Error al crear el motor de conexión: {e}")
            raise

    def fetch_data(self, query):
        try:
            return pd.read_sql(query, con=self.engine)
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            raise

class DataProcessor:
    def _init_(self, authors, titleauthor, titles, sales):
        self.authors = authors
        self.titleauthor = titleauthor
        self.titles = titles
        self.sales = sales

    def calculate_author_earnings(self):
        df_authors = self.authors.merge(self.titleauthor, on='au_id').merge(self.titles, on='title_id').merge(self.sales, on='title_id')
        df_authors['total_earnings'] = df_authors['qty'] * df_authors['price'] * (df_authors['royaltyper'] / 100)
        df_authors = df_authors.groupby(['au_id', 'au_lname', 'au_fname'])['total_earnings'].sum().reset_index()
        df_authors['author_name'] = df_authors['au_lname'] + ' ' + df_authors['au_fname']
        return df_authors

    def calculate_total_sales_earnings(self):
        sales_titles = self.sales.merge(self.titles, on='title_id')
        return (sales_titles['qty'] * sales_titles['price']).sum()

    def calculate_earnings(self):
        df_authors = self.calculate_author_earnings()
        total_sales_earnings = self.calculate_total_sales_earnings()
        total_earnings_authors = df_authors['total_earnings'].sum()
        total_earnings_editorial = total_sales_earnings - total_earnings_authors

        additional_row = pd.DataFrame({
            'au_id': [None],
            'au_lname': [None],
            'au_fname': [None],
            'total_earnings': [total_earnings_editorial],
            'author_name': ['Ganancia de editorial']
        })

        df_final = pd.concat([df_authors, additional_row], ignore_index=True)
        df_final['order'] = df_final['author_name'].apply(lambda x: 1 if x == 'Ganancia de editorial' else 2)
        df_final = df_final.sort_values(by=['order', 'total_earnings'], ascending=[True, False]).drop(columns=['order'])
        return df_final

class ReportGenerator:
    def _init_(self, df_final):
        self.df_final = df_final

    def export_to_excel(self, output_file):
        try:
            self.df_final.to_excel(output_file, index=False)
            print(f"Datos exportados a {output_file}")
        except Exception as e:
            print(f"Error al exportar a Excel: {e}")
            raise

    def show_first_rows(self, num_rows=10):
        print(self.df_final.head(num_rows))

def main():
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'pubs'
    }

    connection = DatabaseConnection(**config)

    try:
        authors = connection.fetch_data('SELECT * FROM authors')
        titleauthor = connection.fetch_data('SELECT * FROM titleauthor')
        titles = connection.fetch_data('SELECT * FROM titles')
        sales = connection.fetch_data('SELECT * FROM sales')

        processor = DataProcessor(authors, titleauthor, titles, sales)
        df_final = processor.calculate_earnings()

        report = ReportGenerator(df_final)
        report.export_to_excel('ConsultaMatriz.xlsx')
        report.show_first_rows()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "_main_":
    main()