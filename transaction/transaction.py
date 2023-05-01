from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.icon_definitions import md_icons
from kivy.core.text import LabelBase
from kivy.uix.widget import Widget

class MyWidget(Widget):
    def build(self):
        # Load the Balsamiq Sans font from the file
        LabelBase.register(
            name='BalsamiqSans',
            fn_regular='fonts/BalsamiqSans-Regular.ttf',
            fn_bold='fonts/BalsamiqSans-Bold.ttf',
            fn_italic='fonts/BalsamiqSans-Italic.ttf',
            fn_bolditalic='fonts/BalsamiqSans-BoldItalic.ttf'
        )

class TransactionWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class TransactionApp(MDApp):
    def build(self):
        return TransactionWindow()
    
if __name__ =="__main__":
    oa = TransactionApp()
    oa.run()
