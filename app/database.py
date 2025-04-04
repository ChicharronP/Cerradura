import sqlite3
import hashlib
from contextlib import closing

class DatabaseManager:
    def __init__(self, db_name='secure_keys.db'):
        self.db_name = db_name
        self._initialize_db()
    
    def _initialize_db(self):
        with closing(sqlite3.connect(self.db_name)) as conn:
            cursor = conn.cursor()
            # Tabla para claves de acceso
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS access_keys (
                    id INTEGER PRIMARY KEY,
                    key_value TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Tabla para administradores
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            ''')
            # Insertar admin por defecto si no existe
            if not self._admin_exists():
                self._create_default_admin()
            conn.commit()
    
    def _admin_exists(self):
        with closing(sqlite3.connect(self.db_name)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM admins LIMIT 1")
            return cursor.fetchone() is not None
    
    def _create_default_admin(self):
        default_password = "admin123"
        hashed = hashlib.sha256(default_password.encode()).hexdigest()
        with closing(sqlite3.connect(self.db_name)) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO admins (username, password_hash)
                VALUES (?, ?)
            ''', ('admin', hashed))
            conn.commit()
    
    def add_access_key(self, key):
        try:
            with closing(sqlite3.connect(self.db_name)) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO access_keys (key_value)
                    VALUES (?)
                ''', (key,))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def key_exists(self, key):
        with closing(sqlite3.connect(self.db_name)) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 1 FROM access_keys
                WHERE key_value = ?
            ''', (key,))
            return cursor.fetchone() is not None
    
    def get_all_keys(self):
        with closing(sqlite3.connect(self.db_name)) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT key_value, created_at
                FROM access_keys
                ORDER BY created_at DESC
            ''')
            return cursor.fetchall()
    
    def verify_admin(self, password):
        with closing(sqlite3.connect(self.db_name)) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT password_hash FROM admins
                WHERE username = 'admin'
            ''')
            result = cursor.fetchone()
            if result:
                return hashlib.sha256(password.encode()).hexdigest() == result[0]
            return False