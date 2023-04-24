from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from signin.signin import SignInWindow
from home.home_admin import HomeAdminWindow
from home.home_cashier import HomeCashierWindow
from transaction.transaction import TransactionWindow

class MainWindow(BoxLayout):

    signin_widget = SignInWindow()
    home_admin_widget = HomeAdminWindow()
    home_cashier_widget = HomeCashierWindow()
    transaction_widget = TransactionWindow()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_home_admin.add_widget(self.home_admin_widget)
        self.ids.scrn_home_cashier.add_widget(self.home_cashier_widget)
        self.ids.scrn_transaction.add_widget(self.transaction_widget)

class MainApp(App):
    def build(self):
        Window.size=(1280, 832)
        return MainWindow()
    
if __name__ == '__main__':
    MainApp().run()