import customtkinter

# set initial appearance and theme
customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


class Program(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("DNAC API")
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="API Options",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame,
            command=self.deploy_frame_list_devices,
            text="List Devices",
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame,
            command=self.deploy_frame_ex_commands,
            text="Execute Command",
        )
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame,
            command=self.exit_program,
            text="Exit",
            hover_color="red",
        )
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10, sticky="s")
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w"
        )
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.change_scaling_event("100%")

        # create diferent frames
        self.frame_list_devices = customtkinter.CTkFrame(self, corner_radius=0)
        self.frame_ex_commands = customtkinter.CTkFrame(self, corner_radius=0)
        self.frame_scrollable = customtkinter.CTkScrollableFrame(
            self.frame_ex_commands, label_text="DEVICES"
        )

        # create main textboxes
        self.textbox_list_devices = customtkinter.CTkTextbox(
            master=self.frame_list_devices
        )
        self.textbox_ex_commands = customtkinter.CTkTextbox(
            master=self.frame_ex_commands
        )

        # create buttons for frame list_devices
        self.clear_button = customtkinter.CTkButton(
            master=self.frame_list_devices, text="Clear Screen", border_width=3
        )
        self.csv_button = customtkinter.CTkButton(
            master=self.frame_list_devices, text="Export to .csv", border_width=3
        )
        self.try_button = customtkinter.CTkButton(
            master=self.frame_list_devices, text="Try", border_width=3
        )

        # create entry for frame ex_commands
        self.entry_commands = customtkinter.CTkEntry(master=self.frame_ex_commands)

        # create button for frame ex_commands
        self.try_button_cmd = customtkinter.CTkButton(
            master=self.frame_ex_commands, text="Try", border_width=3, width=110
        )
        self.export_button_cmd = customtkinter.CTkButton(
            master=self.frame_ex_commands, text="Export", border_width=3, width=110
        )

        # create select all switch for scrollable frame
        self.select_all = customtkinter.CTkSwitch(
            master=self.frame_scrollable,
            text="SELECT ALL",
            command=self.change_switch_status,
        )
        self.separator_lbl = customtkinter.CTkLabel(
            master=self.frame_scrollable, text="--------------------------------------"
        )

        # variables
        self.frame_flag = ""
        self.switches = {}

    # fuction exit button
    def exit_program(self):
        self.quit()

    # change windows appearance as selected in option menu
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # change windows zoom as selected in option menu
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # function that place frame list_devices on top and place widgets
    def deploy_frame_list_devices(self):
        if self.frame_flag == "Execute_Commands":
            self.frame_list_devices.tkraise()
        self.frame_flag = "List_Devices"

        self.frame_list_devices.grid_rowconfigure(0, weight=2)
        self.frame_list_devices.grid_rowconfigure(1, weight=0)
        self.frame_list_devices.grid_columnconfigure((0, 1, 2), weight=1)

        self.frame_list_devices.grid(
            padx=20, pady=10, row=0, column=1, sticky="nsew", rowspan=3, columnspan=2
        )

        self.textbox_list_devices.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.clear_button.grid(row=1, column=0, pady=10)
        self.csv_button.grid(row=1, column=1, pady=10)
        self.try_button.grid(row=1, column=2, pady=10)

    # function that place frame ex_commands on top and place widgets
    def deploy_frame_ex_commands(self):
        if self.frame_flag == "List_Devices":
            self.frame_ex_commands.tkraise()
            self.frame_scrollable.tkraise()
        self.frame_flag = "Execute_Commands"

        self.frame_ex_commands.grid_columnconfigure(0, weight=2)
        self.frame_ex_commands.grid_columnconfigure(1, weight=0)
        self.frame_ex_commands.grid_rowconfigure(0, weight=2)
        self.frame_ex_commands.grid_rowconfigure(1, weight=0)

        self.frame_ex_commands.grid(
            padx=10, pady=10, row=0, column=1, sticky="nsew", rowspan=3
        )
        self.textbox_ex_commands.grid(
            row=0, column=0, padx=(10, 5), pady=10, sticky="nsew"
        )

        self.entry_commands.grid(
            row=1, column=0, padx=(10, 5), pady=(0, 10), sticky="ew"
        )
        self.try_button_cmd.grid(
            row=1, column=1, padx=(5, 10), pady=(0, 10), sticky="w"
        )
        self.export_button_cmd.grid(
            row=1, column=1, padx=(5, 10), pady=(0, 10), sticky="e"
        )

        self.frame_scrollable.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="ns")
        self.frame_scrollable.grid_columnconfigure(0, weight=1)

        self.select_all.grid(row=0, column=0, padx=10, pady=(0, 10))
        self.separator_lbl.grid(row=1, column=0, padx=10)

        # creates switches from content in hosts file
        with open("config/hosts", "r") as file:
            hosts = file.read().split("\n")
        i = 2
        for host in hosts:
            if host:
                switch = customtkinter.CTkSwitch(
                    master=self.frame_scrollable, text=f"{host}"
                )
                switch.grid(row=i, column=0, padx=10, pady=(0, 20))
                i += 1
                self.switches[switch] = host

        # bind mousewheel for linux
        self.frame_scrollable.bind(
            "<Button-4>",
            lambda e: self.frame_scrollable._parent_canvas.yview("scroll", -1, "units"),
        )
        self.frame_scrollable.bind(
            "<Button-5>",
            lambda e: self.frame_scrollable._parent_canvas.yview("scroll", 1, "units"),
        )

    # function that select/deselect all switches
    def change_switch_status(self):
        if self.select_all.get() == 1:
            for device in self.switches.keys():
                device.select()
        else:
            for device in self.switches.keys():
                device.deselect()
