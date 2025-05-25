# IMPORTING PACKAGES ************************************************************

import pandas as pd

import comtradeapicall
import time
import os

# COMTRADE SUBSCRIPTION KEY *****************************************************

subscription_key = os.getenv("COMTRADE_API_KEY")
if not subscription_key:
    raise ValueError("COMTRADE_API_KEY environment variable must be set")

# CODES *************************************************************************

commodities = pd.read_csv('comtrade_codes/harmonized-system.csv')

reporters = pd.read_csv('comtrade_codes/reporterAreas.csv')
partners = pd.read_csv('comtrade_codes/partnerAreas.csv')

# EXTRACTING THE DATA ***********************************************************

comtrade_exp = comtradeapicall.getFinalData(subscription_key,
                                            typeCode='C',
                                            freqCode='A',
                                            clCode='HS',
                                            period='2022',
                                            reporterCode=None,
                                            cmdCode='1001',
                                            flowCode='X',
                                            partnerCode=None,
                                            partner2Code='0',
                                            customsCode='C00',
                                            motCode='0',
                                            maxRecords=250000)

time.sleep(10)

comtrade_imp = comtradeapicall.getFinalData(subscription_key,
                                            typeCode='C',
                                            freqCode='A',
                                            clCode='HS',
                                            period='2022',
                                            reporterCode=None,
                                            cmdCode='1001',
                                            flowCode='M',
                                            partnerCode=None,
                                            partner2Code='0',
                                            customsCode='C00',
                                            motCode='0',
                                            maxRecords=250000)

print(comtrade_exp.head())
print(comtrade_imp.head())
