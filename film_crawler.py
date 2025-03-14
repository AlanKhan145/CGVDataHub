from selenium.webdriver.common.by import By
import time
from detail_crawler import extract_film_details
from database import save_to_database

def extract_film_info(driver, url,films_col):
    """
    Trích xuất danh sách phim từ trang web.

    Args:
        driver (webdriver): Đối tượng trình điều khiển Selenium.
        url (str): Đường dẫn trang web cần lấy thông tin phim.

    Returns:
        list: Danh sách các bộ phim với thông tin chi tiết gồm đường dẫn, poster,
              trạng thái đặt vé, tiêu đề, thể loại, thời lượng, ngày phát hành,
              đạo diễn, diễn viên, ngôn ngữ và mô tả.
    """
    film_list = []
    driver.get(url)
    time.sleep(2)  # Chờ trang tải

    # Tìm tất cả phần tử <li> chứa thông tin phim
    films = driver.find_elements(By.CLASS_NAME, "film-lists.item.last")
    for film in films:
        try:
            link_element = film.find_element(By.CSS_SELECTOR, "a.product-image")
            link_url = link_element.get_attribute("href")

            img_element = film.find_element(By.CSS_SELECTOR, "a.product-image img")
            poster = img_element.get_attribute("src")

            film_info_detail = extract_film_details(link_url)

            # Kiểm tra nút mua vé
            ticket_available = bool(film.find_elements(By.CSS_SELECTOR, "button.btn-booking"))

            film_info = {
                "link": link_url,
                "poster": poster,
                "ticket_available": ticket_available,
                "title": film_info_detail.get("title"),
                "genre": film_info_detail.get("genre"),
                "duration": film_info_detail.get("duration"),
                "release_date": film_info_detail.get("release_date"),
                "director": film_info_detail.get("director"),
                "actors": film_info_detail.get("actors"),
                "language": film_info_detail.get("language"),
                "description": film_info_detail.get("description"),
                "rated" : film_info_detail.get("rated"),
                "technologies" : film_info_detail.get("technologies"),
            }

            film_list.append(film_info)
            save_to_database(films_col, film_info)
        except Exception as e:
            print(f"Lỗi khi trích xuất phim: {e}")

    return film_list

