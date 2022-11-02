# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from sys import exit
import requests
import csv
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import *
import tkinter.font as font
import tkinter.messagebox
from tkinter.constants import DISABLED, NORMAL
import time, datetime
from threading import Thread
import os
from subprocess import *
import subprocess


class DelayRouteOpenGaraje(Toplevel):
    def __init__(self):
        super().__init__(master=master)
        self.btnOK = Button(self, text='OK ', command=self.destroy())  # height=2, width=3
        self.btnOK.pack()
        self.lblAViso = Label(self, text='GARAJE EN RECORRIDO DE APERTURA \n ESPERA UNOS SEGUNDOS MÁS')
        self.lblAViso.pack()
        global boolGarageInRouteOpen
        self.threadDelayRouteOpen = Thread(target=self.DelayRouteOpen(), name='threadDelayRouteOpen')

class WindowOPenendDoors(Toplevel):
    def __init__(self):
        print('Clase Creada')
        pass
class NewWindow(Toplevel):
    def __init__(self, master=None, boton=None, hab_ENTRY=None, IDDoor=None, IDAuxOut=None, DoorType=None, my_headers=None):
        global boolGarageInRouteOpen
        super().__init__(master=master)
        self.grab_set()
        self.focus()
        self.title(boton.cget('text'))
        self.my_headers = my_headers
        self.geometry("400x200")
        self.boton = boton
        self.hab_ENTRY=hab_ENTRY
        self.IDDoor = IDDoor
        self.IDAuxOut = IDAuxOut
        self.DoorType = DoorType
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.DoorStatus = '1'
        self.threadAssign = Thread(target=self.DoorOpen_ButtonOpen_ButtonClose, name='threadAssign')
        self.threadCloseGarage = Thread(target=self.GarageStatus_GarageClose, name='threadCloseGarage')
        self.threadUnBlock = Thread(target=self.ButtonOpen_ButtonClose, name='threadUnBlock')
        self.threadBlock = Thread(target=self.ButtonClose, name='threadBlock')
        self.threadDelayRouteOpen = Thread(target=DelayRouteOpenOrClose, args=(self.boton,), name='threadDelayRouteOpen')
        print(f'Estado de Recorrido de la puerta {boton} = {not(boolGarageInRouteOpen)}')
        #Cambia el Texto de la EntryBox de Habitación para consulta de estado Rápido luego de salir de la Ventana
        self.hab_ENTRY.delete(0, END)
        self.hab_ENTRY.insert(0,self.boton.cget('text')[3:5])

        self.bind('<Escape>', lambda e: close_win(e))

        def close_win(e):
            self.destroy()

        # Gets the requested values of the height and widht.
        windowWidth = self.winfo_reqwidth() * 2
        windowHeight = self.winfo_reqheight() * 2
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(self.winfo_screenheight() / 2 - windowHeight / 2)
        self.geometry("+{}+{}".format(positionRight, positionDown))
        print("Width", windowWidth, "Height", windowHeight)
        self.btnAbrir = Button(self, text='Abrir', command=self.AssignProcess)  # height=2, width=3
        self.btnAbrir.grid(row=2, column=0, sticky=NS, pady=20)  # ,
        if DoorType == 'SEDAN':
            self.btnCerrar = Button(self, text='Cerrar', command=self.CloseGarageProcess,
                                    state='ENABLED')  # height=2, width=3
            self.btnCerrar.grid(row=2, column=1, sticky=NS, pady=20)

        self.btnLock = Button(self, text='Bloquear ', command=self.BlockProcess)  # height=2, width=3
        self.btnLock.grid(row=6, column=0, sticky=NS, pady=20)  # ,

        self.btnUnLock = Button(self, text='Des-Bloquear', command=self.UnBlockProcess)  # height=2, width=3
        self.btnUnLock.grid(row=6, column=1, sticky=NS, pady=20)  # ,

        labelStatusDoor = Label(self, textvariable="Puerta Abierta", relief=RAISED)
        labelStatusDoor.grid(row=7, column=0, pady=20, columnspan=2, rowspan=2, sticky=NSEW)
        labelStatusDoor.config(text="Open_Door")
        print(self.btnUnLock.grid_info())
        self.grab_set()
        self.focus()
    def Write_logListBox(self, texto):
        ct = datetime.datetime.now()
        logListBox.insert(0, self.boton.cget('text') + texto + ' ' + str(ct).split('.')[0])

    def foreground_logListBox(self, colorista):
        ct = datetime.datetime.now()
        logListBox.itemconfigure(0, background="skyblue4", foreground=colorista)

    def AssignProcess(self):
        self.threadAssign.daemon = True
        self.threadAssign.start()
        time.sleep(3) # Para asegurarse que la ventana emergente PACIENCIA si se active
        self.destroy()
        time.sleep(2) #Para que no se den Click super rápido en otro botón


    def CloseGarageProcess(self):
        self.threadCloseGarage.daemon = True
        self.threadCloseGarage.start()
        time.sleep(3)  # Para asegurarse que la ventana emergente PACIENCIA si se active
        self.destroy()
        # classthreadCloseDoor = MTThread(name='Labeling', target=self.VerifyStatusDoor_CloseDoor)
        # classthreadCloseDoor
        # classthreadCloseDoor.start()

    def UnBlockProcess(self):
        self.threadUnBlock.daemon = True
        self.threadUnBlock.start()
        self.Write_logListBox('--- DES-BLOQUEADA ---')
        self.foreground_logListBox("goldenrod1")
        threadLabelWaiting = MTThread(name='Labeling', target=LabelWaiting)
        threadLabelWaiting.start()
        self.destroy()

    def BlockProcess(self):
        self.threadBlock.daemon = True
        self.threadBlock.start()
        self.Write_logListBox('--- BLOQUEADA ---')
        self.foreground_logListBox("SeaGreen1")
        threadLabelWaiting = MTThread(name='Labeling', target=LabelWaiting)
        threadLabelWaiting.start()
        self.destroy()

    def API_door(self):
        endpoint_Door = 'http://' + Dict_Ini_Params[
            'IPV4AddressServer'] + '/api/door/remoteOpenById?' + 'doorId=' + self.IDDoor + \
                        '&interval=1' + '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        # print(frame_buttons'url_abrir_cerrar_puerta {endpoint_Door}')
        response = requests.post(endpoint_Door, headers=self.my_headers)
        print(f'Respuesta JSON API_DoorOpen: {response.json()}')

    def API_Close_door(self):
        endpoint_Door = 'http://' + Dict_Ini_Params[
            'IPV4AddressServer'] + '/api/door/remoteCloseById?doorId=' + self.IDDoor \
                        + '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        # print(frame_buttons'url_abrir_cerrar_puerta {endpoint_Door}')
        response = requests.post(endpoint_Door, headers=self.my_headers)
        print(f'Respuesta JSON API_Close_Door: {response.json()}')

    def VerifyStatusDoor_CloseDoor(self):
        if API_Door_Status(self.IDDoor) == '2':  # Verificamos que está abierta
            print(f'Cerrando Garaje Sedan')
            self.API_door()  # Enviamos Pulso de Abrir Garaje para que esta se Cierre, pues la API Door/remote_Close_ByID no cierra la puerta
        else:
            print("Garaje Ya Esta Cerrada.  No se Ejecuta la acción")

    def ButtonOpen_ButtonClose(self):
        ResponseButtonOpen = self.API_AuxButtonNormalOpen()
        if ResponseButtonOpen == 'success':
            labelQueryResult.config(text=self.boton.cget('text') + " Desbloqueda", background='red')

        for element1 in range(int(Dict_Ini_Params['TimeOutButtonNormalOpen'])):
            time.sleep(1)
            #print(frame_buttons'Threading Time = {element1} Waiting for AuxClose Execute threadUnBlockProcess')
        ResponseButtonClose = self.API_AuxButtonClose()
        # threadButtonClose = MTThread(name='ClosingButton', target=self.API_AuxButtonClose)
        # threadButtonClose.start()
        self.destroy()

    def GarageStatus_GarageClose(self):
        if API_Door_Status(self.IDDoor) == '2':
            print(f'Garaje Abierto....Cerrando Garaje')
            self.threadDelayRouteOpen.daemon = True
            self.threadDelayRouteOpen.start()

            try:
                self.API_door()  # Cierra la puerta  para SEDAN si está abierta. Con comando de Abrir por caprichos de ZKT
                self.Write_logListBox('--- CERRANDO GARAJE ---')
                self.foreground_logListBox("SeaGreen1")
            except:
                print('Error en API de Cerrado de Garaje')
        else:
            print("GARAJE Ya está Cerrada.  No se ejecuta la acción")
            self.Write_logListBox('--- GARAJE YA ESTÁ CERRADO ---')
            self.foreground_logListBox("orchid1")

    def DoorOpen_ButtonOpen_ButtonClose(self):
        # Vamos a Revisar si el garaje está Abierto
        if Dict_Door_Type[self.boton.cget('text')] == 'SEDAN':
            if API_Door_Status(self.IDDoor) == '1':  #1 SIGNIGFICA CERRADA
                print(f'GARAJE en recorrido de Apertura')
                try:
                    self.threadDelayRouteOpen.daemon = True
                    self.threadDelayRouteOpen.start()
                    self.API_door()  # Abre si está cerrada para SEDAN
                except:
                    print('Error en API_Door, Revise API desde la Plataforma ZKT')

            else:
                print("GARAJE Ya está Abierta.  No se ejecuta la acción")
                self.Write_logListBox('--- GARAJE YA ESTÁ ABIERTO ---')
                self.foreground_logListBox("orchid1")
        else:  # Si es Moto o Peaton
            self.API_door()  # Abre de una si es moto o peaton sin importar estado de la puerta
            print(f'Wait...02 seconds for AuxNormalOpen Execution')
            time.sleep(2)
            # self.API_door()  # Repite pulso apertura  para Cantoneras desobedientes
        time.sleep(2)
        print(f'Wait...02 seconds for AuxNormalOpen Execution')
        self.API_AuxButtonNormalOpen()
        self.Write_logListBox(f'--- {self.boton.cget("text")} DESBLOQUEADA ---')
        self.foreground_logListBox("goldenrod1")
        time.sleep(2)
        if Dict_Door_Type[self.boton.cget('text')] == 'SEDAN':
            if API_Door_Status(self.IDDoor) == '2':
                self.Write_logListBox(f'--- GARAJE {self.boton.cget("text")}  ESTÁ ABIERTO  ---')
                self.foreground_logListBox("goldenrod1")
            else:  # Si no cambió el estado del Sensor
                self.Write_logListBox('--- GARAJE PERMANECIO CERRADA ---')
                self.foreground_logListBox("pink")
        else:  # Si es Moto o Peaton
            self.Write_logListBox('--- ABRIÓ GARAJE ---')
            self.foreground_logListBox("goldenrod1")

        labelQueryResult.config(text="Esperando...", background='black')
        for element in range(int(Dict_Ini_Params['TimeOutButtonNormalOpen'])):
            time.sleep(1)
            #print(frame_buttons'Threading Time = {element} AuxClose Next to Execute threadAssignProcess')
        self.API_AuxButtonClose()
        self.Write_logListBox('--- BLOQUEADA ---')
        self.foreground_logListBox("SeaGreen1")

    def ButtonClose(self):
        ResponseButtonClose = self.API_AuxButtonClose()
        if ResponseButtonClose == 'success':
            labelQueryResult.config(text=self.boton.cget('text') + " Bloqueada", background='green')
        threadLabelWaiting = MTThread(name='Labeling', target=LabelWaiting)
        threadLabelWaiting.start()
        self.destroy()

    def API_AuxButtonNormalOpen(self):
        endpoint_Aux = 'http://' + Dict_Ini_Params[
            'IPV4AddressServer'] + '/api/auxOut/remoteNormalOpenByAuxOutById?id=' + self.IDAuxOut + \
                       '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        response = requests.post(endpoint_Aux, headers=self.my_headers)
        print(f'json response NormalOpenAuxOut:   {response.json()}')
        return response.json()['message']
        time.sleep(5)

    def API_AuxButtonClose(self):
        endpoint_Aux = 'http://' + Dict_Ini_Params[
            'IPV4AddressServer'] + '/api/auxOut/remoteCloseByAuxOutById?id=' + self.IDAuxOut + \
                       '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
        response = requests.post(endpoint_Aux, headers=self.my_headers)
        print(f'json response CloseAuxOut:   {response.json()}')
        return response.json()['message']

    def btn_Abrir(self):
        self.API_door()
        self.btnAbrir['state'] = DISABLED
        self.btnAbrir.config(cursor="watch")
        self.btnLock.focus()
        self.btnLock.grab_set()
        time.sleep(5)
        self.destroy()
        print(f'HEADERS:   {self.my_headers}')
        # print(frame_buttons'json response abrir:{response.json()}')

    def API_print(self, response):
        print(f'{response} Tipo de Respuesta {type(response)}')
        print(f'Status Code: {response.status_code}')
        print(f"Headers Content Type: {response.headers['content-type']}")
        print(f'Yeison Final::{response.json()}')


