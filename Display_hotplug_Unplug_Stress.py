import socket
import os
from time import sleep
import sys
import time
import datetime
import os.path
import subprocess
import string
import configparser
import ta_rtl_lib as rtl_lib
import ta_report_lib as report_lib

logger = rtl_lib.get_logger(__name__)
strTestName = 'BSOD and TDR check'

def CheckBSODStatus():
    dirPath = "C:\\Windows"
    strStepName = 'Check BSOD status'
    strDescription = 'BSOD should not occured'
    strExpected = 'BSOD should not found'
    strStatus = 'FAIL'
    for file in os.listdir(dirPath):
        if file.endswith(".dmp"):
            print("BSOD Found")
            strActual = 'BSOD Occur'
            strStatus = 'FAIL'
            report_lib.add_result(strStatus, strDescription, strStepName, strTestName, strExpected, strActual)
            return 0
        elif file.endswith(".BAK"):
            print("BSOD Found")
            strStatus = 'FAIL'
            strActual = 'BSOD Occur'
            report_lib.add_result(strStatus, strDescription, strStepName, strTestName, strExpected, strActual)
            return 0

    else:
        print("BSOD not found")
        strStatus = 'PASS'
        strActual ='BSOD not Occur'
        report_lib.add_result(strStatus, strDescription, strStepName, strTestName, strExpected, strActual)

    print("Exit to Check BSOD Status Function")


def CheckTDRStatus():
    # status = 0;
    print("Entry to Check TDR Status Function")
    dirPath = 'C:/Windows/LiveKernelReports/WATCHDOG'
    strStepName = 'Check TDR status'
    strDescription = 'TDR should not occured'
    strExpected = 'TDR should not found'
    for file in os.listdir(dirPath):
        if file.endswith(".dmp"):
            print("TDR found ")
            strStatus = 'FAIL'
            strActual = 'TDR found '
            report_lib.add_result(strStatus, strDescription, strStepName, strTestName, strExpected, strActual)
            return 0
        elif file.endswith(".BAK"):
            print("TDR Found")
            strStatus = 'FAIL'
            strActual = 'TDR Found'
            report_lib.add_result(strStatus, strDescription, strStepName, strTestName, strExpected, strActual)
            return 0
    else:
        print("Did not find TDR")
        strStatus = 'PASS'
        strActual ='TDR not found'
        report_lib.add_result(strStatus, strDescription, strStepName, strTestName, strExpected, strActual)
    print("Exit to Check TDR Status Function")
    # return status

config= configparser.RawConfigParser()
configfile_path=r'C:\testres\Hotplug Unplug Stress\config.cfg'
config.read(configfile_path)
get_ip=dict(config.items('ip_address_of_rpi'))
print(get_ip['ip'])
host_name=get_ip['ip']
host_port=9095


# Create a client socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

clientSocket.connect((host_name,host_port));

print("------Starting Display Hot-Plug Unplug case for 10 cycle------")
sleep(2)

send_data="Hot_Plug";
clientSocket.send(send_data.encode());
sleep(50)
while(True):
    sleep_dataFromServer = clientSocket.recv(1024);
    if sleep_dataFromServer:
        print(sleep_dataFromServer.decode())
        if (sleep_dataFromServer.decode() == "Blankout detected"):
            Blank_status=1
        if (sleep_dataFromServer.decode() == "No Blankout"):
            Blank_status=0
        BSOD_Check = CheckBSODStatus()
        TDR_Check = CheckTDRStatus()
        strStepName = 'Check BSOD and TDR status'
        strDescription = 'BSOD ,TDR and Blankout should not occured'
        strExpected = 'BSOD, TDR and Blankout should not found'
        
        if ( ( BSOD_Check or TDR_Check ) == 0 ):
            print("----- Test Failed due to TDR/BSOD Found---------")
            strActual = 'BSOD and TDr Occured'
            strStatus = 'FAIL'
            report_lib.add_result(strStatus, strDescription, strStepName, strTestName, strExpected, strActual)

            
        if ( (BSOD_Check != 0) and (TDR_Check != 0) and (Blank_status == 1)):
            print("------- Test case failed due to blankout detection happen-----")
            strActual = 'Blankout detection Happen'
            strStatus = 'FAIL'
            report_lib.add_result(strStatus, strDescription, strStepName, strTestName, strExpected, strActual)

        if ( (BSOD_Check !=0 ) and (TDR_Check!=0) and (Blank_status == 0)):
            print("-------Test Passed---------")
            strActual = 'BSOD,TDR,Blankout not Occured'
            strStatus = 'PASS'
            report_lib.add_result(strStatus, strDescription, strStepName, strTestName, strExpected, strActual)
            


    if (sleep_dataFromServer.decode() == "tests completed"):
        exit(0)
    if not sleep_dataFromServer:
        exit(0)
