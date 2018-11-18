#Функция по выстовления флажка процесса
def Process(t):
 global process
 process = True
#Присвоить ведущему таймеру функцию выставления флажка, прерывает главный процесс и выставляет флажок в True
timProcess.callback(Process)

#Функция стоп
def Stop():
 #перечислены глобальные переменые
 global choice, flag_stop, flag_start, change
 #пребегаемся по списку сервомоторов
 for i in range(len(sm)):
  gzNew = sm[i].gzNew
  #ставим будущую скорость вращения СМ в ноль
  sm[i].gzNew = 0
  #разгоняем
  sm[i].Accel()
  #возвращаем старую будущую скорость
  sm[i].gzNew = gzNew
 #стираем кнопку ок
 buttonOk.clearDrawButton()
 #стираем кнопку отмены
 buttonCancel.clearDrawButton()
 #рисуем кнопку изменения
 buttonChange.drawButton()
 #если ффлаг старт ложь
 if flag_start == False:
  #выбран 4ый СМ
  choice = 3
  #стираем кнопку изменить
  buttonChange.clearDrawButton()
 #флажок стоп ложь
 flag_stop = False
 #флажок старт истина
 flag_start = True
 #флажок изменения ложь
 change = False
 #стираем текст Гц
 labelGz.clearDrawLabel()
 #стираем текст Об/мин
 labelRPM.clearDrawLabel()
 #присваиваем глобальной переменной значение текущего СМ с текущей скоростью
 gz[0] = sm[choice].gzOld
 #рисуем текст Гц
 labelGz.drawLabel()
 #вычисляем количество Об/мин
 roundPerMinut[0] = int(sm[choice].fRoundPerMin() * 10) / 10
 #вносим в этикетку строковое значение Об/мин
 labelRPM.v = str(roundPerMinut[0])
 #выставляем размер шрифта
 lcd.set_font(1, scale=2, bold=0, trans=0, scroll=0)
 #рисуем текст Ою/мин с ограничениями по символам
 labelRPM.qtZeroDrawLabel()

#Функция старт
def Start():
 global choice, flag_stop, flag_start
 flag_stop = True
 flag_start = False
 #выбираем режим инициализации
 choice = 4
 #перерисовываем кнопку выбора СМ
 buttonChoice.clearDrawButton()
 #пишем новую кнопку выбора СМ с текстом "I"
 buttonChoice.t = "I"
 buttonChoice.drawButton()
 labelGz.clearDrawLabel()
 labelRPM.clearDrawLabel()
 buttonChange.clearDrawButton()
 buttonOk.clearDrawButton()
 buttonCancel.clearDrawButton()

#Функция добавить Гц
def AddGz():
 global gz, roundPerMinut, factor, choice
 labelGz.clearDrawLabel()
 labelRPM.clearDrawLabel()
 #если целолчисленное значение равно 9
 if (int(roundPerMinut[0] / factor % 10) == 9):
  #сбрасываем символ в 0
  roundPerMinut[0] = roundPerMinut[0] - factor * 9
 else:
  #иначе просто прибавляем factor
  roundPerMinut[0] = roundPerMinut[0] + factor
 #выводим ненужные части дроби, переводим в целочисленное значение, потом обратно в значение с плавующей точкой
 roundPerMinut[0] = int(roundPerMinut[0] * 10) / 10
 #вносим текст в этикетку Об/мин
 labelRPM.v = str(roundPerMinut[0])
 #вносим текущее вращение в этикетку Гц
 gz[0] = sm[choice].getRoundPerMin(roundPerMinut[0])
 #вырисовываем текст Гц
 labelGz.drawLabel()
 #вырисовываем текст Об/мин с ограничениями по символам
 labelRPM.qtZeroDrawLabel()
#Присваиваем функцию добавить Гц объекту buttonPlus
buttonPlus.setFunc(AddGz)

#Функция отнять Гц
def DifGz():
 global gz, roundPerMinut, factor
 labelGz.clearDrawLabel()
 labelRPM.clearDrawLabel()
 #если целолчисленное значение равно 0
 if (int(roundPerMinut[0] / factor % 10) == 0):
 #сбрасываем символ в 9
  roundPerMinut[0] = roundPerMinut[0] + factor * 9
 else:
 #иначе просто отнимаем factor
  roundPerMinut[0] = roundPerMinut[0] - factor
  #выводим ненужные части дроби, переводим в целочисленное значение, потом обратно в значение с плавующей точкой
 roundPerMinut[0] = int(roundPerMinut[0] * 10 + 0.1) / 10 # +0.1 для избавления погрешнисти, пример 0.9 - 0.1 = 0.7
 #вносим текст в этикетку Об/мин
 labelRPM.v = str(roundPerMinut[0])
 #вносим текущее вращение в этикетку Гц
 gz[0] = sm[choice].getRoundPerMin(roundPerMinut[0])
 #вырисовываем текст Гц
 labelGz.drawLabel()
 #вырисовываем текст Об/мин с ограничениями по символам
 labelRPM.qtZeroDrawLabel()
#Присваиваем функцию отнять Гц объекту buttonMinus
buttonMinus.setFunc(DifGz)

