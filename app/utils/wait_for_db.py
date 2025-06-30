import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

def wait_for_db_connection(database_url: str, timeout: int = 30):
    start_time = time.time()
    engine = create_engine(database_url)

    while True:
        try:
            with engine.connect():
                print("✅ Base de datos conectada correctamente.")
                return
        except OperationalError:
            if time.time() - start_time > timeout:
                raise TimeoutError("⛔ Tiempo de espera agotado para conectar a la base de datos.")
            print("⏳ Esperando conexión con la base de datos...")
            time.sleep(1)