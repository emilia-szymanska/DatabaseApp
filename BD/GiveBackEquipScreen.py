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
from ChooseUserScreen import SelectableLabel
from ChooseUserScreen import SelectableRecycleBoxLayout
from DbAccessFunctions import UnUsOrderEqp
from DbAccessFunctions import ReturnEqp

class ReturnEqpList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(ReturnEqpList, self).__init__(**kwargs)
        self.data=[]

class GiveBackEquipScreen(Screen):
	ordlst = ObjectProperty(ReturnEqpList)
	detailbtn = ObjectProperty(Button)
	bckbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(GiveBackEquipScreen, self).__init__(**kwargs)

	def GetToReturn(self):
		Chosen = self.ordlst.data[self.ordlst.ChosenElement.index]['sprzet']
		app = App.get_running_app()
		Window.size = (900, 100)
		screen = app.root.get_screen("potwierdz oddanie sprzetu")
		screen.UpdateData(Chosen)
		app.root.current = "potwierdz oddanie sprzetu"

	def GetBack(self):
		app = App.get_running_app()
		if app.root.rig == "czlonek_kola":
			Window.size = (400, 160)
			app.root.current = "opcje czlonka kola"
		elif app.root.rig == "administrator":
			Window.size = (400, 360)
			app.root.current = "opcje administratora"
	
	def UpdateData(self):
		app = App.get_running_app()
		orddata = UnUsOrderEqp(app.root.login)
		self.ordlst.data=[{'text':x[0], 'sprzet': x[1]} for x in orddata]
		self.ordlst.refresh_from_data()


class ConfirmReturningEqpScreen(Screen):
	eqpcont = ObjectProperty(Label)
	eqp = StringProperty('')
	bckbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(ConfirmReturningEqpScreen, self).__init__(**kwargs)

	def UpdateData(self, eqptoret):
		self.eqp = eqptoret
		self.eqpcont.text = eqptoret

	def SubmitReturning(self):
		app = App.get_running_app()
		ReturnEqp(self.eqpcont.text)
		if app.root.rig == "czlonek_kola":
			Window.size = (400, 160)
			app.root.current = "opcje czlonka kola"
		elif app.root.rig == "administrator":
			Window.size = (400, 360)
			app.root.current = "opcje administratora"

	def GetBack(self):
		app = App.get_running_app()
		screen = app.root.get_screen("oddaj sprzet")
		screen.UpdateData()
		Window.size = (500, 600)
		app.root.current = "oddaj sprzet"
