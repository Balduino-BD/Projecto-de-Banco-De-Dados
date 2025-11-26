


import pymysql
from config import DB_CONFIG

def get_connection(db_name=True):
    
    
    """
   -- Abre uma conexão com o MySQL usando PyMySQL.
   -- Se db_name=False, ignora a chave 'database' do config.
    """
    
    
    cfg = DB_CONFIG.copy()

    if not db_name and "database" in cfg:
        cfg.pop("database")

    conn = pymysql.connect(
        host=cfg.get("host", "localhost"),
        user=cfg.get("user", "root"),
        password=cfg.get("password", ""),
        database=cfg.get("database") if db_name else None,
        port=cfg.get("port", 3306),
        charset="utf8mb4",
        autocommit=False
    )
    return conn


def execute_ddl(ddl_sql, use_db=True):
    """
    -- Executa um bloco de comandos DDL (CREATE, DROP, INSERT...).
    """
    conn = get_connection(db_name=use_db)
    cur = conn.cursor()
    for stmt in ddl_sql.split(";"):
        s = stmt.strip()
        if s:
            cur.execute(s)
    conn.commit()
    cur.close()
    conn.close()


def execute_query(sql, params=None):
    """
   --  Executa SELECT e retorna (colunas, linhas)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return cols, rows


def execute_dml(sql, params=None):
    """
    -- Executa INSERT, UPDATE e DELETE.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    conn.commit()
    cur.close()
    conn.close()
