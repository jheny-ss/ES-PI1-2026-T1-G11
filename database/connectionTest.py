from connection import get_connection

try:
    conn = get_connection()
    print("Conectado ao banco!")
    conn.close()
except Exception as e:
    print("Erro:", e)
