# https://www.tutorialspoint.com/create-multiple-buttons-with-different-command-function-in-tkinter
# https://www.geeksforgeeks.org/open-a-new-window-with-a-button-in-python-tkinter/
# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
import requests
import time
from tkinter import *

from tkinter.ttk import *
from tkinter.constants import DISABLED, NORMAL


class NewWindow(Toplevel):
    import time
    def __init__(self, master=None,boton=None,Identificador=None):
        super().__init__(master=master)
        self.title(Identificador + "_"*5  +boton.cget('text'))
        self.geometry("400x200")
        self.Identificador=Identificador
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.DoorStatus = '1'
        # Gets the requested values of the height and widht.
        windowWidth = self.winfo_reqwidth() *2
        windowHeight = self.winfo_reqheight() *2
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(self.winfo_screenheight() / 2 - windowHeight / 2)
        self.geometry("+{}+{}".format(positionRight, positionDown))
        print("Width", windowWidth, "Height", windowHeight)

        label = Label(self, text=" " +  boton.cget('text'),font='arial')
        label.config(font=("Tahoma", 20))
        label.grid(row=0,column=0,rowspan=2,sticky=NS)
        self.btnAbrir=Button(self,text='Abrir',style="Custom.TButton",command=self.API_door) #height=2, width=3
        self.btnAbrir.grid(row=2,column=0, sticky=NS, pady=20) #,
        ##btnAbrir.bind("<Button-1>",lambda x=1: self.API_status)
        ##btnAbrir.bind('<Return>', self.API_door, add='+')
        self.btnLock=Button(self,text='Bloquear ',style="Custom.TButton",command=self.API_status) #height=2, width=3
        self.btnLock.grid(row=6,column=0, sticky=NS, pady=20) #,
        btnUnLock=Button(self,text='Des-Bloquear',style="Custom.TButton",command=self.API_status) #height=2, width=3
        btnUnLock.grid(row=6,column=1, sticky=NS, pady=20) #,

        self.focus()
        self.grab_set()


    my_headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
                  'Authorization': 'Basic amFnaWxyZW46VGVtcG9yYWwwMS5hYg=='}

    def API_door(self):
        endpoint_Door = 'http://192.168.40.82:8098/api/door/remoteOpenById?' + 'doorId=' + self.Identificador + \
                       '&interval=1'+ '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        print(f'url_abrir_cerrar_puerta {endpoint_Door}')
        response = requests.post(endpoint_Door, headers=self.my_headers)
        self.btnAbrir['state'] = DISABLED
        self.btnAbrir.config(cursor="heart")
        self.btnLock.focus()
        self.btnLock.grab_set()
        time.sleep(5)
        self.btnAbrir['state'] = NORMAL
        self.btnAbrir.config(cursor="arrow")
        self.destroy()
        print(f'HEADERS:   {self.my_headers}')
        print(f'json response abrir:   {response.json()}')
        # if self.DoorStatus == '1':
        #     url_puerta = 'http://192.168.40.82:8098/api/door/remoteOpenById?' + 'doorId=' + self.Identificador + \
        #                '&interval=1'+ '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        #     response = requests.post(url_puerta, headers=my_headers)
        #     print(f'json response abrir:   {response.json()}')
        # elif self.DoorStatus=='2':
        #     url_puerta = 'http://192.168.40.82:8098/api/door/remoteCloseById?' + 'doorId=' + self.Identificador + \
        #                '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        #     response = requests.post(url_puerta, headers=my_headers)
        #     print(f'json response cerrar:   {response.json()}')
        # else:
        #     pass

    def API_status(self):
        endpoint_Door = 'http://192.168.40.82:8098/api/door/doorStateById?' + 'doorId=' + self.Identificador + \
                     '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        response = requests.get(endpoint_Door, headers=self.my_headers)
        print(f'json response:   {response.json()}')
        self.DoorStatus=response.json()['data'][0]['sensor']
        print(f'Estado Sensor Puerta= {self.DoorStatus}')
        # if self.DoorStatus == '1':
        #      btnAbrir.config(text='Abrir Puerta',command=self.API_door)
        # elif self.DoorStatus == '2':
        #     btnAbrir.config(text='Cerrar Puerta',command=self.API_door)
        # return btnAbrir

    def API_AuxButton(self):
        endpoint_Aux = 'http://192.168.40.82:8098/api/door/doorStateById?' + 'doorId=' + self.Identificador + \
                     '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        response = requests.post(endpoint_Aux, headers=self.my_headers)
        print(f'json response Aux:   {response.json()}')

    def API_print(self, response):
        print(f'{response} Tipo de Respuesta {type(response)}')
        print(f'Status Code: {response.status_code}')
        print(f"Headers Content Type: {response.headers['content-type']}")
        print(f'Yeison Final::{response.json()}')







doorIDs = [str(x) for x in range(1,79,1)]
doorIDs[49] = '4028a8d27eb6046b017eb60684ad0164'



Dict_seznamTextu={}
seznamTextu = ['HAB' + str(x).zfill(2) for x in range(1, 79, 1)]
for index,element in enumerate(seznamTextu):
    Dict_seznamTextu[element]= str(doorIDs[index])

master = Tk()
master.geometry("1440x640")

style = Style(master)
style.configure('Custom.TButton', font=('Sanserif', 11),bordercolor='#00FF00',background='#0000FF',borderwidth=4)

label = Label(master, text="Main window Motel Classic")
label.grid(row=60,column=3,rowspan=2,columnspan=5)
radek = 10
bunka = 0
for element in seznamTextu:
    state=DISABLED
    if element=='HAB50':
        state=NORMAL
        btn = Button(master,
                 text=element,padding=20,state=state,style="Custom.TButton")
        btn.bind("<Button>",
             lambda e,boton=btn,Identificador=Dict_seznamTextu[btn.cget('text')]: NewWindow(master, boton, Identificador))
    else:
        btn = Button(master,
                 text=element,padding=20,state=state,style="Custom.TButton")

    btn.grid(row=radek, column=bunka)

    bunka += 1
    if bunka == 10:  # changed this variable to make it easier to test code.
        bunka = 0
        radek += 1

master.mainloop()