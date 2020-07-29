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
from DbAccessFunctions import UsOrders
from DbAccessFunctions import UnUsOrders
from DbAccessFunctions import UsOrderContent
from DbAccessFunctions import UnUsOrderContent

class ChooseTypeOrderBrowseScreen(Screen):
	usordbtn = ObjectProperty(Button)
	unusordbtn = ObjectProperty(Button)
	bckbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(ChooseTypeOrderBrowseScreen, self).__init__(**kwargs)

	def GetToUsOrd(self):
		app = App.get_running_app()
		Window.size = (600, 400)
		screen = app.root.get_screen("przegladaj zamowienia zuzywalne")
		screen.UpdateData()
		app.root.current = "przegladaj zamowienia zuzywalne"

	def GetToUnUsOrd(self):
		app = App.get_running_app()
		Window.size = (600, 400)
		screen = app.root.get_screen("przegladaj zamowienia niezuzywalne")
		screen.UpdateData()
		app.root.current = "przegladaj zamowienia niezuzywalne"

	def GetBack(self):
		app = App.get_running_app()
		Window.size = (400, 360)
		app.root.current = "opcje administratora"

class UsOrdersList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(UsOrdersList, self).__init__(**kwargs)
        orddata = UsOrders()
        self.data=[{'text':x[0], 'numer': x[1]} for x in orddata]

class UnUsOrdersList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(UnOrdersList, self).__init__(**kwargs)
        orddata = UnUsOrders()
        self.data=[{'text':x[0], 'numer': x[1]} for x in orddata]

class BrowseUsOrdersScreen(Screen):
	ordlst = ObjectProperty(UsOrdersList)
	detailbtn = ObjectProperty(Button)
	bckbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(BrowseUsOrdersScreen, self).__init__(**kwargs)
		orddata = UsOrders()
		self.ordlst.data=[{'text':x[0], 'numer': x[1]} for x in orddata]

	def GetToDetails(self):
		ChosenOrder = self.ordlst.data[self.ordlst.ChosenElement.index]['numer']
		app = App.get_running_app()
		Window.size = (800, 300)
		screen = app.root.get_screen("szczegoly zamowienia zuzywalnego")
		screen.UpdateData(ChosenOrder)
		app.root.current = "szczegoly zamowienia zuzywalnego"

	def GetBack(self):
		app = App.get_running_app()
		Window.size = (400, 150)
		app.root.current = "wybor typu zamowienia przegladanie"
	
	def UpdateData(self):
		orddata = UsOrders()
		self.ordlst.data=[{'text':x[0], 'numer': x[1]} for x in orddata]
		self.ordlst.refresh_from_data()

class BrowseUnUsOrdersScreen(Screen):
	ordlst = ObjectProperty(UsOrdersList)
	detailbtn = ObjectProperty(Button)
	bckbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(BrowseUnUsOrdersScreen, self).__init__(**kwargs)
		orddata = UnUsOrders()
		self.ordlst.data=[{'text':x[0], 'numer': x[1]} for x in orddata]

	def GetToDetails(self):
		ChosenOrder = self.ordlst.data[self.ordlst.ChosenElement.index]['numer']
		app = App.get_running_app()
		Window.size = (900, 300)
		screen = app.root.get_screen("szczegoly zamowienia niezuzywalnego")
		screen.UpdateData(ChosenOrder)
		app.root.current = "szczegoly zamowienia niezuzywalnego"

	def GetBack(self):
		app = App.get_running_app()
		Window.size = (400, 150)
		app.root.current = "wybor typu zamowienia przegladanie"
	
	def UpdateData(self):
		orddata = UnUsOrders()
		self.ordlst.data=[{'text':x[0], 'numer': x[1]} for x in orddata]
		self.ordlst.refresh_from_data()

class UsOrderContList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(UsOrderContList, self).__init__(**kwargs)
        self.data=[{}]

class UnUsOrderContList(RecycleView):
    ChosenElement = ObjectProperty(SelectableLabel)
    def __init__(self, **kwargs):
        super(UnUsOrderContList, self).__init__(**kwargs)
        self.data=[{}]

class DetailsUsOrdersScreen(Screen):
	ordlst = ObjectProperty(UsOrderContList)
	who = ObjectProperty(Label)
	when = ObjectProperty(Label)
	ordernr = ObjectProperty(Label)
	bckbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(DetailsUsOrdersScreen, self).__init__(**kwargs)

	def GetBack(self):
		app = App.get_running_app()
		Window.size = (600, 400)
		app.root.current = "przegladaj zamowienia zuzywalne"
		self.Clear()
	
	def UpdateData(self, ordernumber):
		orddata = UsOrderContent(ordernumber)
		self.who.text = f"Zamawiajacy/a: {orddata[0]}"
		self.when.text = f"Data zlozenia: {orddata[1]}"
		self.ordernr.text = f"Numer zamowienia: {str(ordernumber)}"
		self.ordlst.data=[{'text':x} for x in orddata[2]]
		self.ordlst.refresh_from_data()

	def Clear(self):
		self.who.text = ""
		self.when.text = ""
		self.ordernr.text = ""
		self.ordlst.data = [{}]
		self.ordlst.refresh_from_data()

class DetailsUnUsOrdersScreen(Screen):
	ordlst = ObjectProperty(UnUsOrderContList)
	who = ObjectProperty(Label)
	when = ObjectProperty(Label)
	ordernr = ObjectProperty(Label)
	bckbtn = ObjectProperty(Button)

	def __init__(self,**kwargs):
		super(DetailsUnUsOrdersScreen, self).__init__(**kwargs)

	def GetBack(self):
		app = App.get_running_app()
		Window.size = (600, 400)
		app.root.current = "przegladaj zamowienia niezuzywalne"
		self.Clear()
	
	def UpdateData(self, ordernumber):
		orddata = UnUsOrderContent(ordernumber)
		self.who.text = f"Zamawiajacy/a: {orddata[0]}"
		self.when.text = f"Data zlozenia: {orddata[1]}"
		self.ordernr.text = f"Numer zamowienia: {str(ordernumber)}"
		self.ordlst.data=[{'text':x} for x in orddata[2]]
		self.ordlst.refresh_from_data()

	def Clear(self):
		self.who.text = ""
		self.when.text = ""
		self.ordernr.text = ""
		self.ordlst.data = [{}]
		self.ordlst.refresh_from_data()

