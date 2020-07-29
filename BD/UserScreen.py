from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from AccountSettingsScreen import AccountSettingsScreen

class UserScreen(Screen):
    lendtakebtn = ObjectProperty(Button)
    settingbtn = ObjectProperty(Button)
    givebackbtn = ObjectProperty(Button)
    searchbtn = ObjectProperty(Button)

    def GetToSettings(self):
        app = App.get_running_app()
        screen = app.root.get_screen("ustawienia konta")
        screen.UpdateData(app.root.login)
        Window.size = (400, 360)
        app.root.current = "ustawienia konta"
    
    def LogOut(self):
        app = App.get_running_app()
        screen = app.root.get_screen("ekran logowania")
        screen.ClearInput()
        Window.size = (300, 160)
        app.root.current = "ekran logowania"
        app.root.login = ""
        app.root.rig = ""
    
    def GetToBrowseEqp(self):
        app = App.get_running_app()
        screen = app.root.get_screen("przegladaj sprzet")
        screen.UpdateData()
        Window.size = (500, 600)
        app.root.current = "przegladaj sprzet"

    def GetToReturnEqp(self):
        app = App.get_running_app()
        screen = app.root.get_screen("oddaj sprzet")
        screen.UpdateData()
        Window.size = (500, 600)
        app.root.current = "oddaj sprzet"

    def GetToMakeOrder(self):
        app = App.get_running_app()
        Window.size = (400, 150)
        app.root.current = "wybor typu zamowienia"

