from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import *
from kivy.lang import Builder
import datetime
from kivy.core.window import Window
import time

Builder.load_file('signin/signin.kv')

class SignInWindow(BoxLayout):
    date = datetime.datetime.now()
    dt_string = date.strftime("%a %d/%m/%Y %H:%M:%S")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_user(self):
        user_input = self.ids.username_field
        pwd_input = self.ids.pwd_field
        info = self.ids.info

        user = user_input.text
        pwd = pwd_input.text

        if user == '' or pwd == '':
            info.text = '[color=#FF0000] Username and/or password required [/color]'
        else:
            if (user == 'admin' and pwd == 'admin'):
                info.text = '[color=#00FF00] Log in succesfully [/color]'
                self.parent.parent.current = 'scrn_home_admin'
            elif (user == 'cashier' and pwd == 'cashier'):
                self.parent.parent.current = 'scrn_home_cashier'
            elif (user == 'admin' and pwd is not 'admin') or (user == 'cashier' and pwd is not 'cashier'):
                info.text = '[color=#FF0000] Invalid username and/or password [/color]'

class SigninApp(App):
    def build(self):
        Window.size = (1280, 832)
        return SignInWindow()
    
if __name__ == "__main__":
    sa = SigninApp()
    sa.run()