from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.lang import Builder
import sqlite3

Builder.load_file('test2.kv')
Window.size = (1280,832)


class InventoryScreen(Screen):
    screen_manager = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.8, "center_y": 0.9},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )

        for button_text in ["Search and Filter", "Update"]:
            button_box.add_widget(
                MDRaisedButton(
                    text=button_text, on_release=self.on_button_press
                )
            )

        self.screen_manager = ScreenManager()
        # Add the inventory screen
        table_screen = TableItemsScreen(name="table")
        self.screen_manager.add_widget(table_screen)

        # Add the transaction screen
        update_screen = UpdateItemScreen(name="update")
        self.screen_manager.add_widget(update_screen)

        self.add_widget(button_box)
        self.add_widget(self.screen_manager)
    
    def on_button_press(self, instance_button: MDRaisedButton) -> None:
        '''Called when a control button is clicked.'''

        try:
            {
                "Update": self.show_update_screen,

            }[instance_button.text]()
        except KeyError:
            pass

    def show_table_screen(self):
        self.screen_manager.transition.direction = "right"
        self.screen_manager.current = "table"

    def show_update_screen(self):
        self.screen_manager.transition.direction = "left"
        self.screen_manager.current = "update"

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
        self.add_widget(Label(text="Transaction Screen", color=(0,0,0,1)))

class ReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Report Screen", color=(0,0,0,1)))

class EmployeeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Employee Screen", color=(0,0,0,1)))

class ScreenLayout(MDBoxLayout):
    screen_manager = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()
        # Add the inventory screen
        inventory_screen = InventoryScreen(name="inventory")
        self.screen_manager.add_widget(inventory_screen)

        # Add the transaction screen
        transaction_screen = TransactionScreen(name="transaction")
        self.screen_manager.add_widget(transaction_screen)

        # Add the report screen
        report_screen = ReportScreen(name="report")
        self.screen_manager.add_widget(report_screen)

        # Add the employee screen
        employee_screen = ReportScreen(name="employee")
        self.screen_manager.add_widget(employee_screen)

        # Add the employee screen
        updateItem_screen = ReportScreen(name="updateItem")
        self.screen_manager.add_widget(updateItem_screen)     
        self.add_widget(self.screen_manager)
    

    def show_inventory_screen(self):
        self.screen_manager.transition.direction = "right"
        self.screen_manager.current = "inventory"

    def show_transaction_screen(self):
        self.screen_manager.transition.direction = "left"
        self.screen_manager.current = "transaction"

    def show_report_screen(self):
        self.screen_manager.transition.direction = "left"
        self.screen_manager.current = "report"

    def show_employee_screen(self):
        self.screen_manager.transition.direction = "up"
        self.screen_manager.current = "employee"
    
    def show_update_item_screen(self):
        self.screen_manager.transition.direction = "up"
        self.screen_manager.current = "updateItem"

class MainLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = "BlueGray"
        return MainLayout()


if __name__ == '__main__':
    MainApp().run()