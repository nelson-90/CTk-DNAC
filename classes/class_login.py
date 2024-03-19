#!/env python3

import customtkinter
import hashlib

# set appearance and color for window
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class Login(customtkinter.CTk):

    # constructor create and position elements an windows
    def __init__(self):
        super().__init__()

        self.geometry("600x300")
        self.title("DNAC Login")

        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.lbl_username = customtkinter.CTkLabel(
            master=self.frame,
            justify=customtkinter.LEFT,
            text="USERNAME:",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.lbl_username.place(relx=0.2, rely=0.3, anchor=customtkinter.CENTER)

        self.lbl_password = customtkinter.CTkLabel(
            master=self.frame,
            justify=customtkinter.LEFT,
            text="PASSWORD:",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.lbl_password.place(relx=0.2, rely=0.5, anchor=customtkinter.CENTER)

        self.lbl_error = customtkinter.CTkLabel(
            master=self.frame,
            justify=customtkinter.CENTER,
            text="El usuario o la contraseña son incorrectos",
            text_color="red",
        )

        self.txt_username = customtkinter.CTkEntry(
            master=self.frame, justify=customtkinter.CENTER, width=280
        )
        self.txt_username.place(relx=0.7, rely=0.3, anchor=customtkinter.CENTER)
        self.txt_username.focus()

        self.txt_password = customtkinter.CTkEntry(
            master=self.frame, justify=customtkinter.CENTER, show="*", width=280
        )
        self.txt_password.place(relx=0.7, rely=0.5, anchor=customtkinter.CENTER)
        self.txt_password.bind("<Return>", (lambda enter: self.check_credentials()))

        self.btn_login = customtkinter.CTkButton(
            master=self.frame,
            text="LOGIN",
            border_width=5,
            command=self.check_credentials,
            corner_radius=10,
        )
        self.btn_login.place(relx=0.5, rely=0.8, anchor=customtkinter.CENTER)

    # function to check login panel using credentials user / password
    def check_credentials(self):
        password = "5f4dcc3b5aa765d61d8327deb882cf99"  # password = password
        user_password = hashlib.md5(self.txt_password.get().encode("utf-8")).hexdigest()
        if self.txt_username.get() == "user" and password == user_password:
            self.frame.destroy()
            self.destroy()
        else:
            self.txt_username.delete(0, customtkinter.END)
            self.txt_password.delete(0, customtkinter.END)
            self.lbl_error.place(relx=0.5, rely=0.65, anchor=customtkinter.CENTER)
            self.txt_username.focus()


# for testing as a standalone login panel
if __name__ == "__main__":
    app = Login()
    app.mainloop()
