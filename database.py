from pymongo import MongoClient
from config import MONGO_URL, DATABASE_NAME


def get_database():
    """
    Kết nối đến MongoDB và trả về đối tượng cơ sở dữ liệu.

    Returns:
        Database | None:
            - Đối tượng database nếu kết nối thành công.
            - None nếu có lỗi xảy ra.
    """
    try:
        client = MongoClient(MONGO_URL)
        database = client[DATABASE_NAME]
        print(f"Kết nối thành công đến cơ sở dữ liệu: '{DATABASE_NAME}'")
        return database
    except Exception as loi:
        print(f"Lỗi khi kết nối MongoDB: {loi}")
        return None


def save_to_database(col, data):
    """
    Lưu hoặc cập nhật thông tin phim vào cơ sở dữ liệu.

    Args:
        col (Collection): Collection phim trong MongoDB.
        data (dict): Dữ liệu phim cần lưu.

    Returns:
        None
    """
    result = col.update_one(
        {"title": data["title"]},
        {"$set": data},
        upsert=True
    )

    if result.matched_count == 0:
        print(f"Thêm mới: {data['title']}")
    else:
        print(f"Cập nhật: {data['title']}")
