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

from DbAccessFunctions import UsableEquipmentKind
from DbAccessFunctions import UnUsableEquipmentKind
from DbAccessFunctions import Equipment
from DbAccessFunctions import AddEqpUs
from DbAccessFunctions import AddEqpUnUs
from DbAccessFunctions import AddEqpUsKind
from DbAccessFunctions import AddEqpUnUsKind
from DbAccessFunctions import DeleteUsKind
from DbAccessFunctions import DeleteUnUsKind
from DbAccessFunctions import GetDebtUsers
from DbAccessFunctions import GetUnavailUsEqp
from DbAccessFunctions import GetUnavailUnUsEqp
from DbAccessFunctions import UnUsableEquipmentDaysKind
from DbAccessFunctions import ChangeMaxBorrow
from DbAccessFunctions import CurrentMaxBorrow
from DbAccessFunctions import DeleteEqp
from DbAccessFunctions import UsEqpData
from DbAccessFunctions import IfUsable
from DbAccessFunctions import UnUsEqpData
from DbAccessFunctions import ModUnUsEqpKind
from DbAccessFunctions import ModUsEqpKind
from DbAccessFunctions import ChangeEqpUsName
from DbAccessFunctions import ChangeEqpUnUsName
from DbAccessFunctions import ChangeEqpUsNr
from DbAccessFunctions import IsUsNameUnique
from DbAccessFunctions import IsUnUsNameUnique
from DbAccessFunctions import IsUsKindUnique
from DbAccessFunctions import IsUnUsKindUnique
from DbAccessFunctions import UsEquipment
from DbAccessFunctions import UnUsEquipment
from DbAccessFunctions import IfUsableKind
from DbAccessFunctions import UsEquipByKind
from DbAccessFunctions import UnUsEquipByKind
from DbAccessFunctions import Search
from ChooseUserScreen import SelectableLabel
from ChooseUserScreen import SelectableRecycleBoxLayout

class UnavailUnUsEqpList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(UnavailUnUsEqpList, self).__init__(**kwargs)
        eqpdata = GetUnavailUnUsEqp()
        self.data=[{'text':x[0],'Eqpname':x[1]} for x in eqpdata]

class UnavailUsEqpList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(UnavailUsEqpList, self).__init__(**kwargs)
        eqpdata = GetUnavailUsEqp()
        self.data=[{'text':x[0],'Eqpname':x[1]} for x in eqpdata]

class DebtUsersList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(DebtUsersList, self).__init__(**kwargs)
        usrdata = GetDebtUsers()
        self.data=[{'text':x} for x in usrdata]

class EqpList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(EqpList, self).__init__(**kwargs)
        eqpdata = Equipment()
        self.data=[{'text':x[0]} for x in eqpdata]

class UsKindList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(UsKindList, self).__init__(**kwargs)
        kinddata = UsableEquipmentKind()
        self.data=[{'text':x} for x in kinddata]

class UnUsKindList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(UnUsKindList, self).__init__(**kwargs)
        kinddata = UnUsableEquipmentKind()
        self.data=[{'text':x} for x in kinddata]

