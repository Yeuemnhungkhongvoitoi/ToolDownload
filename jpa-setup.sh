#!/data/data/com.termux/files/usr/bin/bash

echo "Đang cài đặt môi trường cho Tester..."
termux-setup-storage
pkg update && pkg upgrade -y
pkg install python git curl -y

# Cài đặt thư viện
pip install requests tqdm

# Tải script chính từ link GitHub của bạn
echo "Đang tải JPA Tester từ GitHub..."
curl -o /sdcard/Download/jpa-download.py https://raw.githubusercontent.com/Yeuemnhungkhongvoitoi/ToolDownload/refs/heads/main/jpa-download.py

echo "Cài đặt hoàn tất!"
