import PySimpleGUI as sg
from hashlib import md5
import os
import sys
import threading

global sair
sair = False

class Layouts:
    def __init__(self):  
        self.password = [
            [
                sg.Text('senha:'),
                sg.InputText(background_color='#ffffff'),
            ],
            [sg.Button('verificar'), sg.Button('Cancelar')]]

        self.simple = lambda color,text: [sg.Text(text, background_color=color)]

        self.wrong = lambda text:[
            (self.simple(color = 'red', text = text)),
            ([sg.Button('seguir processo')]),
            ([sg.Button('parar processo')]),
            ([sg.Button('tentar etapa novamente')])
        ]
        self.ok = lambda text:[(self.simple(color = 'green', text = text)),([sg.Button('ok')])]

        self.getPath = [
            [
                sg.Text('insira o endereço do arquivo'),
                sg.InputText(background_color='#ffffff'),
                sg.FileBrowse(
                    initial_folder=os.getcwd(),
                    file_types=[("xmls Files", "*.xlsx")]
                    )
            ],
            [sg.Button('começar'), sg.Button('Cancelar')] ]


class Waiters:
    def __init__(self):
        self.passwordStr = ''
        self.filePath = ''
    
    def password(self,title,correctHash):
        window = sg.Window(title).Layout(layouts.password)
        while True:
            event, values = window.read()
            self.passwordStr = input = values[0].replace('"', '')
            userPasswordmd5 = md5(self.passwordStr.encode()).hexdigest()
            
            if event == sg.WIN_CLOSED or event == 'Cancelar':
                window.close()
                sys.exit()
            if event == 'verificar' and userPasswordmd5 == correctHash:  # if user closes window or clicks cancel
                window.close()
                break
        

    def ok(self,title,text='a senha está correta'):
        window = sg.Window(title).Layout(layouts.ok(text =text))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'ok':
                break
        window.close()

    def wrong(self,text,title='erro'):
        window = sg.Window(title).Layout(layouts.wrong(text=text))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'parar processo':
                window.close()
                sys.exit()
            if event == 'seguir processo':
                window.close()
                return {"tryAgain" : False}
            if event == 'tentar etapa novamente':
                
                window.close()
                return {"tryAgain" : True}


    def getPath(self,title='digite o caminho'):
        window = sg.Window(title).Layout(layouts.getPath)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancelar':
                window.close()
                sys.exit()
            if event ==('começar'):
                path=input=values[0].replace('"','')
                break

        window.close()
        return path

layouts = Layouts()
gui = Waiters()