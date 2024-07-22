# merge  extracted information and modality information
# -- step 1: combine date and HN as 1 column
# -- step 2: match 2 dataframe together by HN and Date

import pandas as pd
from bonescan.utils.common import log


class MergeModality:
    def __init__(self, mainReportFilePath, modalityReportFilePath, fileType):
        self.__mainReportFilePath = mainReportFilePath
        self.__modalityReportFilePath = modalityReportFilePath
        self.__fileType = fileType
        self.__mainReportDf = self.read_report_file(self.__mainReportFilePath)
        self.__modalityReportDf = self.read_report_file(self.__modalityReportFilePath)
        self.__mergedDf = None
        
    def read_report_file(self, filePath):
        '''
        function to read the report file, and return a dataframe to private variable __reportDf
        '''
        try: 
            if self.__fileType == 'xlsx':
                df = pd.read_excel(filePath)
            elif self.__fileType == 'csv':
                df = pd.read_csv(filePath)
        except Exception as e:
            df = None
            print('Error reading file: ', e)
        return df
    
    def merge_modality(self):
        '''
        function to merge the main report and modality report
        '''
        df1 = self.__mainReportDf
        df2 = self.__modalityReportDf
        df1 = df1.drop(['index', 'gender'], axis=1)
        df2 = df2.drop(['index', 'date', 'HN', 'age'], axis=1)
        self.__mergedDf = pd.merge(df1, df2, on='ACC')
        
    def get_merged_df(self):
        '''
        function to return the merged dataframe
        '''
        return self.__mergedDf
        

if __name__ == '__main__':
    mainReportFilePath = 'data/report/Extracted_Bone_2024.csv'
    modalityReportFilePath = 'data/report/Extracted_NMModality_2024.csv'
    fileType = 'csv'
    mergeModality = MergeModality(mainReportFilePath, modalityReportFilePath, fileType)
    mergeModality.merge_modality()
    mergedDf = mergeModality.get_merged_df()
    log(mergedDf)
    mergedDf.to_csv('data/report/Merged_2024.csv', index=True)
    
    