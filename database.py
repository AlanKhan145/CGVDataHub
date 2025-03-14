from pymongo import MongoClient
from config import MONGO_URL, DATABASE_NAME


def get_database():
    """
    Kết nối đến MongoDB và trả về đối tượng database.

    Returns:
        Database: Đối tượng database nếu kết nối thành công.
        None: Nếu có lỗi xảy ra trong quá trình kết nối.
    """
    try:
        client = MongoClient(MONGO_URL)
        db = client[DATABASE_NAME]
        print(f"Kết nối thành công đến database '{DATABASE_NAME}'")
        return db
    except Exception as e:
        print(f"Lỗi kết nối MongoDB: {e}")
        return None


def save_to_database(films_col, data):
    """
    Lưu hoặc cập nhật thông tin phim vào cơ sở dữ liệu.

    :param films_col: Collection phim trong MongoDB.
    :param data: Dữ liệu phim cần lưu.
    """
    result = films_col.update_one(
        {"title": data["title"]},
        {"$set": data},
        upsert=True
    )

    if result.matched_count == 0:
        print(f"[✅] Thêm mới: {data['title']}")
    else:
        print(f"[♻️] Cập nhật: {data['title']}")