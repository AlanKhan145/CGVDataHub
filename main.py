from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from database import get_database , save_to_database
from extract_info import extract_film_info, extract_newoffer_info , extract_all_theaters_info
from config import *


def main():
    """
    Chương trình thu thập thông tin phim từ trang web CGV và lưu vào MongoDB.

    - Kết nối MongoDB.
    - Khởi chạy trình duyệt Selenium.
    - Trích xuất thông tin phim từ các trang "Đang chiếu" và "Sắp chiếu".
    - Lưu hoặc cập nhật dữ liệu phim vào MongoDB.
    """

    # Kết nối MongoDB
    db = get_database()
    if db is None:
        print("Kết nối cơ sở dữ liệu thất bại. Đang thoát...")
        return

    films_col = db[FILM_COLLECTION_NAME]
    newoffers_col = db[NEW_OFFER_COLLECTION_NAME]
    theaters_col = db[THEATERS_COLLECTION_NAME]
    # Khởi tạo trình điều khiển Chrome
    service = Service()
    driver = webdriver.Chrome(service=service)


    try:
        print(" Đang tải dữ liệu phim, vui lòng chờ...")
        # Thu thập dữ liệu phim
        extract_film_info(driver, NOW_SHOWING_URL,films_col)
        extract_film_info(driver, COMING_SOON_URL,films_col)
        print(" Đang tải dữ liệu tin khuyến mãi, vui lòng chờ...")
        extract_newoffer_info(driver, NEW_OFFERS_URL,newoffers_col)
        print(" Đang tải dữ liệu sạp chiếu, vui lòng chờ...")
        extract_all_theaters_info(driver, THEATERS_URL,theaters_col)
    except Exception as e:
        print(f" Đã xảy ra lỗi: {e}")

    finally:
        driver.quit()
        print("Trình duyệt đã được đóng.")


if __name__ == "__main__":
    main()
