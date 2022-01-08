from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarListItem,TwoLineAvatarIconListItem, IconRightWidget, OneLineAvatarIconListItem
from kivy.properties import StringProperty
from kivymd.uix.textfield import MDTextField
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
import re
from functools import partial
from kivymd.uix.button import MDRaisedButton
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.list import OneLineListItem

Builder.load_file('main_kv.kv')
Builder.load_file('menu1.kv')
Builder.load_file('cos.kv')
Builder.load_file('oferte.kv')
Builder.load_file('burger.kv')
Builder.load_file('desert.kv')



v=[]



class main_kv(BoxLayout):
    pass

class Item(OneLineAvatarListItem):
    divider = None
    source = StringProperty()
    observatie = ObjectProperty

class Item1(MDDialog):
    pass

class Poplogin(MDDialog):
    pass
class Popstare(MDDialog):
    pass

class Popregister(MDDialog):
    pass



class Food(MDApp):
    def __init__(self, **kwargs):
        super(Food, self).__init__(**kwargs)
    nume = ObjectProperty()
    user=ObjectProperty()



    # User that is logged in in App 
    userlogat=None


    #
    contor=0



    cos = []   #Shopping Cart
    costest=[]
    costest.append(1)
    preturi = dict({
                    'MediteranaMare': 45.99, 'MediteranaMica': 35.99,
                    'SupremaMare': 47.50, 'SupremaMica': 37.50,
                    'MexicanaMare': 49.50, 'MexicanaMica': 38.50,
                    'ProsciuttoFunghiMare': 40.00, 'ProsciuttoFunghiMica': 32.00,
                    'HawaianaMare': 49.50, 'HawaianaMica': 38.50,
                    'DiavolaMare': 49.50, 'DiavolaMica': 38.50,
                    'TaraneascaMare': 49.50, 'TaraneascaMica': 38.50,
                    'RusticaMare': 49.50, 'RusticaMica': 38.50,
                    'RoyalCheeseMare':50.20, 'RoyalCheseMic':41.20,
                    'burgerclasicmare':42.00 , 'burgerclasicmic': 35.00,
                    'chickenburgermare': 48.80, 'chickenburgermic':39.70,
                    'hamburgeriutemare':55.20, 'hamburgeriutemic':48.20,
                    'burgerporcmare':49.99 , 'burgerporcmic':40.00,
                    'chorizoburgermare':54.50, 'chorizoburgermic':47.99,
                    'clatitemieremare':35.00, 'clatitemieremic':20.00,
                    'clatiteciocolatamare':36.50, 'clatiteciocolatamica':25.80
                    })



    dictionarcos=None   # shopping cart dictionary

    contorix=-1
    butonlogin=None
    butonregister=None


    dialog = None
    dialog1= None
    dialoglogin = None
    dialogregister = None
    dialogstare = None


#Message <dialog > that will be showed in case of error 
    def starepop(self):
        if self.dialogstare !=None:
            self.dialogstare= None
        if not self.dialogstare:
            self.dialogstare=None
            self.dialogstare=Popstare()
        self.dialogstare.open()

#Login Popup
    def loginpop(self):
        if self.dialoglogin !=None:
            self.dialoglogin= None
        if not self.dialoglogin:
            self.dialoglogin = Poplogin(
                type="simple",
                items=[


                ],
            )
        # print(source)
        self.dialoglogin.open()

#Register popup with email,password ... 
    def registerpop(self):
        if self.dialogregister !=None:
            self.dialogregister= None
        if not self.dialogregister:

            self.dialogregister = Popregister(
                type="simple",
                items=[


                ],
            )
        # print(source)
        self.dialogregister.open()


#Popup Imagine Mare Mancare   # Full screen image of the food 
    def pop1(self,source):
       # self.test()
        pop = Popup(title='', content=Image(source=source),
                    size_hint=(None, None), size=(400, 400),separator_color=(0,0,0,0))
        pop.open()


    #This button will update the shopping cart and will be added in an array
    def adauga_cos(self, produs, pret, observatie):
        if self.dictionarcos==None:
            print("ADAUGAT!!")
            self.dictionarcos=dict(self.root.ids.items())
        cantitate = pret.split()


        self.cos1=[]
        self.produs=produs
        self.observatie=observatie
        self.pretfinal=re.findall(r'\d+.\d+', cantitate[1])

        if self.observatie=='':
            self.observatie=''

        self.cos1.append(self.contor)
        self.cos1.append(self.produs)
        self.cos1.append(cantitate[0])
        self.cos1.append(self.observatie)
        self.cos1.append(self.pretfinal[0])
        self.cos.append(self.cos1)

        print(self.cos)
        self.contor=self.contor+1
        self.dialog1.dismiss()
        self.update_cos()    # Updated Shopping cart

