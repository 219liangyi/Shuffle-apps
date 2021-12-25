import time
import json
import random
import socket
import asyncio
import requests

from walkoff_app_sdk.app_base import AppBase


class Ocr(AppBase):
    __version__ = "1.0.0"
    app_name = "ocr"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def get_token(self, domain, name, password, region, project):
        url = "https://" + region + "/v3/auth/tokens"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "domain": {
                                "name": domain
                            },
                            "name": name,
                            "password": password
                        }
                    }
                },
                "scope": {
                    "project": {
                        "name": project
                    }
                }
            }
        }
        result = requests.post(url, headers=headers, json=data)
        return result.headers.get("X-Subject-Token")

    def report_image(self, domain, project_id, token, image_base64, image_url):
        url = "https://" + domain + "/v2/" + project_id + "/ocr/general-text"
        if len(image_url) != 0:
            data = {
                "url": image_url
            }
        else:
            data = {
                "image": image_base64
            }
        headers = {
            "X-Auth-Token": token
        }
        return requests.post(url, headers=headers, json=data).text

# Run the actual thing after we've checked params

def run(request):
    action = request.get_json()
    authorization_key = action.get("authorization")
    current_execution_id = action.get("execution_id")

    if action and "name" in action and "app_name" in action:
        Ocr.run(action)
        return f'Attempting to execute function {action["name"]} in app {action["app_name"]}'
    else:
        return f'Invalid action'
if __name__ == "__main__":
    Ocr.run()
