#!/env python3

import customtkinter
import time
import os

from classes.class_login import Login
from classes.class_window import Program
from classes.class_dnac import DNAC
from CTkMessagebox import CTkMessagebox


# class Tk -> CTk -> Login -> App_Login (inheritance)
class App_Login(Login):

    # constructor include login window and object DNAC
    def __init__(self):
        super().__init__()
        self.server = DNAC()

    # overwrite check_credentials method from Login class
    def check_credentials(self):

        # takes input credentials and try to get a token from DNAC Server
        self.server.username = self.txt_username.get()
        self.server.password = self.txt_password.get()
        try:
            self.server.get_auth_token()
            self.frame.destroy()
            self.destroy()
            # if token is correctly retrieved, main windows is open
            manage_main_window(self.server)
        except Exception:
            # if token fails login window resets
            self.txt_username.delete(0, customtkinter.END)
            self.txt_password.delete(0, customtkinter.END)
            self.lbl_error.place(relx=0.5, rely=0.65, anchor=customtkinter.CENTER)
            self.txt_username.focus()


# functions that manages object DNAC and main windows


# clear textbox from list_devices
def clear_screen(main_window, server):
    main_window.textbox_list_devices.delete("0.0", "end")
    server.device_json = {}


# export list of devices to .csv file
def export_to_csv(server):
    if server.device_json:
        created_succesfully = False
        timestamp = time.localtime()
        file_unique_name = f"exports/devices-{timestamp.tm_mday}-{timestamp.tm_mon}-{timestamp.tm_year}_{timestamp.tm_hour}-{timestamp.tm_min}.csv"
        with open(file_unique_name, "w") as file:
            file.write(
                "{0};{1};{2};{3};{4};{5};{6};\n".format(
                    "HOSTNAME",
                    "MGMT IP",
                    "S/N",
                    "MODEL",
                    "SW VERSION",
                    "ROLE",
                    "UPTIME",
                )
            )

            for device in server.device_json["response"]:
                uptime = "N/A" if device["upTime"] is None else device["upTime"]
                if device["serialNumber"] is not None and "," in device["serialNumber"]:
                    serialPlatformList = zip(
                        device["serialNumber"].split(","),
                        device["platformId"].split(","),
                    )
                else:
                    serialPlatformList = [
                        (device["serialNumber"], device["platformId"])
                    ]
                for serialNumber, platformId in serialPlatformList:
                    file.write(
                        "{0};{1};{2};{3};{4};{5};{6};\n".format(
                            device["hostname"],
                            device["managementIpAddress"],
                            serialNumber.strip(),
                            platformId.strip(),
                            device["softwareVersion"],
                            device["role"],
                            uptime,
                        )
                    )
            if os.path.getsize(file_unique_name) > 0:
                created_succesfully = True
        if created_succesfully:
            CTkMessagebox(
                message=f"CSV file succesfuly created!\nNAME: {file_unique_name}",
                icon="check",
                option_1="Close",
            )
        else:
            CTkMessagebox(
                title="Error",
                message="CSV file could not be created!",
                icon="cancel",
                option_1="Close",
            )
    else:
        CTkMessagebox(
            title="Error",
            message="There are no devices in buffer,\nplease click Try to fetch them.",
            icon="cancel",
            option_1="Close",
        )


# print list of devices to textbox
def print_device_list(main_window, server):
    server.device_json = {}
    server.get_device_list()
    main_window.textbox_list_devices.delete("0.0", "end")
    if server.device_json:
        main_window.textbox_list_devices.insert(
            "0.0",
            "{0:42}\t\t\t\t{1:18}\t\t{2:14}\t\t{3:18}\t\t\t{4:12}\t\t{5:16}\t\t{6:15}\n".format(
                "HOSTNAME",
                "MGMT IP",
                "S/N",
                "MODEL",
                "SW VERSION",
                "ROLE",
                "UPTIME",
            ),
        )
        for device in server.device_json["response"]:
            uptime = "N/A" if device["upTime"] is None else device["upTime"]
            if device["serialNumber"] is not None and "," in device["serialNumber"]:
                serialPlatformList = zip(
                    device["serialNumber"].split(","), device["platformId"].split(",")
                )
            else:
                serialPlatformList = [(device["serialNumber"], device["platformId"])]
            for serialNumber, platformId in serialPlatformList:
                main_window.textbox_list_devices.insert(
                    "end",
                    "{0:42}\t\t\t\t{1:18}\t\t{2:14}\t\t{3:18}\t\t\t{4:12}\t\t{5:16}\t\t{6:15}\n".format(
                        device["hostname"],
                        device["managementIpAddress"],
                        serialNumber.strip(),
                        platformId.strip(),
                        device["softwareVersion"],
                        device["role"],
                        uptime,
                    ),
                )


