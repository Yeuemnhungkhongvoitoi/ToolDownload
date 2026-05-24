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
                                              
           >> CHIẾN BINH ROOT TERMUX <<
{RESET}"""
    print(banner)

def kiem_tra_root():
    if os.getuid() != 0:
        print(f"{RED}[!] Công cụ yêu cầu quyền ROOT. Vui lòng chạy bằng lệnh 'tsu' hoặc 'su' trước.{RESET}")
        sys.exit(1)

def lay_id_gofile(url):
    match = re.search(r"gofile\.io/d/([a-zA-Z0-9]+)", url)
    if match:
        return match.group(1)
    return None

def lay_token_gofile():
    try:
        response = requests.post("https://api.gofile.io/accounts").json()
        if response.get("status") == "ok":
            return response["data"]["token"]
    except Exception as e:
        print(f"{RED}[!] Không thể tạo session với GoFile: {e}{RESET}")
    return None

def tai_va_cai_dat(gofile_url):
    folder_id = lay_id_gofile(gofile_url)
    if not folder_id:
        print(f"{RED}[!] Đường link GoFile không hợp lệ!{RESET}")
        return

    print(f"{YELLOW}[*] Đang kết nối tới GoFile...{RESET}")
    token = lay_token_gofile()
    if not token:
        return

    try:
        url_api = f"https://api.gofile.io/contents/{folder_id}?wt={token}"
        response = requests.get(url_api).json()
        
        if response.get("status") != "ok":
            print(f"{RED}[!] Không tìm thấy thư mục hoặc thư mục bị lỗi!{RESET}")
            return
        
        children = response["data"]["children"]
        files = [children[f_id] for f_id in children if children[f_id]["type"] == "file"]
        
        if not files:
            print(f"{YELLOW}[!] Thư mục trống hoặc không chứa file hợp lệ.{RESET}")
            return
        
        print(f"{GREEN}[✓] Tìm thấy {len(files)} file trong thư mục.{RESET}")
        
        # Chọn số lượng file muốn tải
        try:
            so_luong = input(f"{YELLOW}[?] Nhập số lượng file muốn tải (Bấm Enter để tải tất cả): {RESET}")
            if so_luong.strip() == "":
                so_luong_tai = len(files)
            else:
                so_luong_tai = min(int(so_luong), len(files))
        except ValueError:
            print(f"{RED}[!] Số lượng không hợp lệ. Tiến hành tải toàn bộ.{RESET}")
            so_luong_tai = len(files)

        # Tiến hành tải
        for i in range(so_luong_tai):
            file_info = files[i]
            file_name = file_info["name"]
            download_url = file_info["link"]
            
            print(f"\n{CYAN}[{i+1}/{so_luong_tai}] Đang tải: {file_name}...{RESET}")
            
            headers = {"Cookie": f"accountToken={token}"}
            file_data = requests.get(download_url, headers=headers, stream=True)
            
            with open(file_name, "wb") as f:
                for chunk in file_data.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"{GREEN}[✓] Đã tải xong: {file_name}{RESET}")
            
            # Tự động cài đặt nếu là file APK
            if file_name.endswith(".apk"):
                print(f"{YELLOW}[*] Phát hiện file APK. Đang tự động cài đặt bằng quyền ROOT...{RESET}")
                duong_dan_file = os.path.abspath(file_name)
                # Thực thi lệnh cài đặt hệ thống ẩn
                ket_qua = os.system(f"pm install -r '{duong_dan_file}'")
                
                if ket_qua == 0:
                    print(f"{GREEN}[✓] Cài đặt thành công {file_name}!{RESET}")
                    # Xoá file apk sau khi cài xong để sạch máy (tùy chọn)
                    os.remove(duong_dan_file)
                else:
                    print(f"{RED}[!] Cài đặt thất bại. Lỗi hệ thống pm.{RESET}")
            else:
                print(f"{YELLOW}[-] File không phải định dạng APK, bỏ qua bước cài đặt.{RESET}")

    except Exception as e:
        print(f"{RED}[!] Có lỗi xảy ra trong quá trình xử lý: {e}{RESET}")

def hien_thi_menu():
    while True:
        xoa_man_hinh()
        hien_thi_banner()
        print(f"{BOLD}--- DANH SÁCH MENU ---{RESET}")
        print(f"{CYAN}[1]{RESET} Auto tải và cài đặt APK từ GoFile")
        print(f"{CYAN}[2]{RESET} Kiểm tra trạng thái Root")
        print(f"{CYAN}[0]{RESET} Thoát công cụ")
        print("-" * 30)
        
        lua_chon = input(f"{YELLOW}Nhập lựa chọn của bạn: {RESET}")
        
        if lua_chon == "1":
            link = input(f"{YELLOW}Nhập link GoFile (VD: https://gofile.io/d/xxxxx): {RESET}")
            tai_va_cai_dat(link.strip())
            input(f"\n{GREEN}Nhấn Enter để quay lại Menu...{RESET}")
        elif lua_chon == "2":
            if os.getuid() == 0:
                print(f"{GREEN}[✓] Thiết bị đã được Root và Termux đang có quyền tối cao!{RESET}")
            else:
                print(f"{RED}[!] Chưa có quyền Root!{RESET}")
            input(f"\n{GREEN}Nhấn Enter để quay lại Menu...{RESET}")
        elif lua_chon == "0":
            print(f"{CYAN}Cảm ơn bạn đã sử dụng JPA TOOL. Tạm biệt!{RESET}")
            break
        else:
            print(f"{RED}[!] Lựa chọn không hợp lệ!{RESET}")
            input(f"\n{GREEN}Nhấn Enter để thử lại...{RESET}")

if __name__ == "__main__":
    kiem_tra_root()
    hien_thi_menu()
    
