import requests
import os
import sys
import subprocess
from tqdm import tqdm

def print_banner():
    CYAN = "\033[96m"
    RESET = "\033[0m"
    print(CYAN + "   _________  ___    _____ _____  _____ _     " + RESET)
    print(CYAN + "  |_  | ___ \\/ _ \\  |_   _|  _  ||  _  | |    " + RESET)
    print(CYAN + "    | | |_/ / /_\\ \\   | | | | | || | | | |    " + RESET)
    print(CYAN + "    | |  __/|  _  |   | | | | | || | | | |    " + RESET)
    print(CYAN + "/\\__/ / |   | | | |   | | \\ \\_/ /\\ \\_/ / |____" + RESET)
    print(CYAN + "\\____/\\_|   \\_| |_/   \\_/  \\___/  \\___/\\_____/" + RESET)

def install_apk(file_path):
    print(f"[*] Đang cài đặt: {os.path.basename(file_path)}...")
    result = subprocess.run(['pm', 'install', '-r', file_path], capture_output=True, text=True)
    if result.returncode == 0:
        print("[✓] Cài đặt thành công!")
    else:
        print(f"[!] Cài đặt thất bại: {result.stderr}")

def get_gofile_data(content_id):
    # Dùng header giả lập trình duyệt Chrome
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://gofile.io/",
        "Origin": "https://gofile.io"
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    # 1. Tạo account tạm thời để lấy token
    try:
        acc = session.get("https://api.gofile.io/createAccount").json()
        token = acc["data"]["token"]
        
        # 2. Truy cập nội dung folder với token
        url = f"https://api.gofile.io/contents/{content_id}?token={token}"
        resp = session.get(url).json()
        
        if resp['status'] == 'ok':
            return resp['data']['contents']
    except Exception as e:
        print(f"[!] Lỗi kết nối API: {e}")
    return None

def download_file(file_info):
    name = file_info['name']
    link = file_info['link']
    save_path = f"/sdcard/Download/{name}"
    
    print(f"[!] Đang tải: {name}")
    try:
        # Cần thêm header khi tải file thật sự
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(link, stream=True, headers=headers)
        total_size = int(r.headers.get('content-length', 0))
        
        with open(save_path, 'wb') as f:
            with tqdm(total=total_size, unit='iB', unit_scale=True) as bar:
                for data in r.iter_content(chunk_size=1024):
                    size = f.write(data)
                    bar.update(size)
        
        print(f"\n[✓] Hoàn tất: {save_path}")
        if name.lower().endswith('.apk'):
            install_apk(save_path)
    except Exception as e:
        print(f"[!] Lỗi tải file {name}: {e}")

def main():
    while True:
        os.system('clear')
        print_banner()
        print("[ 1 ] Tải và cài đặt tự động từ Gofile")
        print("[ 0 ] Thoát")
        
        choice = input("\n[?] Chọn chức năng: ")
        if choice == '1':
            url = input("[+] Nhập link Gofile: ").strip()
            # Xử lý nếu user nhập cả URL đầy đủ
            content_id = url.split('/')[-1]
            
            files = get_gofile_data(content_id)
            if files:
                file_list = [files[key] for key in files]
                print(f"[!] Tìm thấy {len(file_list)} file.")
                num = int(input(f"[?] Số lượng muốn tải (1-{len(file_list)}): "))
                for i in range(min(num, len(file_list))):
                    download_file(file_list[i])
            else:
                print("[!] Không lấy được dữ liệu. Kiểm tra lại link hoặc kết nối!")
            input("\nNhấn Enter để quay lại menu...")
        elif choice == '0':
            sys.exit()

if __name__ == "__main__":
    main()
    
