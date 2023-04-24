from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file('home/home_admin.kv')


class HomeAdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class HomeAdminApp(App):
    def build(self):
        Window.size = (1280, 832)
        return HomeAdminWindow()
    
if __name__ == "__main__":
    ha = HomeAdminApp()
    ha.run()