class ManageEquipScreen(Screen):

	kind = ListProperty([])
	type = ListProperty([])
	srch = ObjectProperty(TextInput)
	srchbtn = ObjectProperty(Button)
	eqplst = ObjectProperty(EqpList)
	addusbtn = ObjectProperty(Button)
	addunusbtn = ObjectProperty(Button)
	adduskdbtn = ObjectProperty(Button)
	addunuskdbtn = ObjectProperty(Button)
	deluskdbtn = ObjectProperty(Button)
	delunuskdbtn = ObjectProperty(Button)
	advbtn = ObjectProperty(Button)
	delbtn = ObjectProperty(Button)
	modbtn = ObjectProperty(Button)
	bckbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(ManageEquipScreen, self).__init__(**kwargs)
		self.type = ["Wybierz typ","Sprzety zuzywalne", "Sprzety niezuzywalne"]
		self.kind = ["Wybierz rodzaj"]
		eqpdata = Equipment()
		self.eqplst.data = [{'text':x[0]} for x in eqpdata]

	def GetToAddUs(self):
		app = App.get_running_app()
		Window.size = (400, 200)
		screen = app.root.get_screen("dodaj sprzet zuzywalny")
		screen.UpdateData()
		app.root.current = "dodaj sprzet zuzywalny"
		self.ClearInput()

	def GetToAddUnUs(self):
		app = App.get_running_app()
		Window.size = (400, 150)
		app.root.current = "dodaj sprzet niezuzywalny"
		self.ClearInput()

	def GetToAddUsKind(self):
		app = App.get_running_app()
		Window.size = (400, 100)
		app.root.current = "dodaj rodzaj sprzetu zuzywalnego"
		self.ClearInput()

	def GetToAddUnUsKind(self):
			app = App.get_running_app()
			Window.size = (600, 150)
			app.root.current = "dodaj rodzaj sprzetu niezuzywalnego"
			self.ClearInput()

	def GetToDelUsKind(self):
		app = App.get_running_app()
		Window.size = (400, 300)
		app.root.current = "usun rodzaj sprzetu zuzywalnego"
		self.ClearInput()

	def GetToDelUnUsKind(self):
		app = App.get_running_app()
		Window.size = (400, 300)
		app.root.current = "usun rodzaj sprzetu niezuzywalnego"
		self.ClearInput()

	def GetToMaxBor(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zmien maksymalne wypozyczenie")
		screen.UpdateData()
		Window.size = (600, 150)
		app.root.current = "zmien maksymalne wypozyczenie"
		self.ClearInput()

	def GetToDelEqp(self):
		app = App.get_running_app()
		screen = app.root.get_screen("potwierdz usuniecie sprzetu")
		eqp = self.eqplst.data[self.eqplst.ChosenElement.index]['text']
		screen.UpdateData(eqp)
		Window.size = (600, 150)
		app.root.current = "potwierdz usuniecie sprzetu"
		self.ClearInput()

	def GetToMod(self):
		app = App.get_running_app()
		eqp = self.eqplst.data[self.eqplst.ChosenElement.index]['text']
		usable = IfUsable(eqp)
		if usable == True:
			screen = app.root.get_screen("modyfikuj sprzet zuzywalny")
			screen.UpdateData(eqp)
			Window.size = (600, 360)
			app.root.current = "modyfikuj sprzet zuzywalny"
		else:
			screen = app.root.get_screen("modyfikuj sprzet niezuzywalny")
			screen.UpdateData(eqp)
			Window.size = (800, 360)
			app.root.current = "modyfikuj sprzet niezuzywalny"
		self.ClearInput()

	def GetToAdv(self):
		app = App.get_running_app()
		Window.size = (400, 300)
		app.root.current = "zaawansowane zarzadzanie sprzetem"
		self.ClearInput()

	def UpdateData(self):
		eqpdata = Equipment()
		self.eqplst.data=[{'text':x[0]} for x in eqpdata]
		self.eqplst.refresh_from_data()

	def Search(self, type, kind, content):
		eqpdata = Search(type, kind, content)
		self.eqplst.data=[{'text':x} for x in eqpdata]
		self.eqplst.refresh_from_data()

	def UpdateSpinner2(self, chosen1):
		self.ids.kindsel.text = "Wybierz rodzaj"
		if chosen1 == "Sprzety zuzywalne":
			self.ids.kindsel.values = UsableEquipmentKind()
			eqpdata = UsEquipment()
			self.eqplst.data=[{'text':x[0]} for x in eqpdata]
			self.eqplst.refresh_from_data()

		else:
			if chosen1 == "Sprzety niezuzywalne":
				self.ids.kindsel.values = UnUsableEquipmentKind()
				eqpdata = UnUsEquipment()
				self.eqplst.data=[{'text':x[0]} for x in eqpdata]
				self.eqplst.refresh_from_data()
				
			else:
				self.ids.kindsel.values = ["Wybierz rodzaj"]
				self.UpdateData()

	def UpdateContentKind(self, chosen):
		isusable = IfUsableKind(chosen)
		if self.ids.typesel.text != "Wybierz typ":
			if isusable == True:
				eqpdata = UsEquipByKind(chosen)
				self.eqplst.data=[{'text':x} for x in eqpdata]
				self.eqplst.refresh_from_data()

			else:
				eqpdata = UnUsEquipByKind(chosen)
				self.eqplst.data=[{'text':x} for x in eqpdata]
				self.eqplst.refresh_from_data()

	def GetBack(self):
		app = App.get_running_app()
		Window.size = (400, 360)
		app.root.current = "opcje administratora"
		self.ClearInput()
	
	def ClearInput(self):
		self.ids.typesel.text = "Wybierz typ"
		self.ids.kindsel.text = "Wybierz rodzaj"
		self.srch.text = ""

class AddUsableEqpScreen(Screen):
	eqpname = ObjectProperty(TextInput)
	amount = ObjectProperty(TextInput)
	kind = ListProperty([])
	bckbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(AddUsableEqpScreen, self).__init__(**kwargs)
		self.UpdateData()

	def SubmitAdding(self):
		app = App.get_running_app()
		if(IsUsNameUnique(self.eqpname.text) == True and self.eqpname.text != "" and self.amount.text != "" and self.kindsel.text != "Wybierz rodzaj"):
			value = int(self.amount.text)
			AddEqpUs(app.root.login, self.eqpname.text, value, self.kindsel.text)
			screen = app.root.get_screen("zarzadzaj sprzetem")
			screen.UpdateData()
			Window.size = (900, 600)
			app.root.current = "zarzadzaj sprzetem"
			self.ClearInput()

	def UpdateData(self):
		self.kind = UsableEquipmentKind()

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zarzadzaj sprzetem")
		screen.UpdateData()
		Window.size = (900, 600)
		app.root.current = "zarzadzaj sprzetem"
		self.ClearInput()

	def ClearInput(self):
		self.ids.kindsel.text = "Wybierz rodzaj"
		self.eqpname.text = ""
		self.amount.text = ""

class AddUnUsableEqpScreen(Screen):
	eqpname = ObjectProperty(TextInput)
	kind = ListProperty([])
	bckbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(AddUnUsableEqpScreen, self).__init__(**kwargs)
		self.UpdateData() 

	def SubmitAdding(self):
		app = App.get_running_app()
		if(IsUnUsNameUnique(self.eqpname.text) == True and self.eqpname.text != "" and self.kindsel.text != "Wybierz rodzaj"):
			AddEqpUnUs(app.root.login, self.eqpname.text, self.kindsel.text)
			screen = app.root.get_screen("zarzadzaj sprzetem")
			screen.UpdateData()
			Window.size = (900, 600)
			app.root.current = "zarzadzaj sprzetem"
			self.ClearInput()

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zarzadzaj sprzetem")
		screen.UpdateData()
		Window.size = (900, 600)
		app.root.current = "zarzadzaj sprzetem"
		self.ClearInput()

	def ClearInput(self):
		self.ids.kindsel.text = "Wybierz rodzaj"
		self.eqpname.text = ""
	
	def UpdateData(self):
		self.kind = UnUsableEquipmentKind()

class AddUsableEqpKindScreen(Screen):
	kindname = ObjectProperty(TextInput)
	bckbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(AddUsableEqpKindScreen, self).__init__(**kwargs)

	def SubmitAdding(self):
		app = App.get_running_app()
		if(IsUsKindUnique(self.kindname.text) == True and self.kindname.text != ""):
			AddEqpUsKind(app.root.login, self.kindname.text)
			screen = app.root.get_screen("dodaj sprzet zuzywalny")
			screen.UpdateData()
			Window.size = (900, 600)
			app.root.current = "zarzadzaj sprzetem"
			self.ClearInput()

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zarzadzaj sprzetem")
		screen.UpdateData()
		Window.size = (900, 600)
		app.root.current = "zarzadzaj sprzetem"
		self.ClearInput()

	def ClearInput(self):
		self.kindname.text = ""

class AddUnUsableEqpKindScreen(Screen):
	kindname = ObjectProperty(TextInput)
	maxbor = ObjectProperty(TextInput)
	bckbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(AddUnUsableEqpKindScreen, self).__init__(**kwargs)

	def SubmitAdding(self):
		app = App.get_running_app()
		if(IsUnUsKindUnique(self.kindname.text) == True and self.kindname.text != "" and self.maxbor.text != ""):
			AddEqpUnUsKind(app.root.login, self.kindname.text, int(self.maxbor.text))
			screen = app.root.get_screen("dodaj sprzet niezuzywalny")
			screen.UpdateData()
			Window.size = (900, 600)
			app.root.current = "zarzadzaj sprzetem"
			self.ClearInput()

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zarzadzaj sprzetem")
		screen.UpdateData()
		Window.size = (900, 600)
		app.root.current = "zarzadzaj sprzetem"
		self.ClearInput()

	def ClearInput(self):
		self.kindname.text = ""
		self.maxbor.text = ""

class DeleteUsKindScreen(Screen):

	uskindlst = ObjectProperty(UsKindList)
	bckbtn = ObjectProperty(Button)
	delbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(DeleteUsKindScreen, self).__init__(**kwargs)

	def UpdateData(self):
		kinddata = UsableEquipmentKind()
		self.uskindlst.data=[{'text':x} for x in kinddata]
		self.uskindlst.refresh_from_data()

	def GetToDel(self):
		app = App.get_running_app()
		uskind = self.uskindlst.data[self.uskindlst.ChosenElement.index]['text']
		screen = app.root.get_screen("potwierdz usuniecie rodzaju sprzetu zuzywalnego")
		screen.UpdateData(uskind)
		Window.size = (600, 120)
		app.root.current = "potwierdz usuniecie rodzaju sprzetu zuzywalnego"

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zarzadzaj sprzetem")
		screen.UpdateData()
		Window.size = (900, 600)
		app.root.current = "zarzadzaj sprzetem"

class ConfirmDeleteUsKindScreen(Screen):

	kindcont = ObjectProperty(Label)
	kind = StringProperty('')
	bckbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(ConfirmDeleteUsKindScreen, self).__init__(**kwargs)

	def UpdateData(self, kindtodel):
		self.kind = kindtodel
		self.kindcont.text = kindtodel

	def SubmitDeletion(self):
		app = App.get_running_app()
		DeleteUsKind(app.root.login, self.kindcont.text)
		screen = app.root.get_screen("zarzadzaj sprzetem")
		screen.UpdateData()
		screen = app.root.get_screen("usun rodzaj sprzetu zuzywalnego")
		screen.UpdateData()
		Window.size = (900, 600)
		app.root.current = "zarzadzaj sprzetem"

	def GetBack(self):
		app = App.get_running_app()
		Window.size = (400, 300)
		app.root.current = "usun rodzaj sprzetu zuzywalnego"

class DeleteUnUsKindScreen(Screen):

	unuskindlst = ObjectProperty(UnUsKindList)
	bckbtn = ObjectProperty(Button)
	delbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(DeleteUnUsKindScreen, self).__init__(**kwargs)

	def UpdateData(self):
		kinddata = UnUsableEquipmentKind()
		self.unuskindlst.data=[{'text':x} for x in kinddata]
		self.unuskindlst.refresh_from_data()

	def GetToDel(self):
		app = App.get_running_app()
		unuskind = self.unuskindlst.data[self.unuskindlst.ChosenElement.index]['text']
		screen = app.root.get_screen("potwierdz usuniecie rodzaju sprzetu niezuzywalnego")
		screen.UpdateData(unuskind)
		Window.size = (600, 120)
		app.root.current = "potwierdz usuniecie rodzaju sprzetu niezuzywalnego"

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zarzadzaj sprzetem")
		screen.UpdateData()
		Window.size = (900, 600)
		app.root.current = "zarzadzaj sprzetem"

class ConfirmDeleteUnUsKindScreen(Screen):

	kindcont = ObjectProperty(Label)
	kind = StringProperty('')
	bckbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(ConfirmDeleteUnUsKindScreen, self).__init__(**kwargs)

	def UpdateData(self, kindtodel):
		self.kind = kindtodel
		self.kindcont.text = kindtodel

	def SubmitDeletion(self):
		app = App.get_running_app()
		DeleteUnUsKind(app.root.login, self.kindcont.text)
		screen = app.root.get_screen("zarzadzaj sprzetem")
		screen.UpdateData()
		screen = app.root.get_screen("usun rodzaj sprzetu niezuzywalnego")
		screen.UpdateData()
		Window.size = (900, 600)
		app.root.current = "zarzadzaj sprzetem"

	def GetBack(self):
		app = App.get_running_app()
		Window.size = (400, 300)
		app.root.current = "usun rodzaj sprzetu niezuzywalnego"

class AdvancedEqpScreen(Screen):
	debtusrbtn = ObjectProperty(Button)
	unreturneqpbtn = ObjectProperty(Button)
	unavaileqpbtn = ObjectProperty(Button)
	bckbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(AdvancedEqpScreen, self).__init__(**kwargs)

	def GetToDebtUsers(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zadluzeni uzytkownicy")
		screen.UpdateData()
		Window.size = (600, 300)
		app.root.current = "zadluzeni uzytkownicy"

	def GetToUnavailUsEqp(self):
		app = App.get_running_app()
		screen = app.root.get_screen("niedostepny sprzet zuzywalny")
		screen.UpdateData()
		Window.size = (400, 300)
		app.root.current = "niedostepny sprzet zuzywalny"

	def GetToUnavailUnUsEqp(self):
		app = App.get_running_app()
		screen = app.root.get_screen("niedostepny sprzet niezuzywalny")
		screen.UpdateData()
		Window.size = (400, 300)
		app.root.current = "niedostepny sprzet niezuzywalny"

	def GetBack(self):
		app = App.get_running_app()
		Window.size = (900, 600)
		app.root.current = "zarzadzaj sprzetem"

class MaxBorrowScreen(Screen):
	newmaxbor = ObjectProperty(TextInput)
	currentmaxbor = ObjectProperty(Label)
	kind = ListProperty([])
	bckbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(MaxBorrowScreen, self).__init__(**kwargs)
		self.UpdateData() 

	def SubmitChange(self):
		app = App.get_running_app()
		if self.kindsel.text != "Wybierz rodzaj" and self.newmaxbor.text != "":
			ChangeMaxBorrow(app.root.login, self.kindsel.text, int(self.newmaxbor.text))
			screen = app.root.get_screen("zarzadzaj sprzetem")
			screen.UpdateData()
			Window.size = (900, 600)
			app.root.current = "zarzadzaj sprzetem"
			self.ClearInput()

	def UpdateLabel(self):
		if self.kindsel.text != "Wybierz rodzaj":
			self.currentmaxbor.text = CurrentMaxBorrow(self.kindsel.text)

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zarzadzaj sprzetem")
		screen.UpdateData()
		Window.size = (900, 600)
		app.root.current = "zarzadzaj sprzetem"
		self.ClearInput()

	def ClearInput(self):
		self.ids.kindsel.text = "Wybierz rodzaj"
		self.newmaxbor.text = ""
		self.currentmaxbor.text = ""
	
	def UpdateData(self):
		self.kind = UnUsableEquipmentKind()

class DebtUsersScreen(Screen):
	debtusrlst = ObjectProperty(DebtUsersList)
	bckbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(DebtUsersScreen, self).__init__(**kwargs)

	def UpdateData(self):
		usrdata = GetDebtUsers()
		self.debtusrlst.data=[{'text':x} for x in usrdata]
		self.debtusrlst.refresh_from_data()

	def GetBack(self):
		app = App.get_running_app()
		Window.size = (400, 300)
		app.root.current = "zaawansowane zarzadzanie sprzetem"

class UnavailUsEqpScreen(Screen):
	unavaileqplst = ObjectProperty(UnavailUsEqpList)
	modbtn = ObjectProperty(Button)
	bckbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(UnavailUsEqpScreen, self).__init__(**kwargs)

	def GetToMod(self):
		app = App.get_running_app()
		if len(self.unavaileqplst.data) != 0:
			eqp = self.unavaileqplst.data[self.unavaileqplst.ChosenElement.index]['Eqpname']
			usable = IfUsable(eqp)
			if usable == True:
				screen = app.root.get_screen("modyfikuj sprzet zuzywalny")
				screen.UpdateData(eqp)
				Window.size = (600, 360)
				app.root.current = "modyfikuj sprzet zuzywalny"
			else:
				screen = app.root.get_screen("modyfikuj sprzet niezuzywalny")
				screen.UpdateData(eqp)
				Window.size = (800, 360)
				app.root.current = "modyfikuj sprzet niezuzywalny"

	def UpdateData(self):
		eqpdata = GetUnavailUsEqp()
		self.unavaileqplst.data=[{'text':x[0],'Eqpname':x[1]} for x in eqpdata]
		self.unavaileqplst.refresh_from_data()

	def GetBack(self):
		app = App.get_running_app()
		Window.size = (400, 300)
		app.root.current = "zaawansowane zarzadzanie sprzetem"

class UnavailUnUsEqpScreen(Screen):
	unavaileqplst = ObjectProperty(UnavailUnUsEqpList)
	modbtn = ObjectProperty(Button)
	bckbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(UnavailUnUsEqpScreen, self).__init__(**kwargs)

	def GetToMod(self):
		app = App.get_running_app()
		if len(self.unavaileqplst.data) != 0:
			eqp = self.unavaileqplst.data[self.unavaileqplst.ChosenElement.index]['Eqpname']
			usable = IfUsable(eqp)
			if usable == True:
				screen = app.root.get_screen("modyfikuj sprzet zuzywalny")
				screen.UpdateData(eqp)
				Window.size = (600, 360)
				app.root.current = "modyfikuj sprzet zuzywalny"
			else:
				screen = app.root.get_screen("modyfikuj sprzet niezuzywalny")
				screen.UpdateData(eqp)
				Window.size = (800, 360)
				app.root.current = "modyfikuj sprzet niezuzywalny"

	def UpdateData(self):
		eqpdata = GetUnavailUnUsEqp()
		self.unavaileqplst.data=[{'text':x[0],'Eqpname':x[1]} for x in eqpdata]
		self.unavaileqplst.refresh_from_data()

	def GetBack(self):
		app = App.get_running_app()
		Window.size = (400, 300)
		app.root.current = "zaawansowane zarzadzanie sprzetem"

class ConfirmDeleteEqpScreen(Screen):

	eqpcont = ObjectProperty(Label)
	eqp = StringProperty('')
	bckbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(ConfirmDeleteEqpScreen, self).__init__(**kwargs)

	def UpdateData(self, eqptodel):
		self.eqp = eqptodel
		self.eqpcont.text = eqptodel

	def SubmitDeletion(self):
		app = App.get_running_app()
		DeleteEqp(app.root.login, self.eqpcont.text)
		screen = app.root.get_screen("zarzadzaj sprzetem")
		screen.UpdateData()
		Window.size = (900, 600)
		app.root.current = "zarzadzaj sprzetem"

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zarzadzaj sprzetem")
		screen.UpdateData()
		Window.size = (900, 600)
		app.root.current = "zarzadzaj sprzetem"

class ModUsEqpScreen(Screen):
	namecont = ObjectProperty(Label)
	kindcont = ObjectProperty(Label)
	numbercont = ObjectProperty(Label)
	eqp = StringProperty('')
	namebtn = ObjectProperty(Button)
	kindbtn = ObjectProperty(Button)
	numberbtn = ObjectProperty(Button)
	delbtn = ObjectProperty(Button)
	bckbtn = ObjectProperty(Button)
	

	def __init__(self,**kwargs):
		super(ModUsEqpScreen, self).__init__(**kwargs)

	def UpdateData(self, eqpmod):
		self.eqp = eqpmod
		data = UsEqpData(eqpmod)
		self.namecont.text = data[0]
		self.kindcont.text = data[1]
		self.numbercont.text = data[2]

	def SubmitDeletion(self):
		app = App.get_running_app()
		screen = app.root.get_screen("potwierdz usuniecie sprzetu")
		screen.UpdateData(self.eqp)
		Window.size = (600, 150)
		app.root.current = "potwierdz usuniecie sprzetu"

	def GetToModKind(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zmien rodzaj sprzetu zuzywalnego")
		screen.UpdateData(self.eqp)
		Window.size = (600, 200)
		app.root.current = "zmien rodzaj sprzetu zuzywalnego"

	def GetToModName(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zmien nazwe sprzetu zuzywalnego")
		screen.UpdateData(self.eqp)
		Window.size = (600, 100)
		app.root.current = "zmien nazwe sprzetu zuzywalnego"

	def GetToModNr(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zmien liczbe sprzetu zuzywalnego")
		screen.UpdateData(self.eqp)
		Window.size = (600, 100)
		app.root.current = "zmien liczbe sprzetu zuzywalnego"

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zarzadzaj sprzetem")
		screen.UpdateData()
		Window.size = (900, 600)
		app.root.current = "zarzadzaj sprzetem"

class ModUnUsEqpScreen(Screen):
	namecont = ObjectProperty(Label)
	kindcont = ObjectProperty(Label)
	statuscont = ObjectProperty(Label)
	eqp = StringProperty('')
	namebtn = ObjectProperty(Button)
	kindbtn = ObjectProperty(Button)
	statusbtn = ObjectProperty(Button)
	delbtn = ObjectProperty(Button)
	bckbtn = ObjectProperty(Button)
	

	def __init__(self,**kwargs):
		super(ModUnUsEqpScreen, self).__init__(**kwargs)

	def UpdateData(self, eqpmod):
		self.eqp = eqpmod
		data = UnUsEqpData(eqpmod)
		self.namecont.text = data[0]
		self.kindcont.text = data[1]
		self.statuscont.text = data[2]

	def GetToModKind(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zmien rodzaj sprzetu niezuzywalnego")
		screen.UpdateData(self.eqp)
		Window.size = (600, 200)
		app.root.current = "zmien rodzaj sprzetu niezuzywalnego"

	def GetToModName(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zmien nazwe sprzetu niezuzywalnego")
		screen.UpdateData(self.eqp)
		Window.size = (600, 100)
		app.root.current = "zmien nazwe sprzetu niezuzywalnego"

	def SubmitDeletion(self):
		app = App.get_running_app()
		screen = app.root.get_screen("potwierdz usuniecie sprzetu")
		screen.UpdateData(self.eqp)
		Window.size = (600, 150)
		app.root.current = "potwierdz usuniecie sprzetu"

	def GetToReturn(self):
		app = App.get_running_app()
		Window.size = (900, 100)
		screen = app.root.get_screen("potwierdz oddanie sprzetu")
		screen.UpdateData(self.eqp)
		app.root.current = "potwierdz oddanie sprzetu"

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("zarzadzaj sprzetem")
		screen.UpdateData()
		Window.size = (900, 600)
		app.root.current = "zarzadzaj sprzetem"

class ModUsEqpKindScreen(Screen):
	kind = ListProperty([])
	eqpname = StringProperty("")
	bckbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(ModUsEqpKindScreen, self).__init__(**kwargs)
		self.UpdateData(self.eqpname)

	def SubmitChange(self):
		app = App.get_running_app()
		if self.kindsel.text != "Wybierz rodzaj":
			ModUsEqpKind(app.root.login, self.eqpname, self.kindsel.text)
			screen = app.root.get_screen("modyfikuj sprzet zuzywalny")
			screen.UpdateData(self.eqpname)
			Window.size = (600, 360)
			app.root.current = "modyfikuj sprzet zuzywalny"
			self.ClearInput()

	def UpdateData(self, equip):
		self.kind = UsableEquipmentKind()
		self.eqpname = equip

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("modyfikuj sprzet zuzywalny")
		Window.size = (600, 360)
		app.root.current = "modyfikuj sprzet zuzywalny"
		self.ClearInput()

	def ClearInput(self):
		self.ids.kindsel.text = "Wybierz rodzaj"
		self.eqpname = ""

class ModUnUsEqpKindScreen(Screen):
	kind = ListProperty([])
	eqpname = StringProperty("")
	bckbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(ModUnUsEqpKindScreen, self).__init__(**kwargs)
		self.UpdateData(self.eqpname)

	def SubmitChange(self):
		app = App.get_running_app()
		if self.kindsel.text != "Wybierz rodzaj":
			ModUnUsEqpKind(app.root.login, self.eqpname, self.kindsel.text)
			screen = app.root.get_screen("modyfikuj sprzet niezuzywalny")
			screen.UpdateData(self.eqpname)
			Window.size = (600, 360)
			app.root.current = "modyfikuj sprzet niezuzywalny"
			self.ClearInput()

	def UpdateData(self, equip):
		self.kind = UnUsableEquipmentKind()
		self.eqpname = equip

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("modyfikuj sprzet niezuzywalny")
		Window.size = (600, 360)
		app.root.current = "modyfikuj sprzet niezuzywalny"
		self.ClearInput()

	def ClearInput(self):
		self.ids.kindsel.text = "Wybierz rodzaj"
		self.eqpname = ""

class ModNameUsableEqpScreen(Screen):
	neweqpname = ObjectProperty(TextInput)
	eqpname = StringProperty('')
	bckbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(ModNameUsableEqpScreen, self).__init__(**kwargs)

	def SubmitChange(self):
		app = App.get_running_app()
		if self.neweqpname.text != "":
			ChangeEqpUsName(app.root.login, self.eqpname, self.neweqpname.text)
			self.eqpname = self.neweqpname.text
			screen = app.root.get_screen("modyfikuj sprzet zuzywalny")
			screen.UpdateData(self.eqpname)
			Window.size = (600, 360)
			app.root.current = "modyfikuj sprzet zuzywalny"
			self.ClearInput()

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("modyfikuj sprzet zuzywalny")
		screen.UpdateData(self.eqpname)
		Window.size = (600, 360)
		app.root.current = "modyfikuj sprzet zuzywalny"
		self.ClearInput()

	def ClearInput(self):
		self.neweqpname.text = ""

	def UpdateData(self, eqp):
		self.eqpname = eqp

class ModNameUnUsableEqpScreen(Screen):
	neweqpname = ObjectProperty(TextInput)
	eqpname = StringProperty('')
	bckbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(ModNameUnUsableEqpScreen, self).__init__(**kwargs)

	def SubmitChange(self):
		app = App.get_running_app()
		if self.neweqpname.text != "":
			ChangeEqpUnUsName(app.root.login, self.eqpname, self.neweqpname.text)
			self.eqpname = self.neweqpname.text
			screen = app.root.get_screen("modyfikuj sprzet niezuzywalny")
			screen.UpdateData(self.eqpname)
			Window.size = (800, 360)
			app.root.current = "modyfikuj sprzet niezuzywalny"
			self.ClearInput()

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("modyfikuj sprzet niezuzywalny")
		screen.UpdateData(self.eqpname)
		Window.size = (800, 360)
		app.root.current = "modyfikuj sprzet niezuzywalny"
		self.ClearInput()

	def ClearInput(self):
		self.neweqpname.text = ""

	def UpdateData(self, eqp):
		self.eqpname = eqp

class ModNrUsableEqpScreen(Screen):
	neweqpnr = ObjectProperty(TextInput)
	eqpname = StringProperty('')
	bckbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(ModNrUsableEqpScreen, self).__init__(**kwargs)

	def SubmitChange(self):
		app = App.get_running_app()
		if self.neweqpnr.text != "":
			ChangeEqpUsNr(app.root.login, self.eqpname, int(self.neweqpnr.text))
			screen = app.root.get_screen("modyfikuj sprzet zuzywalny")
			screen.UpdateData(self.eqpname)
			Window.size = (600, 360)
			app.root.current = "modyfikuj sprzet zuzywalny"
			self.ClearInput()

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("modyfikuj sprzet zuzywalny")
		screen.UpdateData(self.eqpname)
		Window.size = (600, 360)
		app.root.current = "modyfikuj sprzet zuzywalny"
		self.ClearInput()

	def ClearInput(self):
		self.neweqpnr.text = ""

	def UpdateData(self, eqp):
		self.eqpname = eqp
		