#Функция изменение воздействуещего значения
def ChangeFactor():
 global factor
 #делим на 10 пока
 factor = factor / 10
 #не станет меньше 0.1
 if factor < 0.1: factor = 10
#Присваиваем функцию изменение воздействуещего значения объекту buttonShift
buttonShift.setFunc(ChangeFactor)

#Функция разрешение на изменения значения
def Change():
 global change
 change = True
 buttonChange.clearDrawButton()
 buttonOk.drawButton()
 buttonCancel.drawButton()
#Присваиваем функцию разрешение на изменения значения объекту buttonChange
buttonChange.setFunc(Change)

#Функция принять данные изменения
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
#Присваиваем функцию принять данные изменения объекту buttonOk
buttonOk.setFunc(Ok)

#Функция отменить оперцию
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
#Присваиваем функцию отменить оперцию объекту buttonCancel
buttonCancel.setFunc(Cancel)

#Функция выбора СМ либо режима инициализации
def Choice():
 global choice, flag_start
 choice = choice + 1
 flag_start = True
 if choice >= 4: 
  choice = 0
 #номер СМ из списка, и ему соотвествующая буква. Также можно изменить имя объекта класса SM на букву и выводить её, пример: buttonChoice.t = str(sm.n)
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
#Присваиваем выбора СМ либо режима инициализации объекту buttonChoice
buttonChoice.setFunc(Choice)

#Блок отрисовки при включении МК
def InitDrawBlock():
 lcd.erase()
 buttonPlus.drawButton()
 buttonMinus.drawButton()
 buttonShift.drawButton()
 labelGz.drawLabel()
 labelRPM.drawLabel()
 buttonChange.drawButton()
 buttonChoice.drawButton()

#Блок по отрисовки кнопок: плюса, минуса, шифта, по истечению счетчика касания
def touchDrawBlock():
 global encounterTouch
 if encounterTouch == 1:
  buttonPlus.drawButton()
  buttonMinus.drawButton()
  buttonShift.drawButton()

#Блок по отрисовки выбранного символа при изменении значения
def flashDrawBlock():
 global factor, change, encounter
 #Обозначить символ
 if change and encounter == 5:
  number = 3 - len( str( int( factor * 10 ) ) )
  if number == 2: number = 3
  labelRPM.drawFlash(number)
 #Отрисовать в нормальном виде
 if change and encounter == 1:
  labelRPM.drawLabel()

#Блок отрисовки, количество раз в секунду зависит от ведущего таймера
def DrawBlock():
 touchDrawBlock()
 flashDrawBlock()

#Блок обозначения касания: было совершено касание и где
def TouchBlock():
 global encounterTouch, Touch, X, Y
 touch, X, Y = lcd.get_touch()
 #запускаем счетчик если касание произошло в момент когда счетчик был обнулён
 if touch and encounterTouch == 0:
  #задаем счетчик
  encounterTouch = 10
  #выставляем флажок
  Touch = True
  #пиксель касания
  lcd.set_pixel(1, 1, lcd.rgb(0, 0, 255)) #Extra
 #если счетчик ведет отсчёт
 if encounterTouch != 0:
  encounterTouch = encounterTouch - 1
 #если счетчик близок к концу отсчёта
 if encounterTouch == 1:
  Touch = False
  #пиксель касания
  lcd.set_pixel(1, 1, lcd.rgb(255, 0, 0)) #Extra

#Блок привязки кнопок к дисплею и срабатывания кнопок
def HandlerBlock():
 global Touch, X, Y
 #кнопка стоп
 if buttonOff.value() == 0:
  Stop()
 #кнопка старт
 elif buttonOn.value() == 0:
  Start()
 #касание по лсд дисплею
 if Touch:
  #если касание произошло в указанном месте то выполняем следующую функцию привязанную к данной кнопке
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

#Блок ускорения СМ
def AccelBlock():
 global change, choice, flag_start, flag_stop
 #Если флажок старт истина, то изменяем скорость выбранного СМ
 if flag_start:
 #выбранный СМ проверяем по скорости, его текущей и будущей, и по счетчику раз в 0.2 сек запускаем срабатывание изменения скорости СМ и флаг стоп истина
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
 #Если выбран режим инициализации и флаг стоп истина
 elif choice == 4 and flag_stop:
  #Пробегаемся по списку СМ выставляя всем их назначенные скорости, пока пользователя не удовлетворит данный режим и он не сменит на другой, следующий по выбору СМ[0]
  for i in range(len(sm)):
   sm[i].Accel()
   print(sm[i].gzOld)

#Основной блок программы, в котором высываем все последующие блоки описанные выше
try: #Main Block
 InitDrawBlock()
 while True:
  #если флажок выставлен в истину, изменяемый ведущим таймером
  if process:
   #ведем счетчик главного процесса
   encounter = encounter + 1
   DrawBlock()
   TouchBlock()
   HandlerBlock()
   AccelBlock()
   #обнуляем главный счетчик
   if encounter == 10: encounter = 0
   #выставляем флажок в ложь
   process = False

#Ловим исключение (записываем ошибку)
finally:
 print("error")
