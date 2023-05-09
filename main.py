from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
<<<<<<< Updated upstream
from kivymd.uix.button import MDTextButton

=======
from kivymd.uix.button import MDFlatButton
>>>>>>> Stashed changes
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

from screen import LogInScreen
from screen import HomeScreenAdmin
from screen import HomeScreenCashier
from screen import InventoryScreen
from screen import TransactionScreen
from screen import TableItemsScreen
from screen import UpdateItemScreen
from screen import TransactionScreen
from screen import ReportScreen
from screen import EmployeeScreen
from screen import TransactionScreenCashier
from screen import InventoryScreenCashier

Window.size = (1280,832)

class MainLayout(BoxLayout):

    home_admin_widget = HomeScreenAdmin()
    login_widget = LogInScreen()
    home_cashier_widget = HomeScreenCashier()
    transaction_widget = TransactionScreen()
    transaction_cashier_widget = TransactionScreenCashier()
    inventory_widget = InventoryScreen()
    inventory_cashier_widget = InventoryScreenCashier()
    # table_items_widget = TableItemsScreen()
    # update_items_widget = UpdateItemScreen()
    report_widget = ReportScreen()
    employee_widget = EmployeeScreen()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
<<<<<<< Updated upstream
        
        self.ids.login_scrn.add_widget(self.login_widget)
        self.ids.home_scrn_admin.add_widget(self.home_admin_widget)
        self.ids.home_scrn_cashier.add_widget(self.home_cashier_widget)
        self.ids.inventory_scrn.add_widget(self.inventory_widget)
        self.ids.report_scrn.add_widget(self.report_widget)
        self.ids.employee_scrn.add_widget(self.employee_widget)
        self.ids.transaction_scrn.add_widget(self.transaction_widget)

        self.ids.transaction_scrn_cashier.add_widget(self.transaction_cashier_widget)
        self.ids.inventory_scrn_cashier.add_widget(self.inventory_cashier_widget)
=======
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
        
        self.search_bar_inventory = MDTextField(
            pos_hint={"center_x": 0.34, "center_y": 0.905},
            on_text_validate = self.search,
            size = {600,30},
            font_size = 20,
            padding="24dp",
            hint_text="Search by product Name/Category/Status",
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
        items = sorted(items, key=lambda x: x[2])
        
        conn.commit()
        conn.close()

        _dp = 30
        # delete_column = ("",dp(_dp))

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
                # delete_column,
            ],
            row_data=items,
        )

        # for i in range(len(self.data_tables.row_data)):
        #     delete_button = MDFlatButton(text="Delete")
        #     self.data_tables.get_row_items(i)[5].add_widget(delete_button)

        conn = sqlite3.connect('inventory_db.db')
        c = conn.cursor()

        self.add_widget(button_box)
        self.add_widget(self.data_tables)
        self.add_widget(self.search_bar_inventory)
    
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
        items = sorted(items, key=lambda x: x[2])
        self.data_tables.row_data = items
        
        conn.commit()
        conn.close()

    def search(self, instance):
        conn = sqlite3.connect('inventory_db.db')

        # crate a cursor
        c = conn.cursor()

        c.execute('''SELECT * FROM item WHERE product_name LIKE ? or category LIKE ? or status LIKE ?''', 
                  ['%' + self.search_bar_inventory.text + '%', '%' + self.search_bar_inventory.text + '%', '%' + self.search_bar_inventory.text + '%'])
        filters = c.fetchall()
        filters = sorted(filters, key=lambda x: x[2])
        self.data_tables.row_data = filters
        
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
                        'status': 'full',
                        # 'del': ''
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
        
        self.search_bar_employee = MDTextField(
            id = "search_bar_employee",
            on_text_validate = self.search,
            pos_hint={"center_x": 0.34, "center_y": 0.905},
            size = {600,20},
            font_size = 15,
            padding="24dp",
            hint_text="Search by Name/Role/EmployeeID",
            # fill_color = {229/255, 229/255, 229/255, 229/255}
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
        employees = sorted(employees, key=lambda x: x[1])
        
        conn.commit()
        conn.close()

        _dp = 40
        self.data_tables = MDDataTable(
            pos_hint={"center_y": 0.45, "center_x": 0.5},
            size_hint=(0.9, 0.7),
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
        self.add_widget(self.search_bar_employee)

    
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
        items = sorted(items, key=lambda x: x[1])
        self.data_tables.row_data = items
        
        conn.commit()
        conn.close()
    
    def search(self, instance):
        conn = sqlite3.connect('employee_db.db')

        # crate a cursor
        c = conn.cursor()

        c.execute('''SELECT * FROM employees WHERE name LIKE ? or role LIKE ? or employeeID LIKE ?''', 
                  ['%' + self.search_bar_employee.text + '%','%' + self.search_bar_employee.text + '%', '%' + self.search_bar_employee.text + '%'])
        filters = c.fetchall()
        filters = sorted(filters, key=lambda x: x[1])
        self.data_tables.row_data = filters
        
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


class AdminHomeLayout(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class CashierHomeLayout(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class LogInScreen(Screen):
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
                self.parent.parent.show_admin_screen()
            elif (user == 'cashier' and pwd == 'cashier'):
                self.parent.parent.show_cashier_screen()
            elif (user == 'admin' and pwd is not 'admin') or (user == 'cashier' and pwd is not 'cashier'):
                info.text = '[color=#FF0000] Invalid username and/or password [/color]'

class MainLayout(MDFloatLayout):
    screen_manager = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()
        # Add the inventory screen
        login_screen = LogInScreen(name="login")
        self.screen_manager.add_widget(login_screen)

        # Add the transaction screen
        admin_screen = AdminHomeLayout(name="home_admin")
        self.screen_manager.add_widget(admin_screen)

        # Add the report screen
        cashier_screen = CashierHomeLayout(name="home_cashier")
        self.screen_manager.add_widget(cashier_screen)

        self.add_widget(self.screen_manager)
    
    def show_admin_screen(self):
        self.screen_manager.transition.direction = "up"
        self.screen_manager.current = "home_admin"

    def show_cashier_screen(self):
        self.screen_manager.transition.direction = "up"
        self.screen_manager.current = "home_cashier"

>>>>>>> Stashed changes
        

class MainApp(MDApp):
    def build(self):
        Window.size=(1280, 832)
        return MainLayout()


if __name__ == '__main__':
    MainApp().run()