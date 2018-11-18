#������� �� ����������� ������ ��������
def Process(t):
 global process
 process = True
#��������� �������� ������� ������� ����������� ������, ��������� ������� ������� � ���������� ������ � True
timProcess.callback(Process)

#������� ����
def Stop():
 #����������� ���������� ���������
 global choice, flag_stop, flag_start, change
 #����������� �� ������ ������������
 for i in range(len(sm)):
  gzNew = sm[i].gzNew
  #������ ������� �������� �������� �� � ����
  sm[i].gzNew = 0
  #���������
  sm[i].Accel()
  #���������� ������ ������� ��������
  sm[i].gzNew = gzNew
 #������� ������ ��
 buttonOk.clearDrawButton()
 #������� ������ ������
 buttonCancel.clearDrawButton()
 #������ ������ ���������
 buttonChange.drawButton()
 #���� ����� ����� ����
 if flag_start == False:
  #������ 4�� ��
  choice = 3
  #������� ������ ��������
  buttonChange.clearDrawButton()
 #������ ���� ����
 flag_stop = False
 #������ ����� ������
 flag_start = True
 #������ ��������� ����
 change = False
 #������� ����� ��
 labelGz.clearDrawLabel()
 #������� ����� ��/���
 labelRPM.clearDrawLabel()
 #����������� ���������� ���������� �������� �������� �� � ������� ���������
 gz[0] = sm[choice].gzOld
 #������ ����� ��
 labelGz.drawLabel()
 #��������� ���������� ��/���
 roundPerMinut[0] = int(sm[choice].fRoundPerMin() * 10) / 10
 #������ � �������� ��������� �������� ��/���
 labelRPM.v = str(roundPerMinut[0])
 #���������� ������ ������
 lcd.set_font(1, scale=2, bold=0, trans=0, scroll=0)
 #������ ����� ��/��� � ������������� �� ��������
 labelRPM.qtZeroDrawLabel()

#������� �����
def Start():
 global choice, flag_stop, flag_start
 flag_stop = True
 flag_start = False
 #�������� ����� �������������
 choice = 4
 #�������������� ������ ������ ��
 buttonChoice.clearDrawButton()
 #����� ����� ������ ������ �� � ������� "I"
 buttonChoice.t = "I"
 buttonChoice.drawButton()
 labelGz.clearDrawLabel()
 labelRPM.clearDrawLabel()
 buttonChange.clearDrawButton()
 buttonOk.clearDrawButton()
 buttonCancel.clearDrawButton()

#������� �������� ��
def AddGz():
 global gz, roundPerMinut, factor, choice
 labelGz.clearDrawLabel()
 labelRPM.clearDrawLabel()
 #���� �������������� �������� ����� 9
 if (int(roundPerMinut[0] / factor % 10) == 9):
  #���������� ������ � 0
  roundPerMinut[0] = roundPerMinut[0] - factor * 9
 else:
  #����� ������ ���������� factor
  roundPerMinut[0] = roundPerMinut[0] + factor
 #������� �������� ����� �����, ��������� � ������������� ��������, ����� ������� � �������� � ��������� ������
 roundPerMinut[0] = int(roundPerMinut[0] * 10) / 10
 #������ ����� � �������� ��/���
 labelRPM.v = str(roundPerMinut[0])
 #������ ������� �������� � �������� ��
 gz[0] = sm[choice].getRoundPerMin(roundPerMinut[0])
 #������������ ����� ��
 labelGz.drawLabel()
 #������������ ����� ��/��� � ������������� �� ��������
 labelRPM.qtZeroDrawLabel()
#����������� ������� �������� �� ������� buttonPlus
buttonPlus.setFunc(AddGz)

#������� ������ ��
def DifGz():
 global gz, roundPerMinut, factor
 labelGz.clearDrawLabel()
 labelRPM.clearDrawLabel()
 #���� �������������� �������� ����� 0
 if (int(roundPerMinut[0] / factor % 10) == 0):
 #���������� ������ � 9
  roundPerMinut[0] = roundPerMinut[0] + factor * 9
 else:
 #����� ������ �������� factor
  roundPerMinut[0] = roundPerMinut[0] - factor
  #������� �������� ����� �����, ��������� � ������������� ��������, ����� ������� � �������� � ��������� ������
 roundPerMinut[0] = int(roundPerMinut[0] * 10 + 0.1) / 10 # +0.1 ��� ���������� �����������, ������ 0.9 - 0.1 = 0.7
 #������ ����� � �������� ��/���
 labelRPM.v = str(roundPerMinut[0])
 #������ ������� �������� � �������� ��
 gz[0] = sm[choice].getRoundPerMin(roundPerMinut[0])
 #������������ ����� ��
 labelGz.drawLabel()
 #������������ ����� ��/��� � ������������� �� ��������
 labelRPM.qtZeroDrawLabel()
