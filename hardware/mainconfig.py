#-------------- PINS ------------------
#======================================

up_button_pin = 'Y10'
down_button_pin = 'Y6'
right_button_pin = 'Y9'
start_button_pin = 'Y12'
stop_button_pin = 'Y11'
lcd_pins = 'X'

extruder_pulse_pin = 'Y6'
first_head_pulse_pin = 'Y6'
second_head_pulse_pin = 'Y6'
reciever_pulse_pin = 'Y6'

motors_enable_pin = 'Y6'
reciever_enable_pin = 'Y6'

uart_pin = 6
uart_ctrl_pin = 'Y4'

# Пины датчиков ошибок
level_material_pin = "Y6" # низкий уровень сырья
break_arm_pin = "Y6" # обрыв рукава
emergency_stop_pin = "Y6" # аварийный останов
high_temperature_pin = "Y6" # перегрев расплава


# Пин сигнализации

assertion_pin = "Y8"

#=======================================

#--------------Settings-----------------
#=======================================
max_pressure = 1000

log_length = 15 # minutes
acceleration_delay = 500 # milliseconds

mesh_uart_number = 2
max_mesh_thickness = 100

owen_inputs = [4,4,4,4]
owen_addres = 16

# Ограничения оборотов шаговиков
max_extruder_round = 120.0 # максимальное количество оботов экструдера об/мин
max_first_head_round = 60.0 # максимальное количество оборотов ШДГ1 об/мин
max_second_head_round = 60.0 # максимальное количество оборотов ШДГ2 об/мин
max_reciver_round = 60.0 # максимальное количество оборотов приемки об/мин

# Через сколько секунд напоминать пользователю об ошибке
unset_client_notify_seconds = 10
