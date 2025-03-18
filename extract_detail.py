import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
from config import *
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

def get_value_by_label(driver: WebDriver, label: str) -> str:
    """
    Trả về giá trị văn bản của phần tử dựa trên nhãn được chỉ định.

    Hàm này tìm kiếm phần tử có nhãn chứa văn bản được cung cấp,
    sau đó lấy giá trị văn bản từ phần tử liền kề.

    Args:
        driver (WebDriver): Đối tượng trình điều khiển Selenium WebDriver.
        label (str): Văn bản của nhãn cần tìm.

    Returns:
        str: Giá trị văn bản của phần tử liền kề nếu tìm thấy, ngược lại trả về None.
    """
    try:
        element = driver.find_element(By.XPATH, f"//label[contains(text(), '{label}')]/following-sibling::div")
        return element.text.strip()
    except Exception:
        return None


def extract_film_details(url):
    """
    Trích xuất thông tin chi tiết của một bộ phim từ trang web.

    Args:
        url (str): Địa chỉ URL của trang phim.

    Returns:
        dict: Thông tin chi tiết của bộ phim, bao gồm tiêu đề, thể loại, thời lượng, ngày phát hành,
              đạo diễn, diễn viên, ngôn ngữ, mô tả, xếp hạng và công nghệ chiếu.
    """
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Chạy chế độ không hiển thị trình duyệt
    mini_driver = webdriver.Chrome(service=service, options=options)

    film_info_detail = {
        "title": None,
        "genre": None,
        "duration": None,
        "release_date": None,
        "director": None,
        "actors": None,
        "language": None,
        "description": None,
        "rated": None,
        "technologies": [],
    }

    try:
        mini_driver.get(url)
        time.sleep(2)

        # Lấy tiêu đề phim
        try:
            title_element = mini_driver.find_element(By.CSS_SELECTOR, "div.product-name span.h1")
            film_info_detail["title"] = title_element.text.strip()
        except Exception:
            pass

        # Lấy thông tin khác
        film_info_detail["genre"] = get_value_by_label(mini_driver, "Thể loại")
        film_info_detail["duration"] = get_value_by_label(mini_driver, "Thời lượng")
        film_info_detail["release_date"] = get_value_by_label(mini_driver, "Khởi chiếu")
        film_info_detail["director"] = get_value_by_label(mini_driver, "Đạo diễn")
        film_info_detail["language"] = get_value_by_label(mini_driver, "Ngôn ngữ")
        film_info_detail["rated"] = get_value_by_label(mini_driver, "Rated")

        # Lấy thông tin diễn viên
        actors_text = get_value_by_label(mini_driver, "Diễn viên") or get_value_by_label(mini_driver, "Diễn viên chính")
        film_info_detail["actors"] = actors_text if actors_text else "Không có thông tin"

        # Lấy mô tả phim
        try:
            description_element = mini_driver.find_element(By.CSS_SELECTOR, "meta[name='description']")
            film_info_detail["description"] = description_element.get_attribute("content").strip()
        except Exception:
            film_info_detail["description"] = None

        # Lấy các định dạng công nghệ phim
        try:
            technology_elements = mini_driver.find_elements(By.CSS_SELECTOR,
                                                            "div.movie-technology-icons a.movie-detail-icon-type span")
            film_info_detail["technologies"] = [tech.text.strip() for tech in technology_elements if tech.text.strip()]
        except Exception:
            film_info_detail["technologies"] = []

    except Exception as e:
        print(f"Lỗi khi lấy thông tin phim từ {url}: {e}")

    finally:
        mini_driver.quit()

    return film_info_detail


def extract_newoffer_details(url):
    """
    Trích xuất thông tin chi tiết khuyến mãi từ trang web.

    Tham số:
        url (str): URL của trang khuyến mãi cần trích xuất thông tin.

    Trả về:
        dict: Thông tin khuyến mãi bao gồm tiêu đề, hình ảnh và chi tiết khuyến mãi.
    """
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Chạy chế độ không hiển thị trình duyệt
    mini_driver = webdriver.Chrome(service=service, options=options)

    new_offer_details = {
        "title": None,
        "image": None,
        "promotion_details": ""
    }

    try:
        mini_driver.get(url)
        time.sleep(2)  # Chờ trang tải

        try:
            title_element = mini_driver.find_element(By.CSS_SELECTOR, "meta[name='title']")
            new_offer_details["title"] = title_element.get_attribute("content").strip()
        except Exception:
            new_offer_details["title"] = "Không tìm thấy tiêu đề"

        try:
            image_element = mini_driver.find_element(By.CSS_SELECTOR, "div.col-left-detail-content-new-offer img")
            new_offer_details["image"] = image_element.get_attribute("src")
        except Exception:
            new_offer_details["image"] = None

        try:
            promotion_elements = mini_driver.find_elements(By.CSS_SELECTOR, "div.social-daetail-content-new-offer p")
            promo_texts = [promo.text.strip() for promo in promotion_elements if promo.text.strip()]
            new_offer_details["promotion_details"] = "".join(promo_texts) if promo_texts else ""
        except Exception:
            new_offer_details["promotion_details"] = ""

    except Exception as e:
        print(f"Lỗi khi lấy thông tin khuyến mãi từ {url}: {e}")

    finally:
        mini_driver.quit()

    return new_offer_details


