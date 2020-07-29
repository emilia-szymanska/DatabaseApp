from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from AccountSettingsScreen import AccountSettingsScreen

class AdminScreen(Screen):
    lendtakebtn = ObjectProperty(Button)
    settingbtn  = ObjectProperty(Button)
    givebackbtn = ObjectProperty(Button)
    searchbtn   = ObjectProperty(Button)
    usermgbtn   = ObjectProperty(Button)
    gearmgbtn   = ObjectProperty(Button)

    def GetToSettings(self):
        app = App.get_running_app()
        screen = app.root.get_screen("ustawienia konta")
        screen.UpdateData(app.root.login)
        Window.size = (400, 360)
        app.root.current = "ustawienia konta"

    def GetToMgUsers(self):
        app = App.get_running_app()
        screen = app.root.get_screen("wybierz uzytkownika")
        screen.UpdateData()
        Window.size = (400, 360)
        app.root.current = "wybierz uzytkownika"

    def GetToMgEqp(self):
        app = App.get_running_app()
        screen = app.root.get_screen("zarzadzaj sprzetem")
        screen.UpdateData()
        Window.size = (900, 600)
        app.root.current = "zarzadzaj sprzetem"

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

    def GetToBrowseOrders(self):
        app = App.get_running_app()
        Window.size = (400, 150)
        app.root.current = "wybor typu zamowienia przegladanie"

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