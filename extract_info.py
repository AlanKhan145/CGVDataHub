import time
from selenium.webdriver.common.by import By
from extract_detail import *
from database import *
from config import *

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from typing import Dict, Any, Optional
from pymongo.collection import Collection
# Thiết lập logging
logging.basicConfig(level=logging.INFO)


def extract_film_info(driver: webdriver.Chrome, url: str, films_col: Collection) -> None:
    """
    Trích xuất danh sách phim từ trang web và lưu vào cơ sở dữ liệu.

    Args:
        driver (webdriver.Chrome): Đối tượng trình điều khiển Selenium.
        url (str): Đường dẫn trang web cần lấy thông tin phim.
        films_col (Collection): Đối tượng cơ sở dữ liệu MongoDB để lưu trữ thông tin phim.
    """
    try:
        driver.get(url)
        time.sleep(WAIT_TIME)

        films = driver.find_elements(By.CLASS_NAME, "film-lists.item.last")
        for film in films:
            try:
                link_element = film.find_element(By.CSS_SELECTOR, "a.product-image")
                link_url = link_element.get_attribute("href")

                img_element = film.find_element(By.CSS_SELECTOR, "a.product-image img")
                poster = img_element.get_attribute("src")

                film_info_detail: Dict[str, Any] = extract_film_details(link_url)

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
                    "rated": film_info_detail.get("rated"),
                    "technologies": film_info_detail.get("technologies"),
                }
                save_to_database(films_col, film_info)

            except NoSuchElementException as e:
                logging.warning(f"Lỗi phần tử không tồn tại: {e}")
            except WebDriverException as e:
                logging.error(f"Lỗi Selenium: {e}")

    except WebDriverException as e:
        logging.error(f"Lỗi khi tải trang {url}: {e}")


def extract_newoffer_info(driver: webdriver.Chrome, url: str, newoffer_col: Collection) -> None:
    """
    Trích xuất danh sách khuyến mãi từ trang web và lưu vào cơ sở dữ liệu.

    Args:
        driver (webdriver.Chrome): Đối tượng trình điều khiển Selenium.
        url (str): Đường dẫn trang web cần lấy thông tin khuyến mãi.
        newoffer_col (Collection): Đối tượng cơ sở dữ liệu để lưu trữ thông tin khuyến mãi.
    """
    driver.get(url)
    time.sleep(WAIT_TIME)  # Chờ trang tải hoàn tất

    newoffers = driver.find_elements(
        By.CSS_SELECTOR,
        "ul.cate-new-offer.products-grid.products-grid--max-4-col.first.last.odd li"
    )

    for newoffer in newoffers:
        try:
            link_element = newoffer.find_element(By.CSS_SELECTOR, "a.aw-blog-read-more")
            link_url = link_element.get_attribute("href")

            release_day_element = newoffer.find_element(
                By.CSS_SELECTOR, "div.format-new-offer.release-day-new-offer h4"
            )
            release_day = release_day_element.text.strip()

            newoffer_info_detail = extract_newoffer_details(link_url)

            newoffer_info = {
                "link": link_url,
                "release_day": release_day,
                "title": newoffer_info_detail["title"],
                "image": newoffer_info_detail["image"],
                "promotion_details": newoffer_info_detail["promotion_details"],
            }

            save_to_database(newoffer_col, newoffer_info)
        except Exception as e:
            print(f"Lỗi khi trích xuất khuyến mãi: {e}")


def extract_theater_info(driver: webdriver.Chrome) -> Optional[Dict[str, Any]]:
    """
    Trích xuất thông tin rạp chiếu phim từ trang web.

    Args:
        driver (WebDriver): Đối tượng trình điều khiển Selenium.

    Returns:
        dict | None: Thông tin rạp chiếu phim nếu thành công, None nếu có lỗi.
    """
    try:
        title_element = driver.find_element(By.CLASS_NAME, "page-title.theater-title")
        title = title_element.find_element(By.TAG_NAME, "h3").text.strip()

        theater_info = driver.find_element(By.CLASS_NAME, "theater-infomation")
        address = theater_info.find_element(By.CLASS_NAME, "theater-address").text
        fax = theater_info.find_element(By.CSS_SELECTOR, ".fax .fax-input").text
        hotline = theater_info.find_element(By.CSS_SELECTOR, ".hotline .fax-input").text
        map_link = theater_info.find_element(By.CSS_SELECTOR, ".location a").get_attribute("href")

        theater_images = driver.find_element(By.CLASS_NAME, "theater-thumb-image")
        img_elements = theater_images.find_elements(By.TAG_NAME, "img")
        image_urls = [img.get_attribute("src") for img in img_elements]

        film_schedule = extract_all_days(driver)

        return {
            "title": title,
            "address": address,
            "fax": fax,
            "hotline": hotline,
            "map_link": map_link,
            "image_urls": image_urls,
            "film_schedule": film_schedule,
        }
    except Exception as e:
        print(f"❌ Lỗi khi trích xuất thông tin rạp: {e}")
        return None

def extract_all_theaters_info(driver, url, theaters_col):
    """
    Thu thập thông tin tất cả các rạp phim từ trang web.

    Args:
        driver (webdriver): Đối tượng trình duyệt Selenium WebDriver.
        url (str): URL của trang web cần thu thập dữ liệu.
        theaters_col (collection): Đối tượng cơ sở dữ liệu để lưu trữ thông tin rạp.

    Returns:
        None
    """
    try:
        driver.get(url)
        time.sleep(WAIT_TIME)  # Chờ trang tải xong, có thể thay bằng WebDriverWait nếu cần

        # Tìm tất cả các thành phố có thể chọn
        city_elements = driver.find_elements(By.CSS_SELECTOR, "span[id^='cgv_city_']")
        city_ids = [city.get_attribute("id") for city in city_elements]

        for city_id in city_ids:
            try:
                # Khởi động lại driver bằng cách làm mới trang thay vì tạo driver mới
                driver.refresh()
                time.sleep(WAIT_TIME)

                city_element = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, city_id))
                )
                driver.execute_script("arguments[0].click();", city_element)
                print(f"🌆 Đang thu thập dữ liệu cho thành phố: {city_element.text.strip()}")
                time.sleep(5)

                # Lấy danh sách rạp sau khi chọn thành phố
                theater_elements = driver.find_elements(By.CSS_SELECTOR, "span[id^='cgv_site_']")
                theater_ids = [theater.get_attribute("id") for theater in theater_elements if theater.is_displayed()]

                print("📌 Danh sách rạp có thể thu thập:", theater_ids)

                for theater_id in theater_ids:
                    try:
                        theater_element = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.ID, theater_id))
                        )
                        driver.execute_script("arguments[0].click();", theater_element)
                        print(f"✅ Đang thu thập dữ liệu từ rạp: {theater_id}")
                        time.sleep(WAIT_TIME)

                        # Gọi hàm thu thập dữ liệu rạp
                        try:
                            theater_info = extract_theater_info(driver)
                        except Exception as e:
                            driver.refresh()
                            theater_info = extract_theater_info(driver)
                        finally:
                            if theater_info:
                                save_to_database(theaters_col, theater_info)
                                print(f"💾 Dữ liệu từ {theater_id} đã được lưu.")

                    except Exception as e:
                        print(f"⚠️ Lỗi khi thu thập dữ liệu từ rạp {theater_id}: {e}")

            except Exception as e:
                print(f"⚠️ Lỗi khi xử lý thành phố {city_id}: {e}")

    except Exception as e:
        print(f"🚨 Lỗi khi truy cập URL {url}: {e}")
    finally:
        driver.quit()
