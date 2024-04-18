
import socket

import requests
import netifaces as ni


class Worker:

    def register(self):
        requests.post(
            'http://localhost:8080/schedule',
            json={
                'addr': f'127.0.0.1:{5000}',
                'name': 'worker',
                'hostname': socket.gethostname(),
                'status': 'online'
            }
        )

    def __get_host_ip(self):
        ip_addresses = []
        # 获取所有网络接口的列表
        for interface in ni.interfaces():
            # 获取接口的详细信息
            interface_details = ni.ifaddresses(interface)
            # 仅考虑IPv4配置
            ipv4_info = interface_details.get(ni.AF_INET)
            if ipv4_info:
                for item in ipv4_info:
                    ip_address = item.get('addr')
                    if ip_address and ip_address != '127.0.0.1':
                        ip_addresses.append(ip_address)
        return ip_addresses[0]
