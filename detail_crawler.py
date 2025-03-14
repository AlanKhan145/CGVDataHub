import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def get_value_by_label(driver, label):
    """Hàm giả định để lấy giá trị dựa trên nhãn."""
    try:
        element = driver.find_element(By.XPATH, f"//label[contains(text(), '{label}')]/following-sibling::div")
        return element.text.strip()
    except Exception:
        return None

def extract_film_details(url):
    """Trích xuất thông tin chi tiết của một bộ phim từ trang riêng."""
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
        time.sleep(2)  # Chờ trang tải

        try:
            title_element = mini_driver.find_element(By.CSS_SELECTOR, "div.product-name span.h1")
            film_info_detail["title"] = title_element.text.strip()
        except Exception:
            pass

        film_info_detail["genre"] = get_value_by_label(mini_driver, "Thể loại")
        film_info_detail["duration"] = get_value_by_label(mini_driver, "Thời lượng")
        film_info_detail["release_date"] = get_value_by_label(mini_driver, "Khởi chiếu")
        film_info_detail["director"] = get_value_by_label(mini_driver, "Đạo diễn")
        film_info_detail["language"] = get_value_by_label(mini_driver, "Ngôn ngữ")
        film_info_detail["rated"] = get_value_by_label(mini_driver, "Rated")

        actors_text = get_value_by_label(mini_driver, "Diễn viên") or get_value_by_label(mini_driver, "Diễn viên chính")
        film_info_detail["actors"] = actors_text if actors_text else "Không có thông tin"

        try:
            description_element = mini_driver.find_element(By.CSS_SELECTOR, "meta[name='description']")
            film_info_detail["description"] = description_element.get_attribute("content").strip()
        except Exception:
            film_info_detail["description"] = None

        # Lấy các định dạng công nghệ phim
        try:
            technology_elements = mini_driver.find_elements(By.CSS_SELECTOR, "div.movie-technology-icons a.movie-detail-icon-type span")
            film_info_detail["technologies"] = [tech.text.strip() for tech in technology_elements if tech.text.strip()]
        except Exception:
            film_info_detail["technologies"] = []

    except Exception as e:
        print(f"Lỗi khi lấy thông tin phim từ {url}: {e}")

    finally:
        mini_driver.quit()

    return film_info_detail

url = "https://www.cgv.vn/default/mickey17.html"
film_info_detail = extract_film_details(url)
print(film_info_detail)