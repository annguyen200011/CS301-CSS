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

Builder.load_file('inventory_and_employee.kv')
Window.size = (1280,832)

class InventoryScreen(Screen):
    data_tables = None
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

        # Add the inventory screen
        

        # Connect sqlite3
        #create database or connect to one
        conn = sqlite3.connect('inventory_db.db')

        # crate a cursor
        c = conn.cursor()

        # Create a table
        c.execute("""CREATE TABLE if not exists item (
            category text,
            product_name text,
            quantity_left integer,
            unit_price real,
            status text)
            """)
        c.execute("SELECT * FROM item")
        items = c.fetchall()
        
        conn.commit()
        conn.close()

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
            row_data=items,
        )

        self.add_widget(button_box)
        self.add_widget(self.data_tables)

    
    def on_button_press(self, instance_button: MDRaisedButton) -> None:
        '''Called when a control button is clicked.'''

        try:
            {
                "Update": self.parent.parent.show_update_screen,

            }[instance_button.text]()
        except KeyError:
            pass

    def update_items(self):
        #create database or connect to one
        conn = sqlite3.connect('inventory_db.db')

        # crate a cursor
        c = conn.cursor()

        c.execute("SELECT * FROM item")
        items = c.fetchall()
        self.data_tables.row_data = items
        
        conn.commit()
        conn.close()
        
class UpdateItemScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def confirm(self):
        if self.ids.product_name.text == "" or self.ids.product_quantity.text == "" or self.ids.product_price.text == "" or self.ids.product_category.text == "" :
            pass
        else:
            conn = sqlite3.connect('inventory_db.db')

            c = conn.cursor()

            c.execute("INSERT INTO item VALUES (:category, :name, :quantity, :price, :status)",
                    {
                        'category': self.ids.product_category.text,
                        'name': self.ids.product_name.text,
                        'quantity': self.ids.product_quantity.text,
                        'price': self.ids.product_price.text,
                        'status': 'full'
                    }
                    )

            self.ids.product_category.text = ""
            self.ids.product_name.text = ""
            self.ids.product_quantity.text = ""
            self.ids.product_price.text = ""
        
            conn.commit()   
            conn.close()

            self.parent.parent.screen_manager.get_screen("inventory").update_items()
            self.parent.parent.show_inventory_screen()
            
    def cancel(self):
        self.ids.product_category.text = ""
        self.ids.product_name.text = ""
        self.ids.product_quantity.text = ""
        self.ids.product_price.text = ""

        self.parent.parent.show_inventory_screen()

class TransactionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Transaction Screen", color=(0,0,0,1)))

class ReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Report Screen", color=(0,0,0,1)))

class EmployeeScreen(Screen):
    data_tables = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.8, "center_y": 0.9},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )

        for button_text in ["Search and Filter", "Create New"]:
            button_box.add_widget(
                MDRaisedButton(
                    text=button_text, on_release=self.on_button_press
                )
            )

        # Add the inventory screen
        

        # Connect sqlite3
        #create database or connect to one
        conn = sqlite3.connect('employee_db.db')

        # crate a cursor
        c = conn.cursor()

        # Create a table
        c.execute("""CREATE TABLE if not exists employees (
            employeeID integer,
            name text,
            role text)
            """)
        c.execute("SELECT * FROM employees")
        employees = c.fetchall()
        
        conn.commit()
        conn.close()

        _dp = 30
        self.data_tables = MDDataTable(
            pos_hint={"center_y": 0.45, "center_x": 0.5},
            size_hint=(0.6, 0.6),
            use_pagination=True,
            rows_num = 10,
            pagination_menu_pos = 'top',
            column_data=[
                ("Employee ID", dp(_dp)),
                ("Name", dp(_dp)),
                ("Role", dp(_dp))
            ],
            row_data=employees,
        )

        self.add_widget(button_box)
        self.add_widget(self.data_tables)

    
    def on_button_press(self, instance_button: MDRaisedButton) -> None:
        '''Called when a control button is clicked.'''

        try:
            {
                "Create New": self.parent.parent.show_create_employee_screen,

            }[instance_button.text]()
        except KeyError:
            pass

    def update_items(self):
        #create database or connect to one
        conn = sqlite3.connect('employee_db.db')

        # crate a cursor
        c = conn.cursor()

        c.execute("SELECT * FROM employees")
        items = c.fetchall()
        self.data_tables.row_data = items
        
        conn.commit()
        conn.close()
        
class CreateEmployeeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def confirm(self):
        if self.ids.employee_name.text == "" or self.ids.employee_role.text ==  "" :
            pass
        else:
            conn = sqlite3.connect('employee_db.db')

            c = conn.cursor()

            c.execute("SELECT * FROM employees")
            employees = c.fetchall()

            c.execute("INSERT INTO employees VALUES (:employeeID, :name, :role)",
                    {
                        'employeeID': len(employees) + 1,
                        'name': self.ids.employee_name.text,
                        'role': self.ids.employee_role.text
                    }
                    )

            self.ids.employee_role.text = ""
            self.ids.employee_name.text = ""

        
            conn.commit()   
            conn.close()

            self.parent.parent.screen_manager.get_screen("employee").update_items()
            self.parent.parent.show_employee_screen()
            
    def cancel(self):
        self.ids.employee_role.text = ""
        self.ids.employee_name.text = ""

        self.parent.parent.show_employee_screen()

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
        employee_screen = EmployeeScreen(name="employee")
        self.screen_manager.add_widget(employee_screen)

        # Add the items in inventory screen
        updateItem_screen = UpdateItemScreen(name="updateItem")
        self.screen_manager.add_widget(updateItem_screen)   

        # Add new employee  screen
        createEmployee_screen = CreateEmployeeScreen(name="createEmployee")
        self.screen_manager.add_widget(createEmployee_screen)   


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
    
    def show_update_screen(self):
        self.screen_manager.transition.direction = "up"
        self.screen_manager.current = "updateItem"

    def show_create_employee_screen(self):
        self.screen_manager.transition.direction = "up"
        self.screen_manager.current = "createEmployee"

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