def extract_one_day(driver):
    """
    Trích xuất thông tin phim trong một ngày từ trang web.

    Tham số:
        driver (webdriver): Trình điều khiển Selenium WebDriver.

    Trả về:
        list: Danh sách các phim, bao gồm tên, link chi tiết, poster, định dạng chiếu và suất chiếu.
    """
    film_data = []
    film_elements = driver.find_elements(By.CLASS_NAME, "film-list")

    for film in film_elements:
        # Lấy tên phim & link chi tiết phim
        title_element = film.find_element(By.CSS_SELECTOR, ".film-label h3 a")
        film_title = title_element.text.strip()
        film_link = title_element.get_attribute("href")

        # Lấy link ảnh poster phim
        poster_element = film.find_element(By.CSS_SELECTOR, ".film-poster img")
        poster_url = poster_element.get_attribute("src")

        # Lấy định dạng chiếu (VD: 2D, Lồng Tiếng)
        film_formats = [fmt.text.strip() for fmt in film.find_elements(By.CLASS_NAME, "film-screen")]

        # Lấy danh sách suất chiếu & link đặt vé
        showtimes = []
        showtime_elements = film.find_elements(By.CSS_SELECTOR, ".film-showtimes li a")
        for showtime in showtime_elements:
            time_text = showtime.find_element(By.TAG_NAME, "span").text.strip()
            ticket_link = showtime.get_attribute("href")
            showtimes.append({"time": time_text, "link": ticket_link})

        # Lưu thông tin phim vào danh sách
        film_data.append({
            "title": film_title,
            "detail_link": film_link,
            "poster_url": poster_url,
            "formats": film_formats,
            "showtimes": showtimes
        })

    return film_data

def extract_all_days(driver):
    """
    Trích xuất thông tin phim cho tất cả các ngày từ trang web.

    Tham số:
        driver (webdriver): Trình điều khiển Selenium WebDriver.

    Trả về:
        dict: Danh sách phim theo từng ngày chiếu, với ngày là khóa và danh sách phim là giá trị.
    """
    date_elements = driver.find_elements(By.CSS_SELECTOR, "li.day.cgv-onlyone")
    all_film_data = {}
    consecutive_empty_days = 0  # Đếm số ngày liên tiếp không có dữ liệu

    for date in date_elements:
        try:
            # Lấy thông tin ngày, tháng, năm
            full_date = date.get_attribute("id").replace("cgv", "")  # Định dạng YYYYMMDD
            date_obj = datetime.strptime(full_date, "%Y%m%d")
            formatted_date = date_obj.strftime("%d-%m-%Y")  # Chuyển thành dd-mm-yyyy

            print(f"📅 Đang lấy dữ liệu cho ngày: {formatted_date}")

            # Click vào ngày để load nội dung mới
            driver.execute_script("arguments[0].click();", date)

            # Chờ trang cập nhật dữ liệu mới sau khi click
            time.sleep(2)

            # Gọi hàm thu thập dữ liệu phim
            daily_film_data = extract_one_day(driver)

            if not daily_film_data:
                consecutive_empty_days += 1
                print(f"⚠️ Ngày {formatted_date} không có dữ liệu. Số ngày trống liên tiếp: {consecutive_empty_days}")

                # Nếu 3 ngày liên tiếp không có dữ liệu, dừng chương trình
                if consecutive_empty_days >= 3:
                    print("❌ Đã gặp 3 ngày liên tiếp không có dữ liệu, dừng chương trình.")
                    break
            else:
                all_film_data[formatted_date] = daily_film_data
                consecutive_empty_days = 0  # Reset bộ đếm khi có dữ liệu

        except Exception as e:
            print(f"❌ Lỗi khi lấy dữ liệu ngày {formatted_date}: {e}")

    return all_film_data
