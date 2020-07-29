from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from kivy.uix.dropdown import DropDown
from kivy.properties import StringProperty
from kivy.uix.recycleview import RecycleView


from LoginScreen import LoginScreen
from AccountSettingsScreen import AccountSettingsScreen
from UserScreen import UserScreen
from AdminScreen import AdminScreen 
from ChooseUserScreen import ChooseUserScreen
from ManageEquipScreen import ManageEquipScreen
from BrowseEquipScreen import BrowseEquipScreen
from BrowseOrdersScreen import ChooseTypeOrderBrowseScreen
from GiveBackEquipScreen import GiveBackEquipScreen
from MakeOrderScreen import ChooseTypeOrderScreen

class MyScreenManager(ScreenManager):
    login = StringProperty('')
    rig = StringProperty('')


class BDApp(App):
    def build(self):
        return MyScreenManager(transition = NoTransition())


if __name__ == "__main__":
    Window.size = (300, 160)
    BDApp().run()