# get hosts with switch toogle to on
def get_active_hosts(main_window):
    active_hosts = []
    for device, name in main_window.switches.items():
        if device.get() == 1:
            active_hosts.append(name)
    return active_hosts


# print results of command in devices to textbox on frame_ex_commands
def print_results(main_window, server):

    server.task_info = {}

    commands = main_window.entry_commands.get()
    active_hosts = get_active_hosts(main_window)

    if commands and active_hosts:

        main_window.textbox_ex_commands.delete("0.0", "end")

        if "," in commands:
            commands_list = commands.replace(", ", ",").split(",")
        else:
            commands_list = []
            commands_list.append(commands.strip())

        timestamp = time.localtime()
        task_unique_name = f"Task-{timestamp.tm_mday}-{timestamp.tm_mon}-{timestamp.tm_year}_{timestamp.tm_hour}-{timestamp.tm_min}-{timestamp.tm_sec}"

        server.get_task_id(task_unique_name, commands_list, active_hosts)

        for hostname, task_data in server.task_info.items():

            main_window.textbox_ex_commands.insert(
                "end",
                f"\n[+]  Task initiated with ID: {list(task_data.keys())[0]}",
                "3",
            )

            task_response = server.wait_on_task(list(task_data.values())[0])

            if task_response.json()["response"]["isError"]:
                main_window.textbox_ex_commands.insert(
                    "end", "\n[!] Task failed...\n", "1"
                )
            else:
                main_window.textbox_ex_commands.insert(
                    "end",
                    "\n[+] Task completed succesfuly...\n",
                    "2",
                )
                main_window.textbox_ex_commands.insert(
                    "end", f"\n[+] HOSTNAME: {hostname}\n", "1"
                )
                results = server.get_task_results(
                    task_response.json()["response"]["progress"]
                    .split(":")[-1]
                    .strip("}")
                    .strip('"')
                )

                main_window.textbox_ex_commands.insert("end", "\n[+] RESULTS:", "0")

                for command in server.commands:
                    data = results[0]["commandResponses"]["SUCCESS"][command]
                    main_window.textbox_ex_commands.insert("end", f"\n{data}\n", "4")

    else:
        CTkMessagebox(
            title="Error",
            message="There are no selected devices or\nno commands entered. ",
            icon="cancel",
            option_1="Close",
        )
        main_window.entry_commands.focus()


# export results to txt file
def export_results(main_window):

    timestamp = time.localtime()
    file_unique_name = f"exports/results-{timestamp.tm_mday}-{timestamp.tm_mon}-{timestamp.tm_year}_{timestamp.tm_hour}-{timestamp.tm_min}.txt"

    text_to_export = main_window.textbox_ex_commands.get("0.0", "end")

    if text_to_export.strip() != "":

        with open(file_unique_name, "w") as file:
            file.write(text_to_export)
        if os.path.getsize(file_unique_name) > 0:
            CTkMessagebox(
                message=f"File succesfuly created!\nNAME: {file_unique_name}",
                icon="check",
                option_1="Close",
            )

    else:
        CTkMessagebox(
            title="Error",
            message="There is nothing to export. ",
            icon="cancel",
            option_1="Close",
        )


# configure main window events on button press and key binds
def configure_main_windows_buttons(main_window, server):
    main_window.clear_button.configure(
        command=lambda: clear_screen(main_window, server)
    )
    main_window.csv_button.configure(command=lambda: export_to_csv(server))
    main_window.try_button.configure(
        command=lambda: print_device_list(main_window, server)
    )
    main_window.try_button_cmd.configure(
        command=lambda: print_results(main_window, server)
    )
    main_window.export_button_cmd.configure(command=lambda: export_results(main_window))
    main_window.entry_commands.bind(
        "<Return>", (lambda enter: print_results(main_window, server))
    )


# configure colors on textbox ex_commands
def configure_main_windows_textbox(main_window):
    main_window.textbox_ex_commands.tag_config("1", foreground="red")
    main_window.textbox_ex_commands.tag_config("2", foreground="green")
    main_window.textbox_ex_commands.tag_config("3", foreground="orange")
    main_window.textbox_ex_commands.tag_config("4", foreground="gray")


# creates an object Program that acts as main windows, configure and runs it
def manage_main_window(server):
    main_window = Program()
    configure_main_windows_buttons(main_window, server)
    configure_main_windows_textbox(main_window)
    main_window.mainloop()


# opens login panel
if __name__ == "__main__":
    login_window = App_Login()
    login_window.mainloop()
