import time
import pyautogui
import pandas as pd
import logging
from openpyxl import Workbook, load_workbook
from gui import gui

#import os
#os.startfile('C:\SimplesNacional\SEDIF\SEDIF.exe')

logging.basicConfig(
        handlers=[logging.FileHandler(filename="./logs/logecords.txt",encoding='utf-8', mode='a+')],
        format="%(asctime)s - %(levelname)s - %(message)s", 
        datefmt="%F %A %T", 
        level=logging.INFO)

def notify(text):
    print(text)
    logging.info(text)


def addFeitaColumn(path):
    planilha = load_workbook(path)
    aba = planilha.active
    aba['E1'] = 'feita'
    planilha.save(path)

def putSomething(thing,empresa,path):
    table = pd.read_excel(path)
    try:
        table.loc[table['empresas']==empresa, 'feita'] = thing
    except:
        try:
            table.loc[table['empresas']==empresa, 'E'] = thing
        except Exception as e:
            notify(f'não coloquei o {thing} em {empresa} pois:',e)
            return None
    table.to_excel(path,index=False)
    notify(f'coloquei o{thing}em {empresa}')

putOk = lambda empresa,path : putSomething('ok',empresa,path)

def awaitItGoOut(self,imgName):
  while(1):
    print(f'esperando {imgName} sumir')
    time.sleep(1)
    if not self.find( imgName, matching=0.93, waiting_time=50):
      break


def tryToClick(self,btnName):
  if not self.find( btnName, matching=0.93, waiting_time=2000):
    try:
      self.find( f'{btnName}', matching=0.93, waiting_time=2000)
      self.click()
    except:
      pyautogui.scroll(-10)
  else:
    self.click()

def clicar(self,btnName,error=False):
  if error:
    self.tab()
  btn = btnName
  try:
    tryToClick(self,btn)
  except Exception as e :
    if gui.wrong(text=f'({btn})[{e}]')['tryAgain']:
      clicar(self,btnName,error=not error)

def digitar(text):
  pyautogui.write(text)

def defaultNotFound (imgName):
  raise Exception(f'{imgName} não foi encontrado')

doNothing = lambda x=1,y=2 : print(x,y,'any nothing')
   

def buscar(
      self,
      imgName,
      waiting_time=500,
      afterAction=lambda : pyautogui.press('enter'),
      notFoundAction=defaultNotFound
      ):
  try:
    if not self.find( imgName, matching=0.93, waiting_time=waiting_time):
      notFoundAction(imgName)
    else:
      afterAction()
    return True
  except Exception as e:
    if gui.wrong(text=e)['tryAgain']:
      return buscar(self,
                    imgName,
                    waiting_time=waiting_time,
                    afterAction=afterAction,
                    notFoundAction=notFoundAction)

def findAndClick(self,btn):
    buscar(self,btn,
         waiting_time=1000,
         afterAction= lambda : clicar(self,btn),
         notFoundAction=lambda imgName : print(imgName,'não achado mas segue o fluxo'))

def negarRepetida(self,empresa):
  def auxF():
    self.tab()
    pyautogui.press('enter')
    self.pular = True
    print(f'{empresa} estava repetida')
    putSomething('ja estava repetida',empresa,self.path)
  return auxF

def negarArquivoInexistente(self,empresa):
  def auxF():
    self.pular = True
    pyautogui.press('enter')
    print(f'{empresa} não teve .txt encontrado')
    putSomething('o arquivo .txt não foi encontrado',empresa,self.path)
  return auxF  
  
def negarArquivoComAvisos(self):
  empresa = self.empresa
  def auxF():
    self.pular = True
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    sair(self)
    print(f'{empresa} tinha avisos')
    putSomething('o arquivo continha avisos',empresa,self.path)
  return auxF  

def negarArquivoJaAssinado(self,empresa):
  def auxF():
    self.pular = True
    pyautogui.press('enter')
    print(f'{empresa} ja estava assinada')
    putSomething('ja estava assinada',empresa,self.path)
  return auxF  

def negarEmissaoComErro(self,empresa):
  def auxF():
    self.pular = True
    pyautogui.press('enter')
    print(f'{empresa} gerou um erro na transmissão')
    putSomething('gerou um erro na transmissão',empresa,self.path)
  return auxF  

sair = lambda self : clicar(self,'sair')

midleware = lambda self : self.pular

finish = lambda self : putOk(self.empresa,self.path)

def putAmiddlewarebetwwenAll(self,functions):
  for function in functions:
    if not midleware(self):
      function(self)