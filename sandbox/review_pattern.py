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
        log(tmpImpressionText)
        i = i + 1
        log('Case: ', i)
    