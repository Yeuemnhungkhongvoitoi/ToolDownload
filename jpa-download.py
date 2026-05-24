import requests
import os
import sys
import subprocess
from tqdm import tqdm

def print_banner():
    # Banner JPA TOOL
    print("   _________  ___    _____ _____  _____ _     ")
    print("  |_  | ___ \\/ _ \\  |_   _|  _  ||  _  | |    ")
    print("    | | |_/ / /_\\ \\   | | | | | || | | | |    ")
    print("    | |  __/|  _  |   | | | | | || | | | |    ")
    print("/\\__/ / |   | | | |   | | \\ \\_/ /\\ \\_/ / |____")
    print("\\____/\\_|   \\_| |_/   \\_/  \\___/  \\___/\\_____/")

def install_apk(file_path):
    print(f"[*] Đang cài đặt: {os.path.basename(file_path)}...")
    result = subprocess.run(['pm', 'install', '-r', file_path], capture_output=True, text=True)
    if result.returncode == 0:
        print("[✓] Cài đặt thành công!")
    else:
        print(f"[!] Cài đặt thất bại: {result.stderr}")

def download_and_install(file_info):
    file_link = file_info['link']
    filename = file_info['name']
    save_path = f"/sdcard/Download/{filename}"
    
    print(f"[!] Đang tải: {filename}")
    r = requests.get(file_link, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    
    with open(save_path, 'wb') as f:
        with tqdm(total=total_size, unit='iB', unit_scale=True) as bar:
            for data in r.iter_content(chunk_size=1024):
                size = f.write(data)
                bar.update(size)
    
    print(f"\n[✓] Đã tải xong: {save_path}")
    
    if filename.lower().endswith('.apk'):
        install_apk(save_path)

import re

def download_gofile():
    url = input("\n[+] Nhập link trang Gofile: ").strip()
    headers = {
        "User-Agent": "Mozilla/5.0 (Android 10; Mobile; rv:86.0) Gecko/86.0 Firefox/86.0"
    }
    
    print("[*] Đang kết nối tới Gofile...")
    try:
        # Lấy nội dung trang web
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("[!] Không thể truy cập link, kiểm tra lại kết nối!")
            return

        # Tìm kiếm link tải trực tiếp trong mã HTML bằng Regular Expression
        # Link tải Gofile thường nằm trong các thẻ json hoặc thuộc tính link
        pattern = r'"link":"(https://[^"]+)"'
        direct_links = re.findall(pattern, response.text)
        
        # Lọc các link trùng lặp
        direct_links = list(set(direct_links))
        
        if not direct_links:
            print("[!] Không tìm thấy file trong link này. Có thể link đã hết hạn hoặc riêng tư.")
            return

        print(f"[!] Tìm thấy {len(direct_links)} file.")
        num_to_download = int(input(f"[?] Nhập số lượng file muốn tải (1-{min(10, len(direct_links))}): "))
        num_to_download = max(1, min(num_to_download, 10, len(direct_links)))

        for i in range(num_to_download):
            link = direct_links[i].replace("\\/", "/") # Sửa lỗi định dạng link của Gofile
            filename = link.split('/')[-1].split('?')[0] # Lấy tên file
            
            print(f"\n--- Đang tải file {i+1}: {filename} ---")
            download_and_install_direct(link, filename) # Gọi hàm tải trực tiếp

    except Exception as e:
        print(f"[!] Lỗi hệ thống: {e}")

def download_and_install_direct(file_link, filename):
    save_path = f"/sdcard/Download/{filename}"
    r = requests.get(file_link, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    
    with open(save_path, 'wb') as f:
        with tqdm(total=total_size, unit='iB', unit_scale=True) as bar:
            for data in r.iter_content(chunk_size=1024):
                size = f.write(data)
                bar.update(size)
    
    print(f"\n[✓] Xong: {save_path}")
    if filename.lower().endswith('.apk'):
        install_apk(save_path)

def main():
    while True:
        os.system('clear')
        print_banner()
        print("[ 1 ] Tải và cài đặt tự động từ Gofile")
        print("[ 0 ] Thoát")
        
        choice = input("\n[?] Chọn chức năng (Nhập số): ")
        
        if choice == '1':
            download_gofile()
            input("\nNhấn Enter để quay lại menu...")
        elif choice == '0':
            sys.exit()
        else:
            print("[!] Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
    