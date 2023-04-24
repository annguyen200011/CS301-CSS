from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file('transaction/transaction.kv')


class TransactionWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class TransactionApp(App):
    def build(self):
        Window.size = (1280, 832)
        return TransactionWindow()
    
if __name__ == "__main__":
    tr = TransactionApp()
    tr.run()