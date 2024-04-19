
import socket
import uuid

import requests
import netifaces as ni

from ..app_holder import logger_ as logger


class Worker:

    def __init__(self) -> None:
        self.__id = uuid.uuid4().hex

    def register(self):
        logger.info(f'try to register worker to scheduler, id: {self.__id}')  
        try:
            response = requests.post(
                'http://localhost:8080/schedule',
                json={
                    'addr': f'127.0.0.1:{5000}',
                    'id': self.__id,
                },
                timeout=30
            )
            
            if response.status_code != 200:
                logger.info(response.text)  
                logger.error(f'register worker to scheduler failed, id: {self.__id}')
            else:
                logger.info(f'register worker to schedule success, id: {self.__id}')  
        except Exception as e:
            logger.error(f'register worker to scheduler failed, id: {self.__id}', e)
    
    def unregister(self):
        logger.info(f'try to unregister worker to scheduler, id: {self.__id}')  
        try:
            response = requests.delete(
                f'http://localhost:8080/schedule/{self.__id}',
                timeout=30
            )
            if response.status_code != 200:
                logger.info(response.text)  
                logger.error(f'unregister worker to scheduler failed, id: {self.__id}')
            else:
                logger.info(f'unregister worker to schedule success, id: {self.__id}')  
        except Exception as e:
            logger.error(e)

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
    