def DelayRouteOpenOrClose(btn):
    boolGarageInRouteOpen = True
    btn.bind("<Button>",
             lambda e: messagebox.showinfo("Paciencia","Garaje en recorrido 'PACIENCIA'"))
    print (f'Cambió Bind para <Button> {btn.cget("text")}')
    print (f'Thead Delay Route Open Garage Iniciado durante {int(Dict_Ini_Params["DelayRouteOpenGaraje_Secs"])}')
    time.sleep(int(Dict_Ini_Params["DelayRouteOpenGaraje_Secs"])) # Demora de la Apertura Total del Garage
    boolGarageInRouteOpen = False
    btn.bind("<Button>",
             lambda e, boton=btn, IDDoor=Dict_Door_ID[btn.cget('text')], IDAuxOut=Dict_AuxOut_ID[btn.cget('text')],
                    DoorType=Dict_Door_Type[btn.cget('text')]: NewWindow(master, boton, IDDoor, IDAuxOut, DoorType,
                                                                         my_headers))


def validate_entry(text, new_text):
    try:
        if not (new_text):
            return TRUE
        if len(new_text) > 2:
            return FALSE
        if int(new_text) > 78:
            return FALSE
        return text.isdecimal()
    except:
        hab_ENTRY.config(text="")
        return FALSE

    finally:
        print(f'Entraste al finally')

