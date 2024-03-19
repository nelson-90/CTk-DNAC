## CTk-DNAC

### Introduction

Python program with graphic interface (Custom Tkinter) to retrieve information from Cisco DNA Center.

So far it counts with two functionalities:

- List Devices
- Execute Show Commands

### Install

Clone repository and access directory

(Optional - create an environment) 

```bash
python3 -m venv venv
source venv/bin/activate
```

Install required libraries:

```bash
pip install requirements.txt
```
Access folder **config** and edit **dnac.config** file, change example IP o FQDN to your DNAC server info.

Change **hosts** file, inside write IPs of the switches that you want to possibly execute show commands.

Execute:

```bash
python main.py
```
