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
from ManageEquipScreen import EqpList
from DbAccessFunctions import UsableEquipmentKind
from DbAccessFunctions import UnUsableEquipmentKind
from DbAccessFunctions import AvailEquipment
from DbAccessFunctions import UsEqpData
from DbAccessFunctions import IfUsable
from DbAccessFunctions import UnUsEqpData
from DbAccessFunctions import AvailUsEquipment
from DbAccessFunctions import AvailUnUsEquipment
from DbAccessFunctions import IfUsableKind
from DbAccessFunctions import AvailUsEquipByKind
from DbAccessFunctions import AvailUnUsEquipByKind
from DbAccessFunctions import SearchAvail


class BrowseEquipScreen(Screen):

	kind = ListProperty([])
	type = ListProperty([])
	srch = ObjectProperty(TextInput)
	srchbtn = ObjectProperty(Button)
	eqplst = ObjectProperty(EqpList)
	bckbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(BrowseEquipScreen, self).__init__(**kwargs)
		self.type = ["Wybierz typ","Sprzety zuzywalne", "Sprzety niezuzywalne"]
		self.kind = ["Wybierz rodzaj"]
		eqpdata = AvailEquipment()
		self.eqplst.data = [{'text':x[0]} for x in eqpdata]

	def UpdateData(self):
		eqpdata = AvailEquipment()
		self.eqplst.data=[{'text':x[0]} for x in eqpdata]
		self.eqplst.refresh_from_data()

	def Search(self, type, kind, content):
		eqpdata = SearchAvail(type, kind, content)
		self.eqplst.data=[{'text':x[0]} for x in eqpdata]
		self.eqplst.refresh_from_data()

	def UpdateSpinner2(self, chosen1):
		self.ids.kindsel.text = "Wybierz rodzaj"
		if chosen1 == "Sprzety zuzywalne":
			self.ids.kindsel.values = UsableEquipmentKind()
			eqpdata = AvailUsEquipment()
			self.eqplst.data=[{'text':x[0]} for x in eqpdata]
			self.eqplst.refresh_from_data()

		else:
			if chosen1 == "Sprzety niezuzywalne":
				self.ids.kindsel.values = UnUsableEquipmentKind()
				eqpdata = AvailUnUsEquipment()
				self.eqplst.data=[{'text':x[0]} for x in eqpdata]
				self.eqplst.refresh_from_data()
				
			else:
				self.ids.kindsel.values = ["Wybierz rodzaj"]
				self.UpdateData()

	def UpdateContentKind(self, chosen):
		isusable = IfUsableKind(chosen)
		if self.ids.typesel.text != "Wybierz typ":
			if isusable == True:
				eqpdata = AvailUsEquipByKind(chosen)
				self.eqplst.data=[{'text':x[0]} for x in eqpdata]
				self.eqplst.refresh_from_data()

			else:
				eqpdata = AvailUnUsEquipByKind(chosen)
				self.eqplst.data=[{'text':x[0]} for x in eqpdata]
				self.eqplst.refresh_from_data()

	def GetBack(self):
		app = App.get_running_app()
		if app.root.rig == "czlonek_kola":
			Window.size = (400, 160)
			app.root.current = "opcje czlonka kola"
		elif app.root.rig == "administrator":
			Window.size = (400, 360)
			app.root.current = "opcje administratora"
		self.ClearInput()
	
	def ClearInput(self):
		self.ids.typesel.text = "Wybierz typ"
		self.ids.kindsel.text = "Wybierz rodzaj"
		self.srch.text = ""