def LabelWaiting():
    for tiempo in range(5):
        time.sleep(1)
        print("Waiting for Change Text Label")
    labelQueryResult.config(text="Esperando...", background='black')

class MTThread(Thread):
    def __init__(self, name=None, target=None):
        self.mt_name = name
        self.mt_target = target
        Thread.__init__(self, name=name, target=target)
        print("name en def __init__", name)

    def start(self):
        super().start()
        Thread.__init__(self, name=self.mt_name, target=self.mt_target)

    def run(self):
        super().run()
        Thread.__init__(self, name=self.mt_name, target=self.mt_target)


threadLabelWaiting = MTThread(name='Labeling', target=LabelWaiting)
def submitQuery(labelQueryResult, BioSecurityStatus):
    if not (hab_var.get()):
        return
    if BioSecurityStatus == False:
        infoconexion = messagebox.showinfo("Error de Conexión", "Servidor de Puertas Desconectado \n Verifique RED")
        return
    prefixHab = 'HAB0' + hab_var.get() if len(hab_var.get()) == 1 else 'HAB' + hab_var.get()
    IDAuxOut = Dict_AuxOut_ID[prefixHab]
    IDDoor = Dict_Door_ID[prefixHab]
    typeDoor = Dict_Door_Type[prefixHab]
    Dict_DoorType_Sinonyms = {'MOTO': 'PUERTA', 'SEDAN': 'GARAJE', 'HIBRIDO':'PUERTA'}
    messagePrefix = Dict_DoorType_Sinonyms[typeDoor]

    if (API_Door_Status(IDDoor) == '1'):
        labelQueryResult.config(text=prefixHab + " " + messagePrefix + " está Cerrada(o)", background="green")
    elif (API_Door_Status(IDDoor) == '2'):
        labelQueryResult.config(text=prefixHab + " " + messagePrefix + " está Abierta(o)", background="red")
    elif (API_Door_Status(IDDoor) not in ['1', '2']):
        labelQueryResult.config(text=prefixHab + " Estado del Sensor Desconocido", background="purple")
    threadLabelWaiting.start()

