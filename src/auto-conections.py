from helpers import *
from botcity.core import DesktopBot
import time

skills = [' JavaScript ',' React ',' TypeScript ',' SQL ',' NoSQL ',' Jest ',' RTL ',' Docker']

for skill in skills:
  class Bot(DesktopBot):
    def action(self, execution=None):
      clicar(self,'lupa')
      pyautogui.hotkey('ctrl', 'a')
      pyautogui.press('delete')
      time.sleep(2)
      digitar(skill)
      time.sleep(2)
      pyautogui.press('enter')
      time.sleep(2)
      for i in range(3):
        time.sleep(2)
        clicar(self,'conectar')
        clicar(self,'enviar')
        time.sleep(2) 
  Bot.main()