#����������� ������� ������ �� ������� buttonMinus
buttonMinus.setFunc(DifGz)

#������� ��������� ��������������� ��������
def ChangeFactor():
 global factor
 #����� �� 10 ����
 factor = factor / 10
 #�� ������ ������ 0.1
 if factor < 0.1: factor = 10
#����������� ������� ��������� ��������������� �������� ������� buttonShift
buttonShift.setFunc(ChangeFactor)

#������� ���������� �� ��������� ��������
def Change():
 global change
 change = True
 buttonChange.clearDrawButton()
 buttonOk.drawButton()
 buttonCancel.drawButton()
#����������� ������� ���������� �� ��������� �������� ������� buttonChange
buttonChange.setFunc(Change)

#������� ������� ������ ���������
def Ok():
 global change, flag_stop
 change = False
 flag_stop = True
 labelGz.clearDrawLabel()
 labelRPM.clearDrawLabel()
 sm[choice].setRoundPerMin(roundPerMinut[0])
 gz[0] = sm[choice].gzOld
 labelGz.drawLabel()
 roundPerMinut[0] = int(sm[choice].fRoundPerMin() * 10) / 10
 labelRPM.v = str(roundPerMinut[0])
 labelRPM.qtZeroDrawLabel()
 buttonOk.clearDrawButton()
 buttonCancel.clearDrawButton()
 buttonChange.drawButton()
#����������� ������� ������� ������ ��������� ������� buttonOk
buttonOk.setFunc(Ok)

#������� �������� �������
def Cancel():
 global change
 change = False
 labelGz.clearDrawLabel()
 labelRPM.clearDrawLabel()
 gz[0] = sm[choice].gzOld
 labelGz.drawLabel()
 roundPerMinut[0] = int(sm[choice].fRoundPerMin() * 10) / 10
 labelRPM.v = str(roundPerMinut[0])
 labelRPM.qtZeroDrawLabel()
 buttonOk.clearDrawButton()
 buttonCancel.clearDrawButton()
 buttonChange.drawButton()
#����������� ������� �������� ������� ������� buttonCancel
buttonCancel.setFunc(Cancel)

#������� ������ �� ���� ������ �������������
def Choice():
 global choice, flag_start
 choice = choice + 1
 flag_start = True
 if choice >= 4: 
  choice = 0
 #����� �� �� ������, � ��� �������������� �����. ����� ����� �������� ��� ������� ������ SM �� ����� � �������� �, ������: buttonChoice.t = str(sm.n)
 if choice == 0: buttonChoice.t = "E"
 elif choice == 1: buttonChoice.t = "1"
 elif choice == 2: buttonChoice.t = "2"
 elif choice == 3: buttonChoice.t = "R"
 buttonChoice.drawButton()
 labelGz.clearDrawLabel()
 labelRPM.clearDrawLabel()
 gz[0] = sm[choice].gzOld
 labelGz.drawLabel()
 roundPerMinut[0] = int(sm[choice].fRoundPerMin() * 10) / 10
 labelRPM.v = str(roundPerMinut[0])
 labelRPM.qtZeroDrawLabel()
 buttonOk.clearDrawButton()
 buttonCancel.clearDrawButton()
 buttonChange.drawButton()
#����������� ������ �� ���� ������ ������������� ������� buttonChoice
buttonChoice.setFunc(Choice)

#���� ��������� ��� ��������� ��
def InitDrawBlock():
 lcd.erase()
 buttonPlus.drawButton()
 buttonMinus.drawButton()
 buttonShift.drawButton()
 labelGz.drawLabel()
 labelRPM.drawLabel()
 buttonChange.drawButton()
 buttonChoice.drawButton()

#���� �� ��������� ������: �����, ������, �����, �� ��������� �������� �������
def touchDrawBlock():
 global encounterTouch
 if encounterTouch == 1:
  buttonPlus.drawButton()
  buttonMinus.drawButton()
  buttonShift.drawButton()

#���� �� ��������� ���������� ������� ��� ��������� ��������
def flashDrawBlock():
 global factor, change, encounter
 #���������� ������
 if change and encounter == 5:
  number = 3 - len( str( int( factor * 10 ) ) )
  if number == 2: number = 3
  labelRPM.drawFlash(number)
 #���������� � ���������� ����
 if change and encounter == 1:
  labelRPM.drawLabel()

#���� ���������, ���������� ��� � ������� ������� �� �������� �������
def DrawBlock():
 touchDrawBlock()
 flashDrawBlock()

