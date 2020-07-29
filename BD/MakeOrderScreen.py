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
from DbAccessFunctions import SearchAvail
from DbAccessFunctions import Search
from DbAccessFunctions import AvailUsEquipByKind
from DbAccessFunctions import AvailUnUsEquipByKind
from DbAccessFunctions import AvailUnUsEquipment
from DbAccessFunctions import AvailUsEquipment
from DbAccessFunctions import UsableEquipmentKind
from DbAccessFunctions import UnUsableEquipmentKind
from DbAccessFunctions import MakeUsOrder
from DbAccessFunctions import MakeUnUsOrder

class UsEqpList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(UsEqpList, self).__init__(**kwargs)
        eqpdata = AvailUsEquipment()
        self.data=[{'text':x[0], 'nazwa': x[1]} for x in eqpdata]

class UnUsEqpList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(UsEqpList, self).__init__(**kwargs)
        eqpdata = AvailUnUsEquipment()
        self.data=[{'text':x[0], 'nazwa': x[1]} for x in eqpdata]

class ChosenList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(ChosenList, self).__init__(**kwargs)


class ChooseTypeOrderScreen(Screen):
	usordbtn = ObjectProperty(Button)
	unusordbtn = ObjectProperty(Button)
	bckbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(ChooseTypeOrderScreen, self).__init__(**kwargs)

	def GetToUsOrd(self):
		app = App.get_running_app()
		Window.size = (900, 600)
		screen = app.root.get_screen("zloz zamowienie zuzywalne")
		screen.UpdateData()
		app.root.current = "zloz zamowienie zuzywalne"

	def GetToUnUsOrd(self):
		app = App.get_running_app()
		Window.size = (900, 600)
		screen = app.root.get_screen("zloz zamowienie niezuzywalne")
		screen.UpdateData()
		app.root.current = "zloz zamowienie niezuzywalne"

	def GetBack(self):
		app = App.get_running_app()
		if app.root.rig == "czlonek_kola":
			Window.size = (400, 160)
			app.root.current = "opcje czlonka kola"
		elif app.root.rig == "administrator":
			Window.size = (400, 360)
			app.root.current = "opcje administratora"

class MakeUsOrderScreen(Screen):

	kind = ListProperty([])
	srch = ObjectProperty(TextInput)
	srchbtn = ObjectProperty(Button)
	eqplst = ObjectProperty(UsEqpList)
	chosenlst = ObjectProperty(ChosenList)
	delbtn = ObjectProperty(Button)
	addbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)
	bckbtn = ObjectProperty(Button)
	num = ObjectProperty(TextInput)

 #       ChosenLogin = self.usrlst.data[self.usrlst.ChosenElement.index]['nazwa']

	def __init__(self,**kwargs):
		super(MakeUsOrderScreen, self).__init__(**kwargs)
		eqpdata = AvailUsEquipment()
		self.eqplst.data = [{'text': x[0], 'nazwa': x[1], 'ilosc': x[2] } for x in eqpdata]
		self.kind = []

	def UpdateData(self):
		eqpdata = AvailUsEquipment()
		self.ids.kindsel.values = UsableEquipmentKind()
		self.eqplst.data =   [{'text': x[0], 'nazwa': x[1], 'ilosc': x[2] } for x in eqpdata]
		self.eqplst.refresh_from_data()
		self.chosenlst.refresh_from_data()

	def Search(self, kind, content):
		type = "Sprzety zuzywalne"
		eqpdata = SearchAvail(type, kind, content)
		self.eqplst.data = [{'text': x[0], 'nazwa': x[1], 'ilosc': x[2]  } for x in eqpdata]
		self.eqplst.refresh_from_data()

	def UpdateContentKind(self, chosen):
		eqpdata = AvailUsEquipByKind(chosen)
		self.eqplst.data =  [{'text': x[0], 'nazwa': x[1], 'ilosc': x[2] } for x in eqpdata]
		self.eqplst.refresh_from_data()

	def AddtoCart(self):
		element = self.eqplst.ChosenElement
		cur_num = 0
		ind = -1
		for i in range(len(self.chosenlst.data)):
			label = self.chosenlst.data[i]
			if label['nazwa'] == element.nazwa:
				cur_num = label['ilosc']
				ind = i
		if self.num.text.isdigit() and int(self.num.text) in range(1, element.ilosc + 1 - cur_num):
			updated_num = cur_num + int(self.num.text)
			if ind == -1:
				self.chosenlst.data.append({'text': element.nazwa + " ilosc: " + str(updated_num), 'nazwa': element.nazwa , 'ilosc': updated_num})
			else:
				self.chosenlst.data[ind] = {'text': element.nazwa + "ilosc " + str(updated_num), 'nazwa': element.nazwa , 'ilosc': updated_num}
			self.UpdateData()
			self.num.text = ""

	def PopFromCart(self):
		element = self.chosenlst.ChosenElement
		for i in self.chosenlst.data:
			if i['nazwa'] == element.nazwa:
				self.chosenlst.data.remove(i)
		self.UpdateData()

	def SubmitUsOrder(self):
		app = App.get_running_app()
		login = app.root.login
		MakeUsOrder(login, self.chosenlst.data)
		self.GetBack()
	
	def GetBack(self):
		app = App.get_running_app()
		Window.size = (400, 150)
		app.root.current = "wybor typu zamowienia"
		self.ClearInput()
	
	def ClearInput(self):
		self.ids.kindsel.text = "Wybierz rodzaj"
		self.srch.text = ""
		self.chosenlst.data = []




