from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.lang import Builder
import numpy as np
import sqlite3
from kivy.uix.popup import Popup
from datetime import datetime

Builder.load_file('transaction.kv')
Window.size = (1280,832)


class TransactionTable(MDBoxLayout):
    data_table = None
    items = []
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        _dp = 50
        self.orientation = 'vertical'
        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.5, "center_y": 0.9},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )
        input_search = MDTextField(size_hint_x = None, 
                                   width = 1000, 
                                   hint_text = "Search Item",)
        input_search.id = "search_item"
        button_box.add_widget(input_search)
        for button_text in ["Add Item", "Remove"]:
            button_box.add_widget(
                MDRaisedButton(
                    text=button_text, on_release=self.on_button_press
                )
            )
        self.data_tables = MDDataTable(
            size_hint=(1, 1),
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
        price_layout.id = "cost_info"
        price_layout.add_widget(MDTextField(id="old",size_hint_x = None,         
                                   width = 200, 
                                   hint_text = "Money Gave",
                                   multiline = False,
                                   ))
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
        price = 0
        for i in range(len(self.items)):
            price += int(self.items[i][4])
        #print(self.parent.children[0].children)
        if not self.parent:
            return TransactionTable
        self.parent.children[0].children[1].text = str(price)

    #def calculate_return(self):
        #return_cash = self.root.id.old.text - price
        #global final 
        #final = str(return_cash)

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

    def reset(self):
        self.items = []
        self.update_price()

    def remove_item(self):
        checked = self.data_tables.get_row_checks()
        new_item = []
        for i in range(len(self.data_tables.row_data)):
            if self.data_tables.row_data[i] not in checked:
                new_item.append(self.data_tables.row_data[i])

        self.items = new_item
        self.data_tables.row_data = self.items
        self.update_price()

    #create popup window for the confirm button
class ConfirmPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    #resets the data table and saves transaction info into a .txt file
    def reset_and_dismiss(self):
        self.dismiss()
        with open('transaction.txt', 'a', encoding='utf-8') as file:
            file.write(str(TransactionTable().data_tables.row_data)+"\n")
        TransactionTable().reset() #Error: 'NoneType' object has no attribute children

    #Show time in the display window
class TimeLabel(Label):
    def __init__(self, **kwargs):
        super(TimeLabel, self).__init__(**kwargs)     
        self.text = "Time: "+ datetime.now().strftime(' %H:%M:%S - %a %d %b')   

class TransactionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class POSApp(MDApp):
    def build(self):
        Window.size=(1280, 832)
        return TransactionScreen()
        

if __name__ == '__main__':
    POSApp().run()