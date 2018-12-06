from uModBus.serial import Serial
register_address=0x01
slave_addr=0x01
register_value=42
modbus = Serial(6, ctrl_pin='Y5')
return_flag = modbus.write_single_register(slave_addr, register_address, register_value, False)
output_flag = 'Success' if return_flag else 'Failure'
print('Writing single register status: ' + output_flag)

starting_address=0x00
register_quantity=100
signed=False

register_value = modbus.read_holding_registers(slave_addr, starting_address, register_quantity, signed)
print('Holding register value: ' + ' '.join('{:d}'.format(x) for x in register_value))
