from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from DbAccessFunctions import GetUserData
from DbAccessFunctions import Login
from DbAccessFunctions import GetUsersNamesLogins
from DbAccessFunctions import DeleteUser
from DbAccessFunctions import UserBasicData
from DbAccessFunctions import GetDepartments
from DbAccessFunctions import GetRights
from DbAccessFunctions import AddNewUser
from DbAccessFunctions import IsLoginUnique

from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior


        
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass

class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableLabel, self).on_touch_down(touch):
          return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        rv.ChosenElement = self

class UserList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(UserList, self).__init__(**kwargs)
        usrdata = GetUsersNamesLogins()
        self.data=[{'text':x[0],'UserLogin':x[1]} for x in usrdata]

class ChooseUserScreen(Screen):
    bckbtn = ObjectProperty(Button)
    delbtn = ObjectProperty(Button)
    modbtn = ObjectProperty(Button)
    addbtn = ObjectProperty(Button)
    usrlst = ObjectProperty(UserList)
    

    def __init__(self,**kwargs):
        super(ChooseUserScreen, self).__init__(**kwargs)

    def UpdateData(self):
        usrdata = GetUsersNamesLogins()
        self.usrlst.data=[{'text':x[0],'UserLogin':x[1]} for x in usrdata]
        self.usrlst.refresh_from_data()
    
    def GetToMod(self):
        app = App.get_running_app()
        login = self.usrlst.data[self.usrlst.ChosenElement.index]['UserLogin']
        screen = app.root.get_screen("ustawienia konta")
        screen.UpdateData(login)
        Window.size = (400, 360)
        app.root.current = "ustawienia konta"

 #       ChosenLogin = self.usrlst.data[self.usrlst.ChosenElement.index]['UserLogin']


    def GetBack(self):
        app = App.get_running_app()
        Window.size = (400, 360)
        app.root.current = "opcje administratora"
    
    def GetToAdd(self):
        app = App.get_running_app()
        Window.size = (400, 360)
        app.root.current = "dodaj uzytkownika"

    def GetToDel(self):
        app = App.get_running_app()
        login = self.usrlst.data[self.usrlst.ChosenElement.index]['UserLogin']
        screen = app.root.get_screen("usun uzytkownika")
        screen.UpdateData(login)
        Window.size = (600, 120)
        app.root.current = "usun uzytkownika"

class DeleteUserScreen(Screen):
    nobtn = ObjectProperty(Button)
    yesbtn = ObjectProperty(Button)
    userlogin = StringProperty('')
    usrcont = ObjectProperty(Label)
    
    def __init__(self,**kwargs):
        super(DeleteUserScreen, self).__init__(**kwargs)

    def UpdateData(self, login):
        self.userlogin = login
        self.usrcont.text = UserBasicData(login)
  
    def SubmitDeletion(self):
        app = App.get_running_app()
        DeleteUser(app.root.login, self.userlogin)
        screen = app.root.get_screen("wybierz uzytkownika")
        screen.UpdateData()
        Window.size = (400, 360)
        app.root.current = "wybierz uzytkownika"

    def GetBack(self):
        app = App.get_running_app()
        Window.size = (400, 360)
        app.root.current = "wybierz uzytkownika"

class AddUserScreen(Screen):
    newname = ObjectProperty(TextInput)
    newsname = ObjectProperty(TextInput)
    newlogin = ObjectProperty(TextInput)
    newpwd = ObjectProperty(TextInput)
    newpwd2 = ObjectProperty(TextInput)
    confbtn = ObjectProperty(Button)
    bckbtn = ObjectProperty(Button)
    departments = ListProperty([])
    rights = ListProperty([])

    def __init__(self,**kwargs):
        super(AddUserScreen, self).__init__(**kwargs)
        self.UpdateData()

    def GetBack(self):
        app = App.get_running_app()
        screen = app.root.get_screen("wybierz uzytkownika")
        screen.UpdateData()
        Window.size = (400, 360)
        app.root.current = "wybierz uzytkownika"
        self.ClearInput()
    
    def SubmitNewUsr(self):
        app = App.get_running_app()
        if(self.newpwd.text == self.newpwd2.text and len(self.newlogin.text) >= 6 and len(self.newpwd.text) >= 6 and len(self.newname.text) >= 3 and IsLoginUnique(self.newlogin.text) == True and len(self.newname.text) >= 3):
            if(self.newname.text!='' and self.newsname.text != '' and self.newlogin.text != '' and self.depsel.text != "wybierz dzial" and self.rigsel.text != "wybierz uprawnienia"):
                AddNewUser(app.root.login, self.newname.text, self.newsname.text, self.newlogin.text, self.newpwd.text, self.depsel.text, self.rigsel.text)
                screen = app.root.get_screen("wybierz uzytkownika")
                screen.UpdateData()
                Window.size = (400, 360)
                app.root.current = "wybierz uzytkownika"
                self.ClearInput()
                self.UpdateData()

    def ClearInput(self):
        self.newname.text = ""
        self.newsname.text = "" 
        self.newlogin.text = "" 
        self.newpwd.text = ""
        self.newpwd2.text = ""
        self.ids.depsel.text = "Wybierz dzial"
        self.ids.rigsel.text = "Wybierz uprawnienia"

    def UpdateData(self):
        self.departments = GetDepartments()
        self.rights = GetRights()
