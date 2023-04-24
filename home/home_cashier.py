from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file('home/home_cashier.kv')


class HomeCashierWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class HomeCashierApp(App):
    def build(self):
        Window.size = (1280, 832)
        return HomeCashierWindow()
    
if __name__ == "__main__":
    ha = HomeCashierApp()
    ha.run()