import requests
import time
from requests.auth import HTTPBasicAuth


requests.packages.urllib3.disable_warnings()


# function to get IP or FQDN from dnac.config
def get_DNAC_IP():
    with open("config/dnac.config", "r") as file:
        for line in file.read().split("\n"):
            if "#" not in line and line:
                DNAC_IP = line.split("=")
    return DNAC_IP[1].strip()


class DNAC:

    # constructor
    def __init__(self):
        self.token = ""
        self.host = get_DNAC_IP()
        # username and password initialize empty and then shall took values from login screen
        self.username = ""
        self.password = ""
        self.commands = []
        self.devices = []
        self.device_json = {}
        self.task_info = {}

    # function to get authentication token
    def get_auth_token(self):
        url = "https://" + self.host + "/dna/system/api/v1/auth/token"
        req = requests.post(
            url, auth=HTTPBasicAuth(self.username, self.password), verify=False
        )
        self.token = req.json()["Token"]

    # function to get list of devices
    def get_device_list(self):
        url = "https://" + self.host + "/api/v1/network-device"
        hdr = {"x-auth-token": self.token, "content-type": "application/json"}
        resp = requests.get(url, headers=hdr, verify=False)
        self.device_json = resp.json()

    # function that gets the device ID
    def get_UUID(self, ip):
        url = (
            "https://"
            + self.host
            + f"/dna/intent/api/v1/network-device/ip-address/{ip}"
        )
        hdr = {"x-auth-token": self.token, "content-type": "application/json"}
        response = requests.get(url, headers=hdr, verify=False)
        self.task_info[response.json()["response"]["hostname"]] = {}

        return (
            response.json()["response"]["id"],
            response.json()["response"]["hostname"],
        )

    # function that checks if the task is finished
    def wait_on_task(self, url):
        finished = True
        headers = {"x-auth-token": self.token}
        tries = 0
        while (finished) and (tries < 5):
            time.sleep(1)
            response = requests.get(url, headers=headers, verify=False)
            tries += 1
            finished = response.json()["response"]["isError"]
        return response

    # function that creates a task with the command and device
    def get_task_id(self, name, args, ips):
        self.commands = args
        self.devices = ips
        url = (
            "https://"
            + self.host
            + "/dna/intent/api/v1/network-device-poller/cli/read-request"
        )
        hdr = {"x-auth-token": self.token}

        for ip in self.devices:
            uuid, hostname = self.get_UUID(ip)
            payload = {"commands": self.commands, "name": name, "deviceUuids": [uuid]}

            response = requests.post(url, headers=hdr, verify=False, json=payload)

            self.task_info[hostname][
                response.json()["response"]["taskId"]
            ] = f"https://{self.host}{response.json()['response']['url']}"

    # function that get the output of a finished task
    def get_task_results(self, file_id):

        url = "https://" + self.host + f"/dna/intent/api/v1/file/{file_id}"
        hdr = {"x-auth-token": self.token, "content-type": "application/json"}
        response = requests.get(url, headers=hdr, verify=False)
        return response.json()
