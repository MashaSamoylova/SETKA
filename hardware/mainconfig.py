#-------------- PINS ------------------
#======================================

up_button_pin = 'Y10'
down_button_pin = 'Y11'
right_button_pin = 'Y12'
start_button_pin = 'Y6'
stop_button_pin = 'Y6'
lcd_pins = 'X'

extruder_pulse_pin = 'Y6'
first_head_pulse_pin = 'Y6'
second_head_pulse_pin = 'Y6'
reciever_pulse_pin = 'Y6'

motors_enable_pin = 'Y6'
reciever_enable_pin = 'Y6'

uart_pin = 6
uart_ctrl_pin = 'Y4'
level_material_pin = "Y6"

high_temperature_pin = "Y6"
break_arm_pin = "Y6"
emergency_stop_pin = "Y6"

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

