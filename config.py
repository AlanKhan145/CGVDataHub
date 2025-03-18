"""
Cấu hình kết nối MongoDB và các thông số liên quan đến việc thu thập dữ liệu phim từ CGV.
"""

MONGO_URL = "mongodb+srv://CgvHub:o@cluster0.ktuns.mongodb.net/"
DATABASE_NAME = "cgv_movies"

# Tên collection trong MongoDB
FILM_COLLECTION_NAME = "films"
NEW_OFFER_COLLECTION_NAME = "new_offers"
THEATERS_COLLECTION_NAME = "theaters"
# URL của các trang phim
NEW_OFFERS_URL = "https://www.cgv.vn/default/newsoffer/"
NOW_SHOWING_URL = "https://www.cgv.vn/default/movies/now-showing.html"
COMING_SOON_URL = "https://www.cgv.vn/default/movies/coming-soon-1.html"
THEATERS_URL = "https://www.cgv.vn/default/cinox/site/"
# Thời gian chờ (giây) giữa các lần thu thập dữ liệu
WAIT_TIME = 2