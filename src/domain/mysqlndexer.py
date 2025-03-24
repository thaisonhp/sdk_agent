import mysql.connector
from mysql.connector import Error
from typing import Optional
class MySQLDatabase:
    def __init__(self, host: Optional[str] = "localhost",
                 user: Optional[str] = "root",
                 password: Optional[str] = "luongthaison",
                 database: Optional[str] = "estatebasic"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect()

    def connect(self):
        """Tạo kết nối đến MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("🔗 Kết nối MySQL thành công!")
        except Error as e:
            print(f"❌ Lỗi kết nối MySQL: {e}")

    def execute_query(self, query, params=None):
        """Thực thi câu lệnh INSERT, UPDATE, DELETE"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            print("✅ Truy vấn thực thi thành công!")
        except Error as e:
            print(f"❌ Lỗi thực thi truy vấn: {e}")

    def fetch_all(self, query, params=None):
        """Truy vấn dữ liệu và trả về tất cả kết quả"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"❌ Lỗi truy vấn: {e}")
            return None

    def fetch_one(self, query, params=None):
        """Truy vấn dữ liệu và trả về một dòng"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchone()
        except Error as e:
            print(f"❌ Lỗi truy vấn: {e}")
            return None

    def close(self):
        """Đóng kết nối MySQL"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Kết nối MySQL đã đóng.")

# -------------------------
# 💡 Ví dụ sử dụng class
# -------------------------

if __name__ == "__main__":
    db = MySQLDatabase()

    # Truy vấn tất cả dữ liệu từ bảng users
    buinlding  = db.fetch_all("SELECT * FROM building")
    print(buinlding)
    # Đóng kết nối
    db.close()
