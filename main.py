from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.lang import Builder
import numpy as np
import datetime
import sqlite3

Builder.load_file('main.kv')
Window.size = (1280,832)

class InventoryScreen(Screen):
    data_tables = None
    items = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.8, "center_y": 0.905},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )

        for button_text in ["Delete Selected Item(s)", "Create New"]:
            button_box.add_widget(
                MDRaisedButton(
                    text=button_text, on_release=self.on_button_press
                )
            )

        # Add the inventory screen

        self.search_bar_inventory = MDTextField(
            id = "search_bar_inventory",
            on_text_validate = self.search,
            pos_hint={"center_x": 0.33, "center_y": 0.905},
            size = {580,20},
            font_size = 15,
            padding="24dp",
            hint_text="Search by product Category/Name/Status",
            # fill_color = {229/255, 229/255, 229/255, 229/255}
        )
        

        # Connect sqlite3
        conn = sqlite3.connect('inventory_db.db')
        c = conn.cursor()

        # Create a table
        c.execute("""CREATE TABLE if not exists item (
            product_id integer,
            category text,
            product_name text,
            quantity_left integer,
            unit_price real,
            status text)
            """)
        c.execute("SELECT * FROM item")
        self.items = c.fetchall()
        
        conn.commit()
        conn.close()

        _dp = 25
        self.data_tables = MDDataTable(
            pos_hint={"center_y": 0.45, "center_x": 0.5},
            size_hint=(0.95, 0.8),
            use_pagination=True,
            rows_num = 10,
            pagination_menu_pos = 'top',
            column_data=[
                ("ID", dp(_dp)),
                ("Category", dp(_dp)),
                ("Product Name", dp(_dp)),
                ("Quantity Left", dp(_dp)),
                ("Unit Price", dp(_dp)),
                ("Status", dp(_dp)),
            ],
            # row_data=sorted(self.items, key=lambda x: x[2]),
            row_data = self.items,
            check = True,
        )

        self.add_widget(button_box)
        self.add_widget(self.data_tables)
        self.add_widget(self.search_bar_inventory)
    
    def on_button_press(self, instance_button: MDRaisedButton) -> None:
        '''Called when a control button is clicked.'''

        try:
            {   "Delete Selected Item(s)": self.remove_item,
                "Create New": self.parent.parent.show_update_screen,

            }[instance_button.text]()
        except KeyError:
            pass

    def update_items(self):
        #create database or connect to one
        conn = sqlite3.connect('inventory_db.db')

        # crate a cursor
        c = conn.cursor()

        c.execute("SELECT * FROM item")
        self.items = c.fetchall()
        
        self.data_tables.row_data = self.items
        self.data_tables.row_data = sorted(self.items, key=lambda x: x[2])
        
        conn.commit()
        conn.close()

    def search(self, instance):
        conn = sqlite3.connect('inventory_db.db')

        # crate a cursor
        c = conn.cursor()

        c.execute('''SELECT * FROM item WHERE product_name LIKE ? or category LIKE ? or status LIKE ?''', 
                  ['%' + self.search_bar_inventory.text + '%', '%' + self.search_bar_inventory.text + '%', '%' + self.search_bar_inventory.text + '%'])
        filters = c.fetchall()
        
        self.data_tables.row_data = filters
        self.data_tables.row_data = sorted(filters, key=lambda x: x[2])
        
        conn.commit()
        conn.close()
    
    def remove_item(self):
        # remove item from the list
        checked = self.data_tables.get_row_checks()
        print(checked)

        conn = sqlite3.connect('inventory_db.db')
        c = conn.cursor()
        for item in checked:
            c.execute('DELETE FROM item WHERE product_name = ?', (item[1],))

        conn.commit()
        conn.close()

        self.update_items()
        
class UpdateItemScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def confirm(self):
        if self.ids.product_name.text == "" or self.ids.product_quantity.text == "" or self.ids.product_price.text == "" or self.ids.product_category.text == "" :
            pass
        else:
            conn = sqlite3.connect('inventory_db.db')

            c = conn.cursor()

            c.execute("SELECT * FROM item")
            items = c.fetchall()

            c.execute("INSERT INTO item VALUES (:product_id, :category, :name, :quantity, :price, :status)",
                    {
                        'product_id': len(items) + 1,
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

class TransactionTable(MDBoxLayout):
    data_table = None
    items = []
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        _dp = 35
        self.orientation = 'vertical'
        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.5, "center_y": 0.9},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )
        input_search = MDTextField(
            id = "search_item",
            # on_text_validate = self.search,
            pos_hint={"center_x": 0.5, "center_y": 0.9},
            size = {600,20},
            font_size = 15,
            padding="24dp",
            hint_text="Search by product Category/Name/Status",
            # fill_color = {229/255, 229/255, 229/255, 229/255}
        )

        button_box.add_widget(input_search)
        for button_text in ["Add Item", "Remove"]:
            button_box.add_widget(
                MDRaisedButton(
                    text=button_text, on_release=self.on_button_press
                )
            )

        self.data_tables = MDDataTable(
            size_hint=(0.95, 0.95),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            use_pagination=True,
            rows_num = 10,
            pagination_menu_pos = 'top',
            check=True,
            column_data=[
                ("Item ID", dp(_dp)),
                ("Item Name", dp(_dp)),
                ("Quantity", dp(_dp)),
                ("Unit Item Price", dp(_dp)),
                ("Final Item Price", dp(_dp)),
            ],
            row_data=self.items,
        )

        bottom = MDBoxLayout(orientation = 'vertical', size_hint_y = None, height = 120)
        bottom.add_widget(Label(text = "Payment method ", size_hint_y = None, height = 40, color = (0,0,0,1)))
        price_layout = MDBoxLayout(orientation = 'horizontal', size_hint_y = None, height = 40)
        price_layout.add_widget(MDTextField(size_hint_x = None, 
                                   width = 200, 
                                   hint_text = "Money Gave"))
        price_layout.add_widget(Label(text = "Money Return: ", size_hint_y = None, height = 40, color = (0,0,0,1)))
        bottom.add_widget(price_layout)

        self.add_widget(button_box)
        self.add_widget(self.data_tables)
        self.add_widget(bottom)


    def on_button_press(self, instance_button: MDRaisedButton) -> None:
        try:
            {
                "Add Item": self.add_item,
                "Remove": self.remove_item,
            }[instance_button.text]()
        except KeyError:
            pass
    
    def update_price(self):
        #update price
        price = 0
        for i in range(len(self.items)):
            price += int(self.items[i][4])
        #print(self.parent.children[0].children)
        self.parent.children[0].children[1].text = str(price) + ' $'
    
    def update_table(self):
        #update table info
        self.data_tables.row_data = self.items
        self.update_price()
    
    
    def add_item(self):
        #print(self.children[2].children[2].text)
        input_text = self.children[2].children[2].text
        if input_text != '':
            #check if item is already in the list
            have_item = -1
            for i in range(len(self.items)):
                if input_text == self.items[i][0]:
                    have_item = i
                    
            if have_item != -1:
                new_quantity = int(self.items[have_item][2]) + 1
                new_item = [self.items[have_item][0], self.items[have_item][1], 
                            str(new_quantity), self.items[have_item][3], 
                            str(new_quantity * int(self.items[have_item][3]))]
                self.items.pop(have_item)
                self.items.append(new_item)
                self.children[2].children[2].text = ''
                self.update_table()
                return 
            
            #if item is not in the list
            quantity = np.random.randint(1, 10)
            unit_price = np.random.randint(20, 100)
            item_price = quantity * unit_price
            self.items.append([str(input_text), "Item" , str(quantity) , str(unit_price), str(item_price)])
            self.data_tables.row_data = self.items
            self.children[2].children[2].text = ''
            self.update_price()


    def remove_item(self):
        #remove item from the list
        checked = self.data_tables.get_row_checks()
        print(checked)
        new_item = []
        for i in range(len(self.data_tables.row_data)):
            if self.data_tables.row_data[i] not in checked:
                new_item.append(self.data_tables.row_data[i])

        self.items = new_item
        self.data_tables.row_data = self.items
        self.update_price()



class TransactionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        

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
            check = True,
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

        

class MainApp(MDApp):
    def build(self):
        Window.size=(1280, 832)
        return MainLayout()
        


if __name__ == '__main__':
    MainApp().run()