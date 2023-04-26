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
        
        self.ids.login_scrn.add_widget(self.login_widget)
        self.ids.home_scrn_admin.add_widget(self.home_admin_widget)
        self.ids.home_scrn_cashier.add_widget(self.home_cashier_widget)
        self.ids.inventory_scrn.add_widget(self.inventory_widget)
        self.ids.report_scrn.add_widget(self.report_widget)
        self.ids.employee_scrn.add_widget(self.employee_widget)
        self.ids.transaction_scrn.add_widget(self.transaction_widget)

        self.ids.transaction_scrn_cashier.add_widget(self.transaction_cashier_widget)
        self.ids.inventory_scrn_cashier.add_widget(self.inventory_cashier_widget)
        

class MainApp(MDApp):
    def build(self):
        Window.size=(1280, 832)
        return MainLayout()


if __name__ == '__main__':
    MainApp().run()