#���� ����������� �������: ���� ��������� ������� � ���
def TouchBlock():
 global encounterTouch, Touch, X, Y
 touch, X, Y = lcd.get_touch()
 #��������� ������� ���� ������� ��������� � ������ ����� ������� ��� ������
 if touch and encounterTouch == 0:
  #������ �������
  encounterTouch = 10
  #���������� ������
  Touch = True
  #������� �������
  lcd.set_pixel(1, 1, lcd.rgb(0, 0, 255)) #Extra
 #���� ������� ����� ������
 if encounterTouch != 0:
  encounterTouch = encounterTouch - 1
 #���� ������� ������ � ����� �������
 if encounterTouch == 1:
  Touch = False
  #������� �������
  lcd.set_pixel(1, 1, lcd.rgb(255, 0, 0)) #Extra

#���� �������� ������ � ������� � ������������ ������
def HandlerBlock():
 global Touch, X, Y
 #������ ����
 if buttonOff.value() == 0:
  Stop()
 #������ �����
 elif buttonOn.value() == 0:
  Start()
 #������� �� ��� �������
 if Touch:
  #���� ������� ��������� � ��������� ����� �� ��������� ��������� ������� ����������� � ������ ������
  if X > buttonPlus.x and X < buttonPlus.x + buttonPlus.w and Y > buttonPlus.y and Y < buttonPlus.y + buttonPlus.h and change:
   buttonPlus.touchDrawButton()
   buttonPlus.f()
  elif X > buttonMinus.x and X < buttonMinus.x + buttonMinus.w and Y > buttonMinus.y and Y < buttonMinus.y + buttonMinus.h and change:
   buttonMinus.touchDrawButton()
   buttonMinus.f()
  elif X > buttonShift.x and X < buttonShift.x + buttonShift.w and Y > buttonShift.y and Y < buttonShift.y + buttonShift.h and change:
   buttonShift.touchDrawButton()
   buttonShift.f()
  elif X > buttonChange.x and X < buttonChange.x + buttonChange.w and Y > buttonChange.y and Y < buttonChange.y + buttonChange.h and change == False and flag_start:
   buttonChange.touchDrawButton()
   buttonChange.f()
  elif X > buttonOk.x and X < buttonOk.x + buttonOk.w and Y > buttonOk.y and Y < buttonOk.y + buttonOk.h and change:
   buttonOk.touchDrawButton()
   buttonOk.f()
  elif X > buttonCancel.x and X < buttonCancel.x + buttonCancel.w and Y > buttonCancel.y and Y < buttonCancel.y + buttonCancel.h and change:
   buttonCancel.touchDrawButton()
   buttonCancel.f()
  elif X > buttonChoice.x and X < buttonChoice.x + buttonChoice.w and Y > buttonChoice.y and Y < buttonChoice.y + buttonChoice.h and change == False:
   buttonChoice.touchDrawButton()
   buttonChoice.f()
  Touch = False

#���� ��������� ��
def AccelBlock():
 global change, choice, flag_start, flag_stop
 #���� ������ ����� ������, �� �������� �������� ���������� ��
 if flag_start:
 #��������� �� ��������� �� ��������, ��� ������� � �������, � �� �������� ��� � 0.2 ��� ��������� ������������ ��������� �������� �� � ���� ���� ������
  if sm[choice].gzOld != sm[choice].gzNew and ((encounter + 1) % 2) == 0 and flag_stop: 
   sm[choice].Accel()
   if change == False:
    labelGz.clearDrawLabel()
    labelRPM.clearDrawLabel()
    gz[0] = sm[choice].gzOld
    labelGz.drawLabel()
    roundPerMinut[0] = int(sm[choice].fRoundPerMin() * 10) / 10
    labelRPM.v = str(roundPerMinut[0])
    labelRPM.qtZeroDrawLabel()
 #���� ������ ����� ������������� � ���� ���� ������
 elif choice == 4 and flag_stop:
  #����������� �� ������ �� ��������� ���� �� ����������� ��������, ���� ������������ �� ������������ ������ ����� � �� �� ������ �� ������, ��������� �� ������ ��[0]
  for i in range(len(sm)):
   sm[i].Accel()
   print(sm[i].gzOld)

#�������� ���� ���������, � ������� �������� ��� ����������� ����� ��������� ����
try: #Main Block
 InitDrawBlock()
 while True:
  #���� ������ ��������� � ������, ���������� ������� ��������
  if process:
   #����� ������� �������� ��������
   encounter = encounter + 1
   DrawBlock()
   TouchBlock()
   HandlerBlock()
   AccelBlock()
   #�������� ������� �������
   if encounter == 10: encounter = 0
   #���������� ������ � ����
   process = False

#����� ���������� (���������� ������)
finally:
 print("error")
