import pymysql
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

def get_db_connection():
    return pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)

def log_print_job(file_name, file_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO print_jobs (file_name, file_path) VALUES (%s, %s)", (file_name, file_path))
    conn.commit()
    conn.close()