class MakeUnUsOrderScreen(Screen):

	kind = ListProperty([])
	srch = ObjectProperty(TextInput)
	srchbtn = ObjectProperty(Button)
	eqplst = ObjectProperty(UsEqpList)
	chosenlst = ObjectProperty(ChosenList)
	delbtn = ObjectProperty(Button)
	addbtn = ObjectProperty(Button)
	confbtn = ObjectProperty(Button)
	bckbtn = ObjectProperty(Button)
	days = ObjectProperty(TextInput)


	def __init__(self,**kwargs):
		super(MakeUnUsOrderScreen, self).__init__(**kwargs)
		eqpdata = AvailUsEquipment()
		self.eqplst.data = [{'text':x[0], 'nazwa': x[1], 'ilosc': x[2]} for x in eqpdata]
		self.kind = []

	def UpdateData(self):
		eqpdata = AvailUnUsEquipment()
		self.ids.kindsel.values = UnUsableEquipmentKind()
		self.eqplst.data=[{'text':x[0], 'nazwa': x[1], 'ilosc': x[2]} for x in eqpdata]
		self.eqplst.refresh_from_data()

	def Search(self, kind, content):
		type = "Sprzety niezuzywalne"
		eqpdata = SearchAvail(type, kind, content)
		self.eqplst.data=[{'text':x[0], 'nazwa': x[1], 'ilosc': x[2]} for x in eqpdata]
		self.eqplst.refresh_from_data()

	def UpdateContentKind(self, chosen):
		eqpdata = AvailUnUsEquipByKind(chosen)
		self.eqplst.data=[{'text':x[0], 'nazwa': x[1]} for x in eqpdata]
		self.eqplst.refresh_from_data()

	def AddtoCart(self):
		element = self.eqplst.ChosenElement
		
		for i in range(len(self.chosenlst.data)):
			label = self.chosenlst.data[i]
			if label['nazwa'] == element.nazwa:
				return

		if self.days.text.isdigit() and int(self.days.text) in range(1, element.ilosc + 1):
			self.chosenlst.data.append({'text': element.nazwa + " ilosc dni: " + self.days.text, 'nazwa': element.nazwa , 'ilosc': int(self.days.text)})
			self.UpdateData()
			self.days.text = ""

	def PopFromCart(self):
		element = self.chosenlst.ChosenElement
		for i in self.chosenlst.data:
			if i['nazwa'] == element.nazwa:
				self.chosenlst.data.remove(i)
		self.UpdateData()

	def SubmitUnUsOrder(self):
		app = App.get_running_app()
		login = app.root.login
		if self.chosenlst.data != []:
			MakeUnUsOrder(login, self.chosenlst.data)
		self.GetBack()

	def GetBack(self):
		app = App.get_running_app()
		Window.size = (400, 150)
		app.root.current = "wybor typu zamowienia"
		self.ClearInput()
	
	def ClearInput(self):
		self.ids.kindsel.text = "Wybierz rodzaj"
		self.srch.text = ""
		self.chosenlst.data = []