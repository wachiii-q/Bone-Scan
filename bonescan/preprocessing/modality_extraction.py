# extract modalities from the report
# -- Date, HN, ACC, Age, BMI, Device
# Column
# data: "Date & time", need to remove time after date
# HN: "Patient ID"
# ACC: "Accession #"
# age: "Age"
# bmi: "BMI"
# device: "Device"

import pandas as pd
from bonescan.utils.common import log
from bonescan.utils.texttools import TextTools
import json


class ModalityExtraction:
    def __init__(self, reportFilePath, reportFileType):
        self.__reportFilePath = reportFilePath
        self.__reportFileType = reportFileType
        self.__reportDf = self.read_report_file()
        self.__numCases = self.__reportDf.shape[0]
        self.__reportPropList = []
        
    def read_report_file(self):
        '''
        function to read the report file, and return a dataframe to private variable __reportDf
        '''
        try: 
            if self.__reportFileType == 'xlsx':
                df = pd.read_excel(self.__reportFilePath)
        except Exception as e:
            df = None
            print('Error reading file: ', e)
        return df
    
    def get_properties_dict_template(self):
        '''
        function to get the properties dictionary template
        '''
        propertiesDict = {
            "index": None,
            "date": None,
            "HN": None,
            "ACC": None,
            "gender": None,
            "age": None,
            "BMI": None,
            "device": None
        }
        return propertiesDict
    
    def extract_properties(self):
        '''
        function to extract properties from the report data
        '''
        if self.__reportDf is None:
            log('Error: report file is empty')
            return None
        i = 0
        log(self.__reportDf)
        for i in range(self.__numCases):
            tempDict = self.get_properties_dict_template()
            tempDate = self.__reportDf.loc[i, 'Date']
            tempDate = str(tempDate)
            # tempDate = tempDate.split(' ')[0]
            tempHN = self.__reportDf.loc[i, 'Patient ID']
            tempHN = str(tempHN)
            tempACC = self.__reportDf.loc[i, 'Accession #']
            tempACC = str(tempACC)
            tempGender = self.__reportDf.loc[i, 'Sex']
            tempGender = str(tempGender)
            if tempGender == 'M':
                tempGender = 'Male'
            elif tempGender == 'F':
                tempGender = 'Female'
            tempAge = self.__reportDf.loc[i, 'Age']
            tempAge = str(tempAge)
            tempBMI = self.__reportDf.loc[i, 'BMI']
            tempBMI = str(tempBMI)
            tempDevice = self.__reportDf.loc[i, 'Device']
            tempDate = tempDate.replace('-', "/")
            i = i + 1
            tempDict['index'] = i
            tempDict['date'] = tempDate
            tempDict['HN'] = tempHN
            tempDict['ACC'] = tempACC
            tempDict['gender'] = tempGender
            tempDict['age'] = tempAge
            tempDict['BMI'] = tempBMI
            tempDict['device'] = tempDevice
            self.__reportPropList.append(tempDict)
        log(self.__reportPropList)
    
    def get_report_df(self):
        '''
        function to return the report dataframe
        '''
        return self.__reportDf
    
    def get_reportPropList(self):
        '''
        function to return the report properties
        '''
        return self.__reportPropList
    
    def get_reportPropList_df(self):
        '''
        function to return the report properties in dataframe
        '''
        return pd.DataFrame(self.__reportPropList)
    

if __name__ == "__main__":
    # --[/]: Drop NaN values in the report
    # reportFilePath = 'data/report/NMModality_2024.xlsx'
    # reportFileType = 'xlsx'
    # df = pd.read_excel(reportFilePath)
    # df = df.dropna(subset=['Date & time', 'Patient ID', 'Accession #', 'Age', 'BMI', 'Device'])
    # df.to_excel('data/report/Modified_NMModality_2024.xlsx', index=False)
    
    # --[/]: test the ModalityExtraction class
    reportFilePath = 'data/report/Modified_NMModality_2024.xlsx'
    reportFileType = 'xlsx'
    modalityExtraction = ModalityExtraction(reportFilePath, reportFileType)
    modalityExtraction.extract_properties()
    log(modalityExtraction.get_reportPropList_df())
    modalityExtraction.get_reportPropList_df().to_csv('data/report/Extracted_NMModality_2024.csv', index=False)
    
        

    