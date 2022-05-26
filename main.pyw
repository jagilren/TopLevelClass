# https://www.tutorialspoint.com/create-multiple-buttons-with-different-command-function-in-tkinter
# https://www.geeksforgeeks.org/open-a-new-window-with-a-button-in-python-tkinter/
# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
import requests
import csv
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
from tkinter.constants import DISABLED, NORMAL
import time
from  threading import Thread

class MessageBox(Toplevel):
    def __init__(self ):
        super().__init__(master=master)
        self.btnOK = Button(self,text='OK ',command=self.destroy()) #height=2, width=3
        self.btnOK.pack()

class NewWindow(Toplevel):
    def __init__(self, master=None,boton=None,IDDoor=None, IDAuxOut=None,my_headers=None):
        super().__init__(master=master)
        self.title( boton.cget('text'))
        self.my_headers=my_headers
        self.geometry("400x200")
        self.IDDoor = IDDoor
        self.IDAuxOut = IDAuxOut
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.DoorStatus = '1'
        self.t1 = Thread(target=self.TimeOutforAuxClose, name='t1')
        # Gets the requested values of the height and widht.
        windowWidth = self.winfo_reqwidth() *2
        windowHeight = self.winfo_reqheight() *2
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(self.winfo_screenheight() / 2 - windowHeight / 2)
        self.geometry("+{}+{}".format(positionRight, positionDown))
        print("Width", windowWidth, "Height", windowHeight)
        self.btnAbrir=Button(self,text='Abrir',command=self.AssignProcess) #height=2, width=3
        self.btnAbrir.grid(row=2,column=0, sticky=NS, pady=20) #,
        self.btnCerrar=Button(self,text='Cerrar',command=self.API_Close_door) #height=2, width=3
        self.btnCerrar.grid(row=2,column=1, sticky=NS, pady=20) #,

        self.btnLock = Button(self,text='Bloquear ',command=self.API_AuxButtonClose) #height=2, width=3
        self.btnLock.grid(row=6,column=0, sticky=NS, pady=20) #,

        self.btnUnLock = Button(self,text='Des-Bloquear', command=self.API_AuxButtonNormalOpen) #height=2, width=3
        self.btnUnLock.grid(row=6,column=1, sticky=NS, pady=20) #,

        labelStatusDoor = Label(self, textvariable="Puerta Abierta", relief=RAISED)
        labelStatusDoor.grid(row=7,column=0, pady=20, columnspan=2, rowspan=2,sticky=NSEW)
        labelStatusDoor.config(text="Open_Door")
        print(self.btnUnLock.grid_info())
        self.focus()
        self.grab_set()


    def AssignProcess(self):
        self.btnAbrir.configure(text="Espere...")
        time.sleep(3)
        #MessageBox()
        self.t1.start()
        self.btnAbrir.configure(text="Abrir")
        self.destroy()

    def API_door(self):
        endpoint_Door = 'http://192.168.40.82:8098/api/door/remoteOpenById?' + 'doorId=' + self.IDDoor + \
                       '&interval=1'+ '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        #print(f'url_abrir_cerrar_puerta {endpoint_Door}')
        response = requests.post(endpoint_Door, headers=self.my_headers)
        print(f'Respuesta JSON API_DoorOpen: {response.json()}')

    def API_Close_door(self):
        endpoint_Door = 'http://192.168.40.82:8098/api/door/remoteCloseById?doorId=' + self.IDDoor \
                        + '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        #print(f'url_abrir_cerrar_puerta {endpoint_Door}')
        response = requests.post(endpoint_Door, headers=self.my_headers)
        print(f'Respuesta JSON API_Close_Door: {response.json()}')


    def TimeOutforAuxClose(self):
        print(f'AuxNormalOpen Executed')
        self.API_AuxButtonNormalOpen()
        #Apertura de Puerta
        #self.API_door()
        print(f'Abriendo Puerta')
        #TimeOut for Close Aux Button Recomended 600 secs
        labelQueryResult.config(text="Esperando...", background='black')
        for element in range(10):
            time.sleep(1)
            print(f'Threading Time = {element} AuxClose Exeduted')
        self.API_AuxButtonClose()


    def API_AuxButtonNormalOpen(self):
        endpoint_Aux = 'http://192.168.40.82:8098/api/auxOut/remoteNormalOpenByAuxOutById?id=' + self.IDAuxOut + \
                     '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        response = requests.post(endpoint_Aux, headers=self.my_headers)
        print(f'json response NormalOpenAuxOut:   {response.json()}')

    def API_AuxButtonClose(self):
        endpoint_Aux = 'http://192.168.40.82:8098/api/auxOut/remoteCloseByAuxOutById?id=' + self.IDAuxOut + \
                     '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        response = requests.post(endpoint_Aux, headers=self.my_headers)
        print(f'json response CloseAuxOut:   {response.json()}')

    def btn_Abrir(self):
        self.API_door()
        self.btnAbrir['state'] = DISABLED
        self.btnAbrir.config(cursor="watch")
        self.btnLock.focus()
        self.btnLock.grab_set()
        time.sleep(5)
        self.destroy()
        print(f'HEADERS:   {self.my_headers}')
        print(f'json response abrir:   {response.json()}')

    def API_print(self, response):
        print(f'{response} Tipo de Respuesta {type(response)}')
        print(f'Status Code: {response.status_code}')
        print(f"Headers Content Type: {response.headers['content-type']}")
        print(f'Yeison Final::{response.json()}')

