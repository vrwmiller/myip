
import requests

def get_myip_com():
    url = "https://api.myip.com"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['ip'], data['country'], data['cc']

def get_ipify(ipv6=False):
    url = "https://api64.ipify.org?format=json" if ipv6 else "https://api.ipify.org?format=json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['ip']

def main():
    ip, country, cc = get_myip_com()
    print(f"MyIP.com: {ip} ({country}, {cc})")
    ipv4 = get_ipify(ipv6=False)
    print(f"ipify IPv4: {ipv4}")
    ipv6 = get_ipify(ipv6=True)
    print(f"ipify IPv6: {ipv6}")

if __name__ == "__main__":
    main()
