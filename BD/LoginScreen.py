from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from DbAccessFunctions import Login


class LoginScreen(Screen):
    log = ObjectProperty(TextInput)
    pwd = ObjectProperty(TextInput)

    def LoginTry(self):
        app= App.get_running_app()
        rights = Login(self.log.text, self.pwd.text)
        if rights != None:
            app.root.login = self.log.text
            app.root.rig = rights
            screen = app.root.get_screen("ustawienia konta")
            screen.UpdateData(app.root.login)
        if rights == 'czlonek_kola':
            Window.size = (400, 160)
            app.root.current = 'opcje czlonka kola'
        elif rights == 'administrator':
            Window.size = (400, 360)
            app.root.current = 'opcje administratora'

    def ClearInput(self):
        self.log.text = ""
        self.pwd.text = ""