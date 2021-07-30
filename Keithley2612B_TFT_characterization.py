#!/usr/bin/env python
# coding: utf-8

#  Keithley 2612B SMU TFT Characterization

#  Libraries

from keithley2600 import Keithley2600
import numpy as np
import os
import pyvisa


# Connecting the instrument

rm = pyvisa.ResourceManager()

address = rm.list_resources()

if len(address) == 0:
    print ('No device connected')
    
else:   
    print ('VISA address of the connected devices are:')
    
    for i in range(len(address)):
        print (f"i: {address[i]}")
    
    
    is_valid_input = False 
    
    while(not is_valid_input):
        
        connection_check = input ('Is the VISA address of the SMU listed? (Y/N)')
        
        if connection_check == 'Y' or  connection_check == 'y':
            is_valid_input = True
            smu_index = input('Enter the index number of the SMU:')
            k = Keithley2600(address[smu_index])
            print ('Connected successfully!')

        
        elif connection_check == 'N' or connection_check == 'n': 
            is_valid_input = True 
            print ('Please ensure that the SMU is connected properly')
    
        else: 
            print ('INVALID INPUT')
        
   
# Voltage sweep

# Source voltage from Channel A

start_volt = float (input ('Set the starting voltage (in Volts) for sweep:'))

is_valid_input = False

while (not is_valid_input):
    target_volt = float (input ('Set the target voltage (in Volts) for sweep:'))
    if (target_volt > start_volt):
        is_valid_input = True
    else: 
        print ('INVALID INPUT: Target voltage must be greater than starting voltage.')

is_valid_input = False 

while (not is_valid_input):
    step_volt = float (input ('Set the size of steps (in Volts) of sweep:')) 
    if (step_volt <= target_volt - start_volt):
        is_valid_input = True
    else:
        print ('INVALID INPUT: Step must be less than or equal to the difference between starting and target voltage')

if ((target_volt - start_volt) % step_volt == 0):
    sweep_volt = np.arange (start_volt, target_volt + step_volt, step_volt)
else:
     sweep_volt = np.arange (start_volt, target_volt, step_volt)

is_valid_input = False

while (not is_valid_input):
    integ_time = float (input('Set the integration time for each data point (in PLC)'))
    if (integ_time >= 0.001 and integ_time <= 25):
        is_valid_input = True 
    else: 
        print('INVALID INPUT: The integration time must be between 0.001 and 25 PLC.')


delay_time = float (input('Set settling delay (in seconds) before each measurement: (NOTE: Setting the value to -1 automatically starts taking measuremenet as soon as current in stable)'))

sweep_type = input ('Choose between pulsed and continuous sweep (enter P or C):')

is_valid_input = False

while (not is_valid_input):
    if (sweep_type == 'P' or sweep_type == 'p'):
        pulsed = True
        is_valid_input = True
    elif (sweep_type == 'C' or sweep_type == 'c'):
        pulsed = False
        is_valid_input = True
    else:
        print ('INVALID INPUT')

vi_output = k.voltage_sweep_single_smu (k.smua, sweep_volt, integ_time, delay_time, pulsed)











