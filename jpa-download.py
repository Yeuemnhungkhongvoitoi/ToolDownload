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

def download_gofile():
    url = input("\n[+] Nhập link trang Gofile: ")
    # Loại bỏ khoảng trắng hoặc ký tự thừa nếu có
    url = url.strip()
    
    # Lấy ID (đảm bảo lấy phần cuối của link)
    content_id = url.split('/')[-1]
    api_url = f"https://api.gofile.io/contents/{content_id}"
    
    # Header giả lập trình duyệt để tránh bị chặn
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print("[*] Đang kiểm tra nội dung...")
    try:
        # Thêm headers vào request
        response = requests.get(api_url, headers=headers).json()
        
        if response['status'] == 'ok':
            files_dict = response['data']['contents']
            # Chuyển thành list
            file_list = [files_dict[key] for key in files_dict]
            total_files = len(file_list)
            
            print(f"[!] Tìm thấy {total_files} file trong link.")
            # ... (phần code còn lại của bạn giữ nguyên)

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
    