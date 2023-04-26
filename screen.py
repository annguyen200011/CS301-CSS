from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDTextButton

from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.lang import Builder
import sqlite3
import datetime

Builder.load_file('screen.kv')
Window.size = (1280,832)

class LogInScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    date = datetime.datetime.now()
    dt_string = date.strftime("%a %d/%m/%Y %H:%M:%S")

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
                self.parent.parent.current = 'home_admin'
            elif (user == 'cashier' and pwd == 'cashier'):
                self.parent.parent.current = 'home_cashier'
            elif (user == 'admin' and pwd is not 'admin') or (user == 'cashier' and pwd is not 'cashier'):
                info.text = '[color=#FF0000] Invalid username and/or password [/color]'

class HomeScreenAdmin(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

class HomeScreenCashier(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

class InventoryScreen(Screen):
    pass
    
    # screen_manager = ObjectProperty(None)

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
        
    # button_box = MDBoxLayout(
    #     pos_hint={"center_x": 0.8, "center_y": 0.9},
    #     padding="24dp",
    #     spacing="24dp",
    # )

    # for button_text in ["Search and Filter", "Update"]:
    #     button_box.add_widget(
    #         MDRaisedButton(
    #             text=button_text, 
    #         )
    #     )

    # self.screen_manager = ScreenManager()
    # # Add the inventory screen
    # table_screen = TableItemsScreen(name="table")
    # self.screen_manager.add_widget(table_screen)

    # # Add the transaction screen
    # update_screen = UpdateItemScreen(name="update")
    # self.screen_manager.add_widget(update_screen)

    # self.add_widget(button_box)
    # self.add_widget(self.screen_manager)

    # def on_button_press(self, instance_button: Button) -> None:
    #     '''Called when a control button is clicked.'''

    #     try:
    #         {
    #             "Update": self.show_update_screen,

    #         }[instance_button.text]()
    #     except KeyError:
    #         pass
        
    # def show_table_screen(self):
    #     self.screen_manager.transition.direction = "right"
    #     self.screen_manager.current = "table"

    # def show_update_screen(self):
    #     self.screen_manager.transition.direction = "left"
    #     self.screen_manager.current = "update"

class InventoryScreenCashier(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class TableItemsScreen(Screen):
    data_tables = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create a table.
        _dp = 35
        self.data_tables = MDDataTable(
            pos_hint={"center_y": 0.45, "center_x": 0.5},
            size_hint=(0.95, 0.8),
            use_pagination=True,
            rows_num = 10,
            pagination_menu_pos = 'top',
            column_data=[
                ("Category", dp(_dp)),
                ("Product Name", dp(_dp)),
                ("Quantity Left", dp(_dp)),
                ("Unit Price", dp(_dp)),
                ("Status", dp(_dp)),
            ],
            row_data=[
                ("Cake", "Cake 1", "30,000", "100", "Full"),
                ("Cake", "Cake 2", "40,000", "100", "Medium"),
                ("Cake", "Cake 3", "40,000", "100", "Low Stock"),
            ],
        )

        # Connect sqlite3
        #create database or connect to one
        conn = sqlite3.connect('first_db.db')

        # crate a cursor
        c = conn.cursor()

        # Create a table
        c.execute("""CREATE TABLE if not exists customer (
            name text)
            """)
        
        conn.commit()
        conn.close()

        self.add_widget(self.data_tables)
    
    def confirm(self):
        if self.root.ids.product_name.text == "" or self.root.ids.product_quantity.text == "" or self.root.ids.product_price.text == "" or self.root.ids.product_category.text == "" :
            pass
        else:
            conn = sqlite3.connect('first_db.db')

            c = conn.cursor()

            c.execute("INSERT INTO customer VALUES (:first)",
                    {
                        'first': self.root.ids.word_input.text,
                    }
                    )
            
            self.root.ids.word_label.text = self.root.ids.word_input.text + " Added"

            self.root.ids.word_input.text = ''
            conn.commit()   

            conn.close()
        
class UpdateItemScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        


class TransactionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class TransactionScreenCashier(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class EmployeeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