def API_Door_Status(IDDoor):
    print(f'Api Status Ejecutado, {IDDoor}')
    endpoint_Door = 'http://' + Dict_Ini_Params['IPV4AddressServer'] + '/api/door/doorStateById?' + 'doorId=' + IDDoor + \
                    '&access_token=17F6FBF25F23BFC07BD133624B1B76AF60D589B72C7F3F2E0C99CB940D3E6DD0'
    try:
        response = requests.get(endpoint_Door, headers=my_headers)
        print(f'json response:   {response.json()}')
        DoorStatus = response.json()['data'][0]['sensor']
        print(f'Estado Sensor Puerta= {DoorStatus}')
        return DoorStatus
    except:
        return "Puerta  o Garaje Inexistente"

# Specify path
def VerificaTXT(filetxt):
    isExist = os.path.exists(filetxt)
    return isExist

def CheckAllFilesExist(queryexist=True):
    list_configFiles = ['./AuxOut.txt', './doors.txt', './RAM4GB.png']
    for ConfigFiles in list_configFiles:
        queryexist = queryexist * VerificaTXT(ConfigFiles)
    if (queryexist):
        pass
    else:
        master.destroy()


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

boolGarageInRouteOpen = False
intCountWarningConnectivy=0
Dict_Door_ID = leer_csv('doors.txt')
Dict_AuxOut_ID = leer_csv('AuxOut.txt')
Dict_Door_Type = leer_csv('doors_type.txt')
Dict_Ini_Params = leer_csv('zkt.ini')

