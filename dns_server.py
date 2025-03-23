import json
import subprocess
import socket
import sys
from dnslib import DNSRecord, QTYPE, A
from dnslib.server import DNSServer

# خواندن دامنه‌های مجاز از فایل JSON
with open("allowed_domains.json", "r") as file:
    ALLOWED_DOMAINS = json.load(file)

# وضعیت سرور
SERVER_RUNNING = True

class SimpleDNSResolver:
    def resolve(self, request, handler):
        reply = request.reply()
        qname = request.q.qname
        domain = str(qname).rstrip('.')

        if domain in ALLOWED_DOMAINS:
            # پاسخ به درخواست‌های مجاز
            reply.add_answer(
                DNSRecord(
                    qname,
                    QTYPE.A,
                    rdata=A("127.0.0.1"),  # پاسخ با IP لوکال (یا هر IP دیگر)
                    ttl=60,
                )
            )
        else:
            # عدم پاسخ به درخواست‌های غیرمجاز
            reply.header.rcode = 3  # کد خطای NXDOMAIN (دامنه وجود ندارد)

        return reply

def get_local_ip():
    # دریافت IP لوکال
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def ping_ip(ip):
    # اجرای دستور پینگ
    try:
        output = subprocess.run(["ping", "-c", "1", ip], capture_output=True, text=True)
        print(output.stdout)
    except Exception as e:
        print(f"Ping failed: {e}")

def start_server():
    global SERVER_RUNNING
    # چاپ IP سرور
    local_ip = get_local_ip()
    print(f"DNS Server IP: {local_ip}")

    # پینگ به IP سرور
    ping_ip(local_ip)

    # راه‌اندازی DNS سرور
    resolver = SimpleDNSResolver()
    server = DNSServer(resolver, port=53)

    print("DNS Server started on port 53...")
    while SERVER_RUNNING:
        server.start()

    print("DNS Server stopped.")

def stop_server():
    global SERVER_RUNNING
    SERVER_RUNNING = False
    print("Server stopped.")

def restart_server():
    global SERVER_RUNNING
    SERVER_RUNNING = True
    print("Server restarted.")

def show_status():
    print("Server is running." if SERVER_RUNNING else "Server is stopped.")

if __name__ == "__main__":
    # مدیریت آرگومان‌های خط فرمان
    if len(sys.argv) < 2:
        print("Usage: python dns_server.py <command>")
        print("Commands: start, stop, restart, status")
        sys.exit(1)

    command = sys.argv[1].lower()
    if command == "start":
        start_server()
    elif command == "stop":
        stop_server()
    elif command == "restart":
        restart_server()
    elif command == "status":
        show_status()
    else:
        print("Invalid command. Use: start, stop, restart, status")