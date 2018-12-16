#-------------- PINS ------------------
#======================================
# Пины цифровых кнопок
up_button_pin = 'Y4'
down_button_pin = 'Y8'
right_button_pin = 'X11'
start_button_pin = 'X12'
stop_button_pin = 'X10'

# lcd соединение
# см http://docs.micropython.org/en/v1.9.4/pyboard/library/lcd160cr.html#lcd160cr.LCD160CR
lcd_pins = 'XY'

# Пины шаговиков
extruder_pulse_pin = 'Y3' # экструдер
first_head_pulse_pin = 'Y12' # ШДГ1
second_head_pulse_pin = 'Y6' # ШДГ2
reciever_pulse_pin = 'X9' # Приемка

# Пины для подачи питания на шаговки
motors_enable_pin = 'Y5'
reciever_enable_pin = 'Y7'

uart_pin = 6 # номер uart
uart_ctrl_pin = 'X6' # RSE пин


# Пины датчиков ошибок
level_material_pin = "X3" # низкий уровень сырья
break_arm_pin = "X7" # обрыв рукава
emergency_stop_pin = "X8" # аварийный останов
high_temperature_pin = "X5" # перегрев расплава


# Пин сигнализации

assertion_pin = "Y11"

#--------------Settings-----------------
#=======================================
max_pressure = 1000 # Превышение давления вызывает ошибку "Первышено давление"

log_length = 15 # minutes
acceleration_delay = 500 # milliseconds

# ОВЕН
# Порядок температура1, температура2, давление1, давление2
temperature1_input = 4
temperature2_input = 4
pressuare1_input = 4
pressuare2_input = 4
owen_inputs = [temperature1_input, temperature2_input, pressuare1_input, pressuare2_input] # входы овена
owen_addres = 16 # адрес овена в сети modbus

# Ограничения оборотов шаговиков
max_extruder_round = 120.0 # максимальное количество оботов экструдера об/мин
max_first_head_round = 60.0 # максимальное количество оборотов ШДГ1 об/мин
max_second_head_round = 60.0 # максимальное количество оборотов ШДГ2 об/мин
max_reciver_round = 60.0 # максимальное количество оборотов приемки об/мин

# Через сколько секунд напоминать пользователю об ошибке
unset_client_notify_seconds = 10
