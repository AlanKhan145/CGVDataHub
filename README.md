# CGVDataHub

## Giới thiệu
CGVDataHub là một dự án thu thập dữ liệu từ trang web CGV, tập trung vào việc crawl danh sách phim, khuyến mãi và thông tin rạp chiếu phim. Dữ liệu sau khi thu thập sẽ được trích xuất, xử lý và lưu trữ vào cơ sở dữ liệu MongoDB để phục vụ cho các ứng dụng phân tích hoặc hiển thị thông tin.

## Chức năng chính
- **Crawl dữ liệu** từ các nguồn chính thức của CGV.
- **Trích xuất thông tin chi tiết** về:
  - Danh sách phim: thể loại, đạo diễn, diễn viên, thời lượng, ngày phát hành, ngôn ngữ, mô tả, v.v.
  - Danh sách khuyến mãi: thông tin chi tiết về các ưu đãi hiện có.
  - Thông tin rạp chiếu phim: địa chỉ, hotline, hình ảnh, lịch chiếu phim.
- **Lưu trữ dữ liệu** vào hệ thống cơ sở dữ liệu MongoDB để dễ dàng truy vấn và phân tích.

## Công nghệ sử dụng
- **Jupyter Notebook**: Hỗ trợ phát triển và kiểm thử dữ liệu.
- **Python**: Ngôn ngữ lập trình chính của dự án.
- **Selenium**: Thu thập dữ liệu từ các trang web bằng trình điều khiển WebDriver.
- **MongoDB**: Lưu trữ dữ liệu phim, khuyến mãi và rạp chiếu.
- **Logging**: Theo dõi lỗi và ghi lại các hoạt động trong quá trình crawl dữ liệu.

## Cấu trúc thư mục
```
CGVDataHub/
│── config.py               # Cấu hình các thông số quan trọng (thời gian chờ, URL, v.v.)
│── crawlData.ipynb         # Notebook hỗ trợ quá trình crawl dữ liệu
│── database.py             # Xử lý lưu trữ dữ liệu vào MongoDB
│── extract_detail.py       # Trích xuất thông tin chi tiết từ trang phim
│── extract_info.py         # Tổng hợp và xử lý dữ liệu trích xuất
│── main.ipynb              # Chạy toàn bộ quá trình crawl dữ liệu
│── main.py                 # Chạy toàn bộ quá trình crawl dữ liệu dưới dạng script Python
│── requirements.txt        # Danh sách các thư viện cần cài đặt
```

## Cách cài đặt và chạy dự án

### 1. Cài đặt các thư viện cần thiết
Sử dụng lệnh sau để cài đặt tất cả các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### 2. Cài đặt Selenium WebDriver
- Đảm bảo đã cài đặt trình điều khiển WebDriver tương thích với trình duyệt Chrome.
- Nếu chưa có WebDriver, tải về tại: [ChromeDriver](https://sites.google.com/chromium.org/driver/)

### 3. Chạy chương trình
- Nếu sử dụng Jupyter Notebook, mở `main.ipynb` và chạy từng ô lệnh.
- Nếu chạy bằng script Python, sử dụng lệnh sau:
```bash
python main.py
```

## Các tính năng mới
- **Trích xuất danh sách phim**: Thu thập dữ liệu từ trang CGV và lưu vào MongoDB.
- **Trích xuất danh sách khuyến mãi**: Lấy thông tin về các chương trình ưu đãi, hình ảnh và chi tiết khuyến mãi.
- **Trích xuất thông tin rạp chiếu**: Lấy thông tin về địa chỉ, số fax, hotline, bản đồ và lịch chiếu.
- **Hỗ trợ đa thành phố**: Tự động quét danh sách thành phố, lấy dữ liệu từng rạp trong mỗi thành phố.



