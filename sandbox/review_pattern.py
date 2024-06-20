from bonescan.utils.common import log
from bonescan.utils.texttools import TextTools
import pandas as pd  


if __name__ == '__main__':
    # -- Step 1: cut the part of "IMPRESSION" section
    filePath = "./data/BoneReport_2018.xlsx"
    reportDf = pd.read_excel(filePath)
    impressionTextLst = []      # -- initialize list to store the impression text
    log(reportDf.head())
    numCases = reportDf.shape[0]
    log('Number of cases: ', numCases)
    i = 0
    for case in range(numCases):
        reportText = reportDf.loc[case, 'Report']
        tmpImpressionText = TextTools.split_text(reportText, 'IMPRESSION', 'end of report')
        impressionTextLst.append(tmpImpressionText)
        i = i + 1
    lenImpressionText = len(impressionTextLst)
    log('Number of impression text: ', lenImpressionText)
    
    # -- Step 2: convert list of text to dataframe
    impressionDf = pd.DataFrame(impressionTextLst, columns=['Impression'])
    numCases = impressionDf.shape[0]
    
    # -- Step 3: loop check for the misspelled word "metastasis" in the impression text
    j = 0
    for case in range(500, 1000):
        tmpText = impressionDf.loc[case, 'Impression']
        tmpText = str(tmpText)
        if "metastasis" or "metastases" in tmpText:
            log("Metastasis found in case ", j)
            log(tmpText)
        else:
            log(tmpText)
            log("Metastasis not found in case ", j)
            break
        j = j + 1
    
    # -- Step 4:
    