global my_headers
my_headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
              'Authorization': 'Basic amFnaWxyZW46VGVtcG9yYWwwMS5hYg=='}
BioSecurityStatus = False
master = Tk()
master.geometry(
    "1140x900+0+0")  # se pone x x in lowercase para significar pixeles.  Y los ceros para desplazar 0 Unidades desde el left top corner

frame_buttons = Frame(master)
f_foot = Frame(master)

style = Style()
style.configure('TButton', font=('Tahoma', 10), borderwidth='4',background='black',foreground='black',highlightthickness='20')
#style_Garaje = {'fg': 'black', 'bg': 'SlateBlue2', 'activebackground':'SlateBlue2', 'activeforeground': 'SlateBlue2'}
#style.configure('TButton', **style_Garaje)
style.map('TButton', foreground=[('active','!disabled', ('magenta'))], background=[('active', 'black')])
styleButtonGaraje =Style()
styleButtonGaraje.configure('small.TButton', font=('Tahoma', 8, 'bold'), background="red",foreground='orange red')
styleButtonGaraje.configure('sedan.TButton', font=('Tahoma', 10), background="black",foreground='blue')
styleButtonGaraje.configure('moto.TButton', font=('Tahoma', 10), background="red",foreground='orange red')


style.configure('TFrame', bordercolor='pink', background='#68839B', borderwidth=1)

labelTitleQuery = Label(f_foot, text="Consulta Estado", font=('calibre', 11, 'bold'), padding=1, foreground="white",
                        background='black')
labelTitleQuery.grid(row=62, column=0, sticky=W, pady=2)

hab_var = StringVar()

frame_buttons = Frame(master, style="Custom.TFrame")
frame_buttons.grid(row=0, column=0)

f_foot = Frame(master)
#Ponerlo en Column 0 Garantiza que se posiciona en la Izquierda
f_foot.grid(row=70, column=0, columnspan=20, sticky=NS) #

f_query = Frame(f_foot)
f_query.grid(columns=1, row=0,columnspan=5,sticky=W) #,

f_openedDoors = Frame(f_foot)
f_openedDoors.grid(columns=7, row=0) #,

hab_ENTRY = Entry(f_query, textvariable=hab_var, font=('calibre', 11, 'bold'), width=5, validate="key",
                  validatecommand=(master.register(validate_entry), "%S", "%P"))
hab_ENTRY.grid(row=0, column=0, sticky=W) #
btnQuery = Button(f_query, text="CONSULTAR", padding=1, command=NONE, width=15)
btnQuery.grid(row=1, column=0, pady=2, sticky=W) #
btnQuery.bind("<Button>",
              lambda e, IDDoor=hab_var.get(), IDAuxOut=hab_var.get(): submitQuery(labelQueryResult, BioSecurityStatus))
btnQuery.bind('<Return>',
              lambda e, IDDoor=hab_var.get(), IDAuxOut=hab_var.get(): submitQuery(labelQueryResult, BioSecurityStatus))
btnQOpenedDoors =Button(f_openedDoors, text="PUERTAS ABIERTAS", padding=1, command=NONE, width=18,style="small.TButton")
btnQOpenedDoors.grid(row=2, column=6, pady=2)
btnQOpenedDoors.bind("<Button>",lambda e, IDDoor=hab_var.get(), IDAuxOut=hab_var.get(): submitQuery(labelQueryResult, BioSecurityStatus))
myFont = font.Font(family='Helvetica')

global logListBox
logListBox = Listbox(f_foot, width=120, height=20)
logListBox.grid(column=0,row=5,rowspan=2, columnspan=20,sticky=W)
logListBox.configure(background="skyblue4", foreground="white", font=('Aerial 13'))


#btnQOpenedDoors['font']=myFont



labelQueryResult = Label(f_query, text="Esperando...:", font=('calibre', 11, 'bold'), foreground='white',
                         background='black')
