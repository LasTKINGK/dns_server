# DNS Server Project

This is a custom DNS server written in Python. It allows only specific domains and blocks others.

## Features
- Blocks unauthorized domains.
- Admin commands: start, stop, restart, status.
- Easy installation on Ubuntu.

## Installation
1. Clone the repository:
   //bash
 //  git clone https://github.com/yourusername/dns_server.git
 //  cd dns_server
   
   
   
   Run the installation script:

bash
Copy
chmod +x install.sh
./install.sh
Usage
Start the server:

bash
Copy
sudo systemctl start dns_server
Stop the server:

bash
Copy
sudo systemctl stop dns_server
Check status:

bash
Copy
sudo systemctl status dns_server