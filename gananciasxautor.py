# main.py

from database_manager import DatabaseManager

if __name__ == "__main__":
    # Crear una instancia de DatabaseManager
    db_manager = DatabaseManager(user='root', password='', host='localhost', database='pubs')

    # Conectar a la base de datos
    db_manager.connect()

    # Calcular y exportar ganancias
    db_manager.calculate_earnings()