labelQueryResult.grid(row=3, column=0, pady=2, sticky=W)

radek_line = 2  # Set  ROW  of  matríz of Buttons
bunka_column = 0
for element in Dict_Door_ID.keys():
    state = DISABLED

    if len(Dict_Door_ID[element]) == 32:
        state = NORMAL
        if (Dict_Door_Type[element]=='SEDAN'):
            btn = Button(frame_buttons, text=element, padding=10, state=state, style="TButton")

        elif (Dict_Door_Type[element]=='MOTO' or Dict_Door_Type[element]=='HIBRIDO'):
            btn = Button(frame_buttons, text=element, padding=10, state=state, style="moto.TButton")

        btn.bind("<Button>",
                 lambda e, boton=btn, IDDoor=Dict_Door_ID[btn.cget('text')], IDAuxOut=Dict_AuxOut_ID[btn.cget('text')],
                        DoorType=Dict_Door_Type[btn.cget('text')]: NewWindow(master, boton, hab_ENTRY, IDDoor, IDAuxOut,
                                                                             DoorType,
                                                                             my_headers))
    else:
        btn = Button(frame_buttons, text='...', padding=10, state=state)

    btn.grid(row=radek_line, column=bunka_column, padx=2, pady=2, sticky=W)

    bunka_column += 1
    if bunka_column == 10:  # changed this variable to make it easier to test code.
        bunka_column = 0
        radek_line += 1
master.title('Apertura Puertas y Garajes Motel Classic')
master.config(bg='#68839B')
p1 = PhotoImage(file='RAM4GB.png')
p1 = master.iconphoto(True, p1)


def checkPing():
    global BioSecurityStatus
    my_address = Dict_Ini_Params['IPV4AddressServer'].split(':')[0]
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    output = Popen(["ping", "-n", "2", my_address], startupinfo=startupinfo, stdout=PIPE).communicate()[0]
    if output.find(b'tiempo') > 0:
        BioSecurityStatus = True
    elif output.find(b'tiempo') == -1:
        BioSecurityStatus = False
    print(f'BioSecurityStatus={BioSecurityStatus}')
    return output.find(b'tiempo')  # If return -1, then Host inaccessible

def WarningConectivity():
    while True:
        global intCountWarningConnectivy
        if logListBox.size() > 16:
            logListBox.delete(0, END)
        y = checkPing()
        if y == -1:
            print('Servidor de Apertura de Puertas Caido o Fuera de Línea')
            ct = datetime.datetime.now()
            logListBox.configure(background="LightBlue1", foreground="red", font=('Aerial 13'))
            logListBox.insert(0,
                              "Servidor de Apertura de Puertas y Garajes Caido o Fuera de Línea" + ' --- ' + str(ct).split('.')[
                                  0])
            time.sleep(3)
            messagebox.showerror("Error de Conectividad",
                                 "Error de Conexion con el Server BioTime \nReinicie el Computador \nSi el problema Continúa Comuníquese con Soporte Técnico")
            time.sleep(1)
            master.destroy()
            exit()

        elif y >= 0:
            print('Servidor de Aperturas de Puertas y Garajes Online')
            ct = datetime.datetime.now()
            if (intCountWarningConnectivy== 0 or intCountWarningConnectivy> 20):
                logListBox.configure(background="skyblue4", foreground="white", font=('Aerial 13'))
                logListBox.insert(0, "Servidor de Apertura está Conectado   en línea" + ' --- ' + str(ct).split('.')[0])
                intCountWarningConnectivy=0
        intCountWarningConnectivy = +1
        time.sleep(int(Dict_Ini_Params['WatchDog_Server_Secs']))


#  Rutina para Determinar si hay conexion con el Servidor de BioTime
if  (checkPing() == -1):
    messagebox.showerror("Error de Conectividad", "Error de Conexion con el Servidor \nReinicie el Computador \nSi el problema Continúa llame a Soporte Técnico")
    #time.sleep(1)
    #  Alternative para Modal Window
    #  master.after(5000, lambda: _show('Title', 'Prompting after 5 seconds'))
    master.destroy()
    exit()

WindowOpenDoor=WindowOPenendDoors()

threadCheckConectivity = MTThread(name='Conectivity', target=WarningConectivity)
threadCheckConectivity.daemon = True
threadCheckConectivity.start()

CheckAllFilesExist()
master.mainloop()
# Line Footer01
# Linde01 from Github
