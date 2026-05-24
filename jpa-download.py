#!/usr/bin/env python3
import os
import sys
import re
import requests

# Màu sắc ANSI
CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Header chuẩn giả lập trình duyệt Chrome trên Android (Termux) để qua mặt bộ lọc GoFile
HEADERS_CHUAN = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Origin": "https://gofile.io",
    "Referer": "https://gofile.io/",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}

def xoa_man_hinh():
    os.system('clear')

def hien_thi_banner():
    banner = f"""{CYAN}{BOLD}
   ___  ______  ___   _____ _____ _____ _     
  |_  | | ___ \/ _ \ |_   _|  _  |  _  | |    
    | | | |_/ / /_\ \  | | | | | | | | | |    
    | | |  __/|  _  |  | | | | | | | | | |    
/\__/ / | |   | | | |  | | \ \_/ /\ \_/ / |____
\____/  \_|   \_| |_/  \_/  \___/  \___/\_____/
                                              
           >> TESTER <<
{RESET}"""
    print(banner)

def kiem_tra_root():
    if os.getuid() != 0:
        print(f"{RED}[!] Công cụ yêu cầu quyền ROOT. Vui lòng chạy bằng lệnh 'tsu' hoặc 'su' trước.{RESET}")
        sys.exit(1)

def lay_id_gofile(url):
    match = re.search(r"gofile\.io/d/([a-zA-Z0-9\-]+)", url)
    if match:
        return match.group(1)
    return None

def lay_token_gofile():
    try:
        # Tạo tài khoản guest kèm headers trình duyệt
        response = requests.post("https://api.gofile.io/accounts", headers=HEADERS_CHUAN).json()
        if response.get("status") == "ok":
            return response["data"]["token"]
        else:
            print(f"{RED}[!] Không thể lấy Token: {response}{RESET}")
    except Exception as e:
        print(f"{RED}[!] Lỗi kết nối API lấy Token: {e}{RESET}")
    return None

def tai_va_cai_dat(gofile_url):
    folder_id = lay_id_gofile(gofile_url)
    if not folder_id:
        print(f"{RED}[!] Đường link GoFile không đúng định dạng!{RESET}")
        return

    print(f"{YELLOW}[*] Đang khởi tạo session bảo mật với GoFile...{RESET}")
    token = lay_token_gofile()
    if not token:
        return

    try:
        # Cấu hình header riêng cho thư mục cần tải
        headers = HEADERS_CHUAN.copy()
        headers["Referer"] = f"https://gofile.io/d/{folder_id}"
        headers["Authorization"] = f"Bearer {token}"  # Gửi token qua quyền Bearer mã hóa

        url_api = f"https://api.gofile.io/contents/{folder_id}?wt={token}"
        response = requests.get(url_api, headers=headers).json()
        
        # Nếu GoFile trả về lỗi, in hẳn chi tiết lỗi ra màn hình để debug
        if response.get("status") != "ok":
            print(f"{RED}[!] Lỗi từ GoFile: Thư mục không tồn tại hoặc bị chặn hệ thống!{RESET}")
            print(f"{YELLOW}[*] Chi tiết phản hồi phản hồi: {response}{RESET}")
            return
        
        data = response.get("data", {})
        children = data.get("children", {})
        
        # Xử lý danh sách file từ cấu trúc JSON của GoFile
        files = []
        if isinstance(children, dict):
            files = [children[f_id] for f_id in children if children[f_id].get("type") == "file"]
        elif isinstance(children, list):
            files = [f for f in children if f.get("type") == "file"]
            
        if not files:
            print(f"{YELLOW}[!] Thư mục này trống hoặc không chứa tệp tin nào hợp lệ.{RESET}")
            return
        
        print(f"{GREEN}[✓] Kết nối thành công! Tìm thấy {len(files)} file.{RESET}")
        
        # Chọn số lượng file muốn tải
        try:
            so_luong = input(f"{YELLOW}[?] Nhập số lượng file muốn tải (Bấm Enter để tải tất cả): {RESET}")
            if so_luong.strip() == "":
                so_luong_tai = len(files)
            else:
                so_luong_tai = min(int(so_luong), len(files))
        except ValueError:
            print(f"{RED}[!] Nhập sai định dạng số. Tiến hành tải toàn bộ.{RESET}")
            so_luong_tai = len(files)

        # Tiến hành tải và cài đặt
        for i in range(so_luong_tai):
            file_info = files[i]
            file_name = file_info["name"]
            download_url = file_info["link"]
            
            print(f"\n{CYAN}[{i+1}/{so_luong_tai}] Đang tải: {file_name}...{RESET}")
            
            # Khi tải file cũng cần truyền Cookie token
            download_headers = HEADERS_CHUAN.copy()
            download_headers["Cookie"] = f"
            