def work():
    print("sleep time start")
    for i in range(10):
        print(i)
        time.sleep(1)
    print("sleep time stop")

def LabelWaiting():
    for tiempo in range(5):
        time.sleep(1)
        print ("Waiting for Change Text Label")
    labelQueryResult.config(text="Esperando...", background='black')


class MTThread(Thread):
    def __init__(self, name = None, target = None):
        self.mt_name = name
        self.mt_target = target
        Thread.__init__(self, name = name, target = target)
    def start(self):
        super().start()
        Thread.__init__(self, name = self.mt_name, target = self.mt_target)
    def run(self):
        super().run()
        Thread.__init__(self, name = self.mt_name, target = self.mt_target)

thread1 = MTThread(name='Labeling',target=LabelWaiting)


def submit(labelQueryResult):
    prefixHab = 'HAB' + hab_var.get()
    IDAuxOut=Dict_AuxOut_ID[prefixHab]
    IDDoor= Dict_Door_ID[prefixHab]
    #print("The Door  is : " + IDDoor)
    #print("The AuxOut is : " + IDAuxOut)
    print(labelQueryResult.cget('text'))
    if (API_Door_Status(IDDoor)== '2'):
        labelQueryResult.config(text=prefixHab + " Puerta está Cerrada", background="green")
    elif (API_Door_Status(IDDoor) == '1'):
        labelQueryResult.config(text=prefixHab  + " Puerta está Abierta", background="red")
    thread1.start()


def API_Door_Status(IDDoor):
    print(f'Api Status Ejecutado, {IDDoor}')
    endpoint_Door = 'http://192.168.40.82:8098/api/door/doorStateById?' + 'doorId=' + IDDoor + \
     '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
    response = requests.get(endpoint_Door, headers=my_headers)
    print(f'json response:   {response.json()}')
    DoorStatus=response.json()['data'][0]['sensor']
    print(f'Estado Sensor Puerta= {DoorStatus}')
    return DoorStatus

def leer_csv(filename):
    fields = []
    rows = {}
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            # door_ids=row.split(",")
            rows[row[0]] = row[1]
    return rows
Dict_Door_ID = leer_csv('doors.txt')
Dict_AuxOut_ID=leer_csv('AuxOut.txt')
global my_headers
my_headers = {'Accept': 'application/json', 'Content-Type': 'application/json','Authorization': 'Basic amFnaWxyZW46VGVtcG9yYWwwMS5hYg=='}
master = Tk()
master.geometry("1140x640")
f = Frame(master)

