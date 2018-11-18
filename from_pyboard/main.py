def Process(t):
 global process
 process = True

timProcess.callback(Process)

def AddGz():
 global gz, roundPerMinut, factor
 labelGz.clearDrawLabel()
 labelRPM.clearDrawLabel()
 if (int(roundPerMinut[0] / factor % 10) == 9):
  roundPerMinut[0] = roundPerMinut[0] - factor * 9
 else:
  roundPerMinut[0] = roundPerMinut[0] + factor
 roundPerMinut[0] = int(roundPerMinut[0] * 10) / 10
 labelRPM.v = str(roundPerMinut[0])
 gz[0] = sme.getRoundPerMin(roundPerMinut[0])
 labelGz.drawLabel()
 labelRPM.qtZeroDrawLabel()

buttonPlus.setFunc(AddGz)

def DifGz():
 global gz, roundPerMinut, factor
 labelGz.clearDrawLabel()
 labelRPM.clearDrawLabel()
 if (int(roundPerMinut[0] / factor % 10) == 0):
  roundPerMinut[0] = roundPerMinut[0] + factor * 9
 else:
  roundPerMinut[0] = roundPerMinut[0] - factor
 roundPerMinut[0] = int(roundPerMinut[0] * 10 + 0.1) / 10 # +0.1 для избавления погрешнисти, пример 0.9 - 0.1 = 0.7
 labelRPM.v = str(roundPerMinut[0])
 gz[0] = sme.getRoundPerMin(roundPerMinut[0])
 labelGz.drawLabel()
 labelRPM.qtZeroDrawLabel()

buttonMinus.setFunc(DifGz)

def ChangeFactor():
 global factor
 factor = factor / 10
 if factor < 0.1: factor = 10
 factor = int(factor * 10) / 10

buttonShift.setFunc(ChangeFactor)

def Change():
 global change
 change = True
 buttonChange.clearDrawButton()
 buttonOk.drawButton()
 buttonCancel.drawButton()

buttonChange.setFunc(Change)

def Ok():
 global change
 change = False
 labelGz.clearDrawLabel()
 labelRPM.clearDrawLabel()
 sme.setRoundPerMin(roundPerMinut[0])
 gz[0] = sme.gzOld
 labelGz.drawLabel()
 roundPerMinut[0] = int(sme.fRoundPerMin() * 10) / 10
 labelRPM.v = str(roundPerMinut[0])
 labelRPM.qtZeroDrawLabel()
 buttonOk.clearDrawButton()
 buttonCancel.clearDrawButton()
 buttonChange.drawButton()

buttonOk.setFunc(Ok)

def Cancel():
 global change
 change = False
 labelGz.clearDrawLabel()
 labelRPM.clearDrawLabel()
 gz[0] = sme.gzOld
 labelGz.drawLabel()
 roundPerMinut[0] = int(sme.fRoundPerMin() * 10) / 10
 labelRPM.v = str(roundPerMinut[0])
 labelRPM.qtZeroDrawLabel()
 buttonOk.clearDrawButton()
 buttonCancel.clearDrawButton()
 buttonChange.drawButton()

buttonCancel.setFunc(Cancel)

def InitDrawBlock():
 lcd.erase()
 buttonPlus.drawButton()
 buttonMinus.drawButton()
 buttonShift.drawButton()
 labelGz.drawLabel()
 labelRPM.drawLabel()
 buttonChange.drawButton()

def touchDrawBlock():
 global encounterTouch
 if encounterTouch == 1:
  buttonPlus.drawButton()
  buttonMinus.drawButton()
  buttonShift.drawButton()

def flashDrawBlock():
 global factor, change, encounter
 if change and encounter == 5:
  number = 3 - len( str( int( factor * 10 ) ) )
  if number == 2: number = 3
  labelRPM.drawFlash(number)
 if change and encounter == 1:
  labelRPM.drawLabel()

def DrawBlock():
 touchDrawBlock()
 flashDrawBlock()

def TouchBlock():
 global encounterTouch, Touch, X, Y
 touch, X, Y = lcd.get_touch()

 if touch and encounterTouch == 0:
  encounterTouch = 10
  Touch = True
  lcd.set_pixel(1, 1, lcd.rgb(0, 0, 255)) #Extra
 if encounterTouch != 0:
  encounterTouch = encounterTouch - 1
 if encounterTouch == 1:
  Touch = False
  lcd.set_pixel(1, 1, lcd.rgb(255, 0, 0)) #Extra

def HandlerBlock():
 global Touch, X, Y
 if Touch:
  if X > buttonPlus.x and X < buttonPlus.x + buttonPlus.w and Y > buttonPlus.y and Y < buttonPlus.y + buttonPlus.h and change:
   buttonPlus.touchDrawButton()
   buttonPlus.f()
  elif X > buttonMinus.x and X < buttonMinus.x + buttonMinus.w and Y > buttonMinus.y and Y < buttonMinus.y + buttonMinus.h and change:
   buttonMinus.touchDrawButton()
   buttonMinus.f()
  elif X > buttonShift.x and X < buttonShift.x + buttonShift.w and Y > buttonShift.y and Y < buttonShift.y + buttonShift.h and change:
   buttonShift.touchDrawButton()
   buttonShift.f()
  elif X > buttonChange.x and X < buttonChange.x + buttonChange.w and Y > buttonChange.y and Y < buttonChange.y + buttonChange.h and change == False:
   buttonChange.touchDrawButton()
   buttonChange.f()
  elif X > buttonOk.x and X < buttonOk.x + buttonOk.w and Y > buttonOk.y and Y < buttonOk.y + buttonOk.h and change:
   buttonOk.touchDrawButton()
   buttonOk.f()
  elif X > buttonCancel.x and X < buttonCancel.x + buttonCancel.w and Y > buttonCancel.y and Y < buttonCancel.y + buttonCancel.h and change:
   buttonCancel.touchDrawButton()
   buttonCancel.f()
  Touch = False

def AccelBlock():
 if sme.gzOld != sme.gzNew and ((encounter + 1) % 2) == 0: 
  sme.Accel()
  if change == False:
   labelGz.clearDrawLabel()
   labelRPM.clearDrawLabel()
   gz[0] = sme.gzOld
   labelGz.drawLabel()
   roundPerMinut[0] = int(sme.fRoundPerMin() * 10) / 10
   labelRPM.v = str(roundPerMinut[0])
   labelRPM.qtZeroDrawLabel()

try: #Main Block
 InitDrawBlock()
 while True:
  if process:
   encounter = encounter + 1
   DrawBlock()
   TouchBlock()
   HandlerBlock()
   AccelBlock()
   if encounter == 10: encounter = 0
   process = False

finally:
 print("error")