#this function will check if the register information is okay, else the login button won't work
    def functieverificarelogin(self):

        if self.dialoglogin.password.text=="crossplatform" and self.dialoglogin.user.text=="root":
            self.butonlogin1()
            self.dialoglogin.dismiss()
            self.userlogat=self.dialoglogin.user.text

    # Logout function 
    def functiedelogare(self):
        self.userlogat=None
        self.butonlogout1()

     # Register function 
    def functieinregistrare(self):
        print(self.dialogregister.nume.text)
        data=[]
        data.append(self.dialogregister.nume.text)
        data.append(self.dialogregister.prenume.text)
        data.append(self.dialogregister.parola.text)
        data.append(self.dialogregister.email.text)
        self.raspuns=UrlRequest("127.0.0.1:8080", req_body=data, on_failure=self.starepop())
        #self.raspuns = UrlRequest("localhost", on_failure=self.starepop())
        print(self.raspuns.result)
        self.dialogregister.dismiss()


    # comanda = order
    # Function that will send the order to the flask server 
    def butoncomanda(self):
        data=self.cos
        print(data)
        self.raspuns = UrlRequest("127.0.0.1:8080", req_body=data, on_failure=self.starepop())
        self.root.ids.cosx.clear_widgets()
        self.cos=[]
        print(self.cos)

    #Function that deletes the login and register buttons after you login
    def butonlogin1(self):

        self.butonlogout=MDRaisedButton(text="Logout")
        self.butonlogout.bind(on_press=lambda x:self.butonlogout1())

        self.root.ids.toolbar.remove_widget(self.root.ids.login)
        self.root.ids.toolbar.remove_widget(self.root.ids.register)

        if(self.butonlogin != None):
            self.root.ids.toolbar.remove_widget(self.butonlogin)
            self.root.ids.toolbar.remove_widget(self.butonlogin)

        self.root.ids.toolbar.add_widget(self.butonlogout)


    #function that will delete the register button 
    def butonlogout1(self):
        self.butonlogin = MDRaisedButton(text="Login")
        self.butonlogin.bind(on_press=lambda x: self.loginpop())

        self.butonregister = MDRaisedButton(text="Register")
        self.butonregister.bind(on_press=lambda x: self.registerpop())
        self.root.ids.toolbar.remove_widget(self.butonlogout)
        self.root.ids.toolbar.add_widget(self.butonlogin)
        self.root.ids.toolbar.add_widget(self.butonregister)


    contorsecundar=0
    # this function will update the shopping cart 
    #this function get triggered when you add an product from the shopping cart 
    def update_cos(self):
        self.root.ids.cosx.clear_widgets()  # update dinamically the shopping cart 


        contor = 0

        self.root.ids=dict(self.dictionarcos)



        while contor < len(self.cos):
            layout = TwoLineAvatarIconListItem(text=''+self.cos[contor][1]+' '+self.cos[contor][2]+'      '+self.cos[contor][4],
                                               secondary_text=self.cos[contor][3])

            layoutsecundar=IconRightWidget(icon="minus",on_release=lambda x:self.update_cos_dupa_stergere(self.contorix))
            layoutsecundar.bind(on_press= partial(self.butonapasat,layoutsecundar))

            layout.add_widget(layoutsecundar)
            self.root.ids.cosx.add_widget(layout)

            self.root.ids[str(contor + self.contorsecundar)] = layoutsecundar  # adauga layout cu numarul aferent al produsului



            contor=contor+1
    # this function will update the shopping cart 
    #this function get triggered when you add an product from the shopping cart  get triggered when you delete an product from the shopping cart 
    def update_cos_dupa_stergere(self, contor1):
        #print(contor1)
        self.root.ids = dict(self.dictionarcos)

        self.cos.pop(int(contor1))
        print("Contorul care scoate din vector"+contor1)
        self.update_cos()
        print(self.cos)


    def butonapasat(self,instance,layout):



        butondesters=0

        for key, value in self.root.ids.items():

            if str(value)==str(layout):
                print(str(key) + ':' + str(value))
                butondesters=key

            else:
                pass
        self.root.ids.pop(str(key), None)
        self.contorix= butondesters


# Popup that will let you add extra info after you add in shopping cart a new product : " no mushrooms pls " 
    def comentariu_dialog(self,comanda,pret):

        self.dialog.dismiss()
        self.comanda=comanda
        self.pret=pret

        buton=MDFlatButton(text="Comanda")
        buton.bind(on_press=lambda x:self.adauga_cos(self.comanda,self.pret, self.dialog1.observatie.text))


        if not self.dialog1:
            self.dialog1 = Item1(
                text="Observatii:",
                buttons=[
                    buton],
            )

        self.dialog1.open()
        self.dialog1.observatie.text = ''

# Ask you if you want for you product to  be small(mic ) or big(mare) 
    def pizza_dialog(self,pretPizzaMare, pretPizzaMica,source,nume):
        self.dialog=None
        self.nume=nume
        self.source=source
        if not self.dialog:
            self.dialog = MDDialog(
                type="simple",
                items=[
                    Item(text="Mare   "+str(pretPizzaMare)+"Lei", source=source,),
                    Item(text="Mica   "+str(pretPizzaMica)+"Lei", source=source, ),
                ],
            )
        #print(source)
        self.dialog.open()



# General theme and colour of the app 
    def build(self):
        self.theme_cls.primary_palette = "Yellow"
        self.theme_cls.primary_hue = "900"
        #self.theme_cls.
        return main_kv()


Food().run()