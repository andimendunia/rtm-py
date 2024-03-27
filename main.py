import pymodbus.client as ModbusClient
from pymodbus import (
   ExceptionResponse,
   Framer,
   ModbusException,
   pymodbus_apply_logging_config
)
import requests
import time

# Modbus client configuration
MODBUS_IP_ADDRESS = "172.70.52.201"  # Replace with the Modbus device IP address
MODBUS_PORT = 502  # Standard Modbus TCP port

# API endpoint configuration
API_ENDPOINT = "http://172.70.52.150"  # Replace with your API endpoint URL

# Polling interval (in seconds)
POLLING_INTERVAL = 5  # Replace with your desired polling interval

# Connect to the Modbus device


def run_sync():

   # Activate debugging
   # pymodbus_apply_logging_config("DEBUG")
    
   client = ModbusClient.ModbusTcpClient(
      MODBUS_IP_ADDRESS,
      port = MODBUS_PORT,
   )
    
   print("Connecting to server...")
   client.connect()

   print("Getting and verifying data...")

   try:
      rr = client.read_input_registers(10,1,slave=1)
   except ModbusException as exc:
      print(f"Received ModbusException({exc}) from library")
      client.close()
      return
   
   if rr.isError():
      print(f"Received Modbus library error({rr})")
      client.close()
      return
   
   if isinstance(rr, ExceptionResponse):
      print(f"Received Modbus library exception ({rr})")
      # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
      client.close()

   print(client.read_input_registers(10,1,slave=1).registers)
   print(client.read_input_registers(20,1,slave=1).registers)

   print("close connection")
   client.close()

while True:
   run_sync()    
   quit()