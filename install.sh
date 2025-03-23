#!/bin/bash

# به روزرسانی سیستم
echo "Updating system..."
sudo apt-get update -y

# نصب Python و pip
echo "Installing Python and pip..."
sudo apt-get install python3 python3-pip -y

# نصب وابستگی‌های Python
echo "Installing Python dependencies..."
pip3 install dnslib

# ایجاد دایرکتوری پروژه
echo "Setting up project directory..."
mkdir -p /opt/dns_server
cp dns_server.py /opt/dns_server/
cp allowed_domains.json /opt/dns_server/

# ایجاد سرویس systemd برای مدیریت سرور
echo "Creating systemd service..."
sudo bash -c 'cat > /etc/systemd/system/dns_server.service <<EOF
[Unit]
Description=DNS Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/dns_server/dns_server.py start
WorkingDirectory=/opt/dns_server
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF'

# بارگذاری و فعال‌سازی سرویس
echo "Reloading systemd and enabling service..."
sudo systemctl daemon-reload
sudo systemctl enable dns_server
sudo systemctl start dns_server

# نمایش وضعیت سرویس
echo "Checking service status..."
sudo systemctl status dns_server

echo "Installation completed successfully!"