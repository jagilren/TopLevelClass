# https://www.tutorialspoint.com/create-multiple-buttons-with-different-command-function-in-tkinter
# https://www.geeksforgeeks.org/open-a-new-window-with-a-button-in-python-tkinter/
# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
import requests
import csv
import time
from tkinter import *
from tkinter.ttk import *
from tkinter.constants import DISABLED, NORMAL

class NewWindow(Toplevel):
    import time
    def __init__(self, master=None,boton=None,IDDoor=None, IDAuxOut=None):
        super().__init__(master=master)
        self.title(IDAuxOut + "_"*1 + boton.cget('text'))
        self.geometry("400x200")
        self.IDDoor = IDDoor
        self.IDAuxOut = IDAuxOut
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
        self.btnAbrir=Button(self,text='Abrir',style="Custom.TButton",command=self.API_door) #height=2, width=3
        self.btnAbrir.grid(row=2,column=0, sticky=NS, pady=20) #,
        ###btnAbrir.bind("<Button-1>",lambda x=1: self.API_status)
        ###btnAbrir.bind('<Return>', self.API_door, add='+')
        self.btnCerrar=Button(self,text='Cerrar',style="Custom.TButton",command=self.API_door) #height=2, width=3
        self.btnCerrar.grid(row=2,column=1, sticky=NS, pady=20) #,

        self.btnLock = Button(self,text='Bloquear ', style="Custom.TButton",command=self.API_AuxButtonClose) #height=2, width=3
        self.btnLock.grid(row=6,column=0, sticky=NS, pady=20) #,

        self.btnUnLock = Button(self,text='Des-Bloquear', style="Custom.TButton", command=self.API_AuxButtonNormalOpen) #height=2, width=3
        self.btnUnLock.grid(row=6,column=1, sticky=NS, pady=20) #,

        labelStatusDoor = Label(self, textvariable="Puerta Abierta", relief=RAISED)
        labelStatusDoor.grid(row=7,column=0, pady=20, columnspan=2, rowspan=2,sticky=NSEW)
        labelStatusDoor.config(text="Open_Door")
        print(self.btnUnLock.grid_info())
        self.focus()
        self.grab_set()


    my_headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
                  'Authorization': 'Basic amFnaWxyZW46VGVtcG9yYWwwMS5hYg=='}

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

    def API_door(self):
        endpoint_Door = 'http://192.168.40.82:8098/api/door/remoteOpenById?' + 'doorId=' + self.IDDoor + \
                       '&interval=1'+ '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        print(f'url_abrir_cerrar_puerta {endpoint_Door}')
        response = requests.post(endpoint_Door, headers=self.my_headers)
        self.btnAbrir['state'] = DISABLED
        self.btnAbrir.config(cursor="watch")
        self.btnLock.focus()
        self.btnLock.grab_set()
        time.sleep(2)
        self.btnAbrir['state'] = NORMAL
        self.btnAbrir.config(cursor="arrow")
        self.destroy()
        print(f'HEADERS:   {self.my_headers}')
        print(f'json response abrir:   {response.json()}')
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

    def API_print(self, response):
        print(f'{response} Tipo de Respuesta {type(response)}')
        print(f'Status Code: {response.status_code}')
        print(f"Headers Content Type: {response.headers['content-type']}")
        print(f'Yeison Final::{response.json()}')


def submit(labelQueryResult):
    prefixHab = 'HAB' + hab_var.get()
    IDAuxOut=Dict_AuxOut_ID[prefixHab]
    IDDoor= Dict_Door_ID[prefixHab]
    #print("The Door  is : " + IDDoor)
    #print("The AuxOut is : " + IDAuxOut)
    print(labelQueryResult.cget('text'))
    if (API_status(IDDoor)=='0'):
        labelQueryResult.config(text=prefixHab + " Puerta está Cerrada", background="green")
    elif (API_status(IDDoor)=='1'):
        labelQueryResult.config(text=prefixHab  + " Puerta está Abierta", background="red")



def API_status(IDDoor):
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
my_headers = {'Accept': 'application/json', 'Content-Type': 'application/json','Authorization': 'Basic amFnaWxyZW46VGVtcG9yYWwwMS5hYg=='}
master = Tk()
master.geometry("1440x640")

style = Style(master)
style.configure('Custom.TButton', font=('Sanserif', 11),bordercolor='#00FF00',background='#0000FF',borderwidth=4)

labelTitleQuery = Label(master, text="Consulta Estado",font=('calibre',11,'bold'), padding=1,foreground="white",background='black')
labelTitleQuery.grid(row=62,column=0,sticky = W,pady=2)
hab_var = StringVar()
hab_entry = Entry(master,textvariable=hab_var, font=('calibre',11,'bold'),width=5)
hab_entry.grid(row=68,column=0,sticky = W)
btnQuery = Button(master, text="OK", padding=1,command=NONE,width=5)
btnQuery.grid(row=70,column=0,sticky = W,pady=2)
btnQuery.bind("<Button>",lambda e, IDDoor=hab_var.get(),IDAuxOut=hab_var.get(): submit(labelQueryResult))

labelQueryResult = Label(master, text="Resultado:",font=('calibre',11,'bold'),foreground='white',background='black')
labelQueryResult.grid(row=72,column=0,pady=2,sticky=W)

radek_line = 10 #Set  ROW  of  matríz of Buttons
bunka_column = 0
for element in Dict_Door_ID.keys():
    state = DISABLED
    if element=='HAB50':
        state=NORMAL
        btn = Button(master,
                 text=element,padding=10,state=state,style="Custom.TButton")
        btn.bind("<Button>",
                 lambda e, boton = btn, IDDoor=Dict_Door_ID[btn.cget('text')], IDAuxOut=Dict_AuxOut_ID[btn.cget('text')]: NewWindow(master, boton, IDDoor, IDAuxOut))
    else:
        btn = Button(master,
                 text=element,padding=10,state=state,style="Custom.TButton")

    btn.grid(row=radek_line, column=bunka_column,padx=2,pady=2)

    bunka_column += 1
    if bunka_column == 10:  # changed this variable to make it easier to test code.
        bunka_column = 0
        radek_line += 1


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

"""