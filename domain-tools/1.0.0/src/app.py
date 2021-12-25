import requests
import ssl, socket
from urllib.parse import urlparse
import json
import datetime
from walkoff_app_sdk.app_base import AppBase

def formatGMTime(timestamp):
    GMT_FORMAT = '%b %d %H:%M:%S %Y GMT'
    a = datetime.datetime.strptime(timestamp, GMT_FORMAT) + datetime.timedelta(hours=8)
    return str(a)
class DomainTools(AppBase):
    __version__ = "1.0.0"
    app_name = "domain tools"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def get_cert_info(self, url):
        if "https://" in url:
            domain = urlparse(url).netloc
            hostname = domain
        else:
            hostname = url
        print(hostname)
        c = ssl.create_default_context()
        s = c.wrap_socket(socket.socket(), server_hostname=hostname)
        s.connect((hostname, 443))
        cert = s.getpeercert()
        cert['notBefore'] = formatGMTime(cert.get('notBefore'))
        cert['notAfter'] = formatGMTime(cert.get('notAfter'))
        subjectAltName = s.getpeercert().get('subjectAltName')
        list = []
        for i in subjectAltName:
            list.append(i[1])
        cert['subjectAltName'] = list
        j = json.dumps(cert)
        return j

    def get_ip_list(self, domain):  # 获取域名解析出的IP列表
        ip_list = []
        try:
            addrs = socket.getaddrinfo(domain, None)
            for item in addrs:
                if item[4][0] not in ip_list:
                    ip_list.append(item[4][0])
        except Exception as e:
            # print(str(e))
            pass
        return ip_list

# Run the actual thing after we've checked params

def run(request):
    action = request.get_json()
    authorization_key = action.get("authorization")
    current_execution_id = action.get("execution_id")

    if action and "name" in action and "app_name" in action:
        DomainTools.run(action)
        return f'Attempting to execute function {action["name"]} in app {action["app_name"]}'
    else:
        return f'Invalid action'
if __name__ == "__main__":
    DomainTools.run()
