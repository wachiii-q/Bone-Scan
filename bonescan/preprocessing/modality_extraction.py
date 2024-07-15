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
            "Date": None,
            "HN": None,
            "ACC": None,
            "Age": None,
            "BMI": None,
            "Device": None
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
        for i in range(self.__numCases):
            tempDict = self.get_properties_dict_template()
            tempDate = self.__reportDf.loc[i, 'Date & time']
            # the result would be "9/7/2024  13:14:31", split time out
            tempDate = tempDate.split(' ')[0]
            tempHN = self.__reportDf.loc[i, 'Patient ID']
            tempACC = self.__reportDf.loc[i, 'Accession #']
            tempACC = str(tempACC)
            tempAge = self.__reportDf.loc[i, 'Age']
            tempAge = str(tempAge)
            tempBMI = self.__reportDf.loc[i, 'BMI']
            tempBMI = str(tempBMI)
            tempDevice = self.__reportDf.loc[i, 'Device']
            tempDict['Date'] = tempDate
            tempDict['HN'] = tempHN
            tempDict['ACC'] = tempACC
            tempDict['Age'] = tempAge
            tempDict['BMI'] = tempBMI
            tempDict['Device'] = tempDevice
            self.__reportPropList.append(tempDict)
            i = i + 1
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
    reportFilePath = 'data/report/NMModality_2024.xlsx'
    reportFileType = 'xlsx'
    modalityExtraction = ModalityExtraction(reportFilePath, reportFileType)
    modalityExtraction.extract_properties()
    log(modalityExtraction.get_reportPropList_df())
    modalityExtraction.get_reportPropList_df().to_csv('data/report/Extracted_NMModality_2024.csv', index=False)
    
        

    