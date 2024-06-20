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
    # j = 0
    # k = 0
    # for case in range(500, 1000):
    #     tmpText = impressionDf.loc[case, 'Impression']
    #     tmpText = str(tmpText)
    #     # if "metastasis" or "metastases" in tmpText:
    #     if "evidence" in tmpText:
    #         # log("Metastasis found in case ", j)
    #         # log(tmpText)
    #         # log("Evidence found in case ", j)
    #         k = k + 1
    #         log(k)
    #     else:
    #         # log(tmpText)
    #         # log("Metastasis not found in case ", j)
    #         log("Evidence not found in case ", j)
    #         log(tmpText)
    #         # break
    #     j = j + 1
    
    # -- Step 4: check word "evidence" in the impression text; for defining no metastasis; "no" & "evidence" in the same sentence
    j = 0
    k = 0
    l = 0
    for case in range(numCases):
        tmpText = impressionDf.loc[case, 'Impression']
        tmpText = str(tmpText)
        tempText = TextTools.word_search_and_split_both(tmpText, ['metastasis', 'metastases', 'bbone metastasis', 'bskeletal metastasis', 'metastatic'], 10)
        # if "metastasis" or "metastases" in tmpText:
        if "evidence" in tmpText:
            if "no" in tmpText:
                k = k + 1
                pass
                log(k)
                log(tmpText)
            # else:
                # pass
        # elif "cannot exclude" in tmpText:
        #     k = k + 1
        #     log(k)
        #     log(tmpText)
        #     pass
        elif "no definite bone metastases" in tmpText:
            k = k + 1
            pass
            # log(k)
        else:
            # log(tempText)
            # log(tmpText)
            # check None
            if tempText is None:
                pass
            else:
                if "progressive" in tempText:
                    l = l + 1
                    # log(l)  
                    # log(tempText)
                    pass
                elif "improvement" in tempText:
                    l = l + 1
                    # log(l)
                    # log(tempText)
                    pass
                elif "extensive" in tempText:
                    l = l + 1
                    # log(l)
                    # log(tempText)
                    pass
                elif "multiple" in tempText:
                    l = l + 1
                    # log(l)
                    # log(tempText)
                    pass
                elif "widespread" in tempText:
                    l = l + 1
                    # log(l)
                    # log(tempText)
                    pass
                elif "diffuse" in tempText:
                    l = l + 1
                    # log(l)
                    # log(tempText)
                    pass
                elif "new" in tempText:
                    l = l + 1
                    # log(l)
                    # log(tempText)
                    pass
                elif "bone metastasis at" in tempText:
                    l = l + 1
                    # log(l)
                    # log(tempText)
                    pass
                elif "bone metastases at" in tempText:
                    l = l + 1
                    # log(l)
                    # log(tempText)
                    pass
                elif "stable bone metastasis" in tempText:
                    l = l + 1
                    # log(l)
                    # log(tempText)
                    pass
                elif "bony metastases" in tempText:
                    l = l + 1
                    # log(l)
                    # log(tempText)
                    pass
                elif "skeletal metastases" in tempText:
                    l = l + 1
                    # log(l)
                    # log(tempText)
                    pass
                elif "bony metastasis" in tempText:
                    l = l + 1
                    # log(l)
                    # log(tempText)
                    pass
                else:
                    # pass
                    log(l)
                    # log(tempText)
            # log("Evidence not found in case ", j)
            
            # log(l, tempText)
        j = j + 1
        log(j)
        log(k)
        log(l)