from domain.mysqlndexer import MySQLDatabase
from agents import function_tool

@function_tool
def get_all_infor_building() -> str:
    """Lấy thông tin tất cả các tòa nhà."""
    db = MySQLDatabase()
    building = db.fetch_all("SELECT * FROM building")
    db.close()
    return building

@function_tool
def get_building_by_id(id: int) -> str:
    """Lấy thông tin tòa nhà theo ID."""
    db = MySQLDatabase()
    building = db.fetch_one("SELECT * FROM building WHERE id = %s", (id,))
    db.close()
    return building

@function_tool
def get_building_by_name(name: str) -> dict:
    """Lấy thông tin tòa nhà theo tên."""
    db = MySQLDatabase()
    try:
        query = "SELECT * FROM building WHERE name LIKE %s"
        building = db.fetch_one(query, (f"%{name}%",))  # Thêm wildcard %
        return building if building else {}  # Trả về dict rỗng nếu không có kết quả
    finally:
        db.close()  # Đảm bảo đóng kết nối


@function_tool
def get_building_by_ward(ward: str) -> str:
    """Lấy thông tin tòa nhà theo địa chỉ."""
    db = MySQLDatabase()
    query = "SELECT * FROM building WHERE ward LIKE %s"
    building = db.fetch_one("SELECT * FROM building WHERE ward = %s", (ward,))
    db.close()
    return building