style = Style()
style.configure('TButton', font =('Tahoma', 10 ),borderwidth = '4')
style.map('TButton', foreground = [('active', '!disabled', ('green'))],background = [('active', 'black')])

style.configure('TFrame',bordercolor='pink',background='#68839B',borderwidth=1)

labelTitleQuery = Label(master, text="Consulta Estado",font=('calibre',11,'bold'), padding=1,foreground="white",background='black')
labelTitleQuery.grid(row=62,column=0,sticky = W,pady=2)
hab_var = StringVar()
hab_entry = Entry(master,textvariable=hab_var, font=('calibre',11,'bold'),width=5)
hab_entry.grid(row=68,column=0,sticky = W)
btnQuery = Button(master, text="OK", padding=1,command=NONE,width=5)
btnQuery.grid(row=70,column=0,sticky = W,pady=2)
btnQuery.bind("<Button>",lambda e, IDDoor=hab_var.get(),IDAuxOut=hab_var.get(): submit(labelQueryResult))
f = Frame(master,style="Custom.TFrame")
f.grid(row=1,column=0)
labelQueryResult = Label(master, text="Esperando...:",font=('calibre',11,'bold'),foreground='white',background='black')
labelQueryResult.grid(row=72,column=0,pady=2,sticky=W,columnspan=20)

radek_line = 2 #Set  ROW  of  matríz of Buttons
bunka_column = 0
for element in Dict_Door_ID.keys():
    state = DISABLED
    if element=='HAB50':
        state=NORMAL
        btn = Button(f,text=element,padding=10,state=state)
        btn.bind("<Button>",
                 lambda e, boton = btn, IDDoor=Dict_Door_ID[btn.cget('text')], IDAuxOut=Dict_AuxOut_ID[btn.cget('text')]: NewWindow(master, boton, IDDoor, IDAuxOut,my_headers))
    else:
        btn = Button(f,text=element,padding=10,state=state)

    btn.grid(row=radek_line, column=bunka_column,padx=2,pady=2,sticky=W)

    bunka_column += 1
    if bunka_column == 10:  # changed this variable to make it easier to test code.
        bunka_column = 0
        radek_line += 1
master.title('Apertura Puertas Motel Classic')
master.config(bg='#68839B')
p1 = PhotoImage(file ='RAM4GB.png')
p1=master.iconphoto(True, p1)
"""sb = Scrollbar(f,orient=VERTICAL)
sb.grid(row=0, column=15, sticky=NS)"""
master.mainloop()


"""doorIDs = [str(x) for x in range(1,79,1)]
AuxOutIDs=[str(x) for x in range(1, 79, 1)]
doorIDs[49] =    '4028a8d27eb6046b017eb60684ad0164'
AuxOutIDs[49] = '4028a8d27eb6046b017eb60684b90174'
list_textButton = ['HAB' + str(x).zfill(2) for x in range(1, 79, 1)]
for index,element in enumerate(list_textButton):
    Dict_Door_ID[element]= str(doorIDs[index])
for index,element in enumerate(list_textButton):
    Dict_AuxOut_ID[element]= str(AuxOutIDs[index])

        # if self.DoorStatus == '1':
        #     url_puerta = 'http://192.168.40.82:8098/api/door/remoteOpenById?' + 'doorId=' + self.IDDoor + \
        #                '&interval=1'+ '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        #     response = requests.post(url_puerta, headers=my_headers)
        #     print(f'json response abrir:   {response.json()}')
        # elif self.DoorStatus=='2':
        #     url_puerta = 'http://192.168.40.82:8098/api/door/remoteCloseById?' + 'doorId=' + self.IDDoor + \
        #                '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        #     response = requests.post(url_puerta, headers=my_headers)
        #     print(f'json response cerrar:   {response.json()}')
        # else:
        #     pass


"""