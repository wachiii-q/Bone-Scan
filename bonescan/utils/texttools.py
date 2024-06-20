# functions for preprocessing text data
# if the properties are not found, the value is set to "not defined"

from bonescan.utils.common import log


class TextTools:
    def __init__(self):
        pass
    
    @staticmethod
    def split_text(text, text1, text2):
        '''
        function that split the text between "text1" and "text2"
        '''
        text = text.lower()
        text1 = text1.lower()
        text2 = text2.lower()
        # handling of misspelled words TODO: make it more feasible; json key
        if "histor" in text:
            text1 = "histor"
        if text1 not in text:
            text1 = "impresions"
            if text1 not in text:
                text1 = "impreesion"
                if text1 not in text:
                    text1 = "impresssion"
                    if text1 not in text:
                        text1 = "impressoin"
        #TODO: Raise if not found -> show which index is not found
        if (text2 == "end of report"):
            text = text.split(text1)[1]               # split text between text1 and end of text
        else:     
            try:
                if ("history" not in text) and ("histor" not in text):
                    # split all before text2
                    text1 = "bone"
                    text = text.split(text1)[1].split(text2)[0]
                    return text
                text = text.split(text1)[1].split(text2)[0]
            except:
                text = None
        return text
        
    @staticmethod
    def word_search_and_split_both(text: str, wordLst: list, num_words: int): # TODO: refactor this function
        '''
        function that search for a word in a text and split the text before and after the word for length characters
        '''
        text = text.lower()
        # convert text to list of words
        words = text.split()
        # handle case with '.' at the end of the word
        for i in range(len(words)):
            if '.' in words[i]:
                words[i] = words[i].replace('.', '')
            if ' ' in words[i]:
                words[i] = words[i].replace(' ', '')
        for i in range(len(wordLst)):
            tmpWord = str(wordLst[i])
            if tmpWord in words:
                index = words.index(wordLst[i])
                frontWordsLst = []
                try:
                    if index - num_words > 0:
                        frontWordsLst = words[index-num_words:index + num_words]
                    else:
                        frontWordsLst = words[:index + num_words]
                except:
                    frontWordsLst = words[:index + num_words]
                splitText = ' '.join(frontWordsLst)
                return splitText
            else:
                pass
        return None
    
    @staticmethod
    def word_search_and_split_front(text: str, wordLst: list, num_words: int):
        '''
        function that search for a word in a text and split the text before the word for num_words
        '''
        text = text.lower()
        # convert text to list of words
        words = text.split()
        # handle case with '.' at the end of the word
        for i in range(len(words)):
            if '.' in words[i]:
                words[i] = words[i].replace('.', '')
            if ' ' in words[i]:
                words[i] = words[i].replace(' ', '')
        for i in range(len(wordLst)):
            tmpWord = str(wordLst[i])
            if tmpWord in words:
                index = words.index(wordLst[i])
                frontWordsLst = []
                try:
                    if index - num_words > 0:
                        frontWordsLst = words[index-num_words:index]
                    else:
                        frontWordsLst = words[:index]
                except:
                    frontWordsLst = words[:index]
                splitText = ' '.join(frontWordsLst)
                return splitText
            else:
                pass
        return None
        
    
    @staticmethod
    def search_gender(text):
        '''
        function that search for gender in a text (HISTORY section)
        '''
        log(text)
        text = text.lower()
        if ("woman" or "female" or "women") in text:
            gender = "female"
        elif ("man" or "male" or "men") in text:
            gender = "male"
        else:
            gender = "not defined"
        return gender
    
    @staticmethod
    def search_age(text):
        '''
        function that search for age in a text (HISTORY section)
        '''
        text = text.lower()
        if ("year-old" or "years-old" or "year old" or "years old") in text:
            age = text.split("-year-old")[0].split()[-1]
            try:
                age = int(age)
            except:
                age = "not defined"
            return age
        else:
            return "not defined"
        
    @staticmethod
    def search_cancer_type(text):
        ''' 
        function that search for cancer type in a text (HISTORY section)
        '''
        text = text.lower()
        if ("cancer" or "carcinoma") in text:
            # get word before cancer; characters until found space
            cancerType = text.split("cancer")[0].split()[-1]
            log(cancerType)
            return cancerType
        else:
            return "not defined"
        
    @staticmethod
    def search_is_metastasis(text):
        '''
        function that search for metastasis in a text (IMPRESSION section) return in 3 classes
        - no metastasis
        - not sure
        - metastasis
        '''
        text = text.lower()
        spitedText = TextTools.word_search_and_split_front(text, ['metastasis', 'metastases'], 6)
        log(spitedText)



if __name__ == '__main__':
    # ------------------- test cases: other text functions -------------------
    # --[/]: search_is_metastasis
    
    # ------------------- test cases: basic text functions -------------------
    # --[ ]: test split_text function
    text = "This is HISTORY section. This is fsfklgnlkansfv IMPRESSION sectionuhhkjkjjk;j;k;."
    result = TextTools.split_text(text, 'HISTORY', 'END OF REPORT')
    log(result)
    
    # --[/]: test word_search_and_split function
    text = "This is HISTORY section. meta This is fsfklgnlkansfv IMPRESSION section."
    result = TextTools.word_search_and_split_both(text, 'meta', 5)
    log(result)
    
    # --[/]: test search gender
    text = "This is HISTORY section. woman s fsfklgnlkansfv IMPRESSION section."
    gender = TextTools.search_gender(text)
    log(gender)
    
    # --[/]: test search age
    text = "A 76-year-old woman with lung cancer was sent to evaluate bone metastasis"
    age = TextTools.search_age(text)
    log(age)

    # --[/]: test search cancer type    TODO: add more test case
    text = "A 76-year-old woman with lung cancer was sent to evaluate bone metastasis"
    cancer_type = TextTools.search_cancer_type(text)
    
    # --[/]: test word_search_and_split_front
    text = "no definite evidence of bone metastasis. degenerative change at lower cervical "
    result = TextTools.word_search_and_split_front(text, ['metastasis', 'metastases'], 6)
    log(result)
        # --[/]: test word_search_and_split_front: case big number; more than index 
    result_1 = TextTools.word_search_and_split_front(text, ['metastasis', 'metastases'], 100)
    log(result_1)
        # --[/]: test word_search_and_split_front: case small number; less than index
    result_2 = TextTools.word_search_and_split_front(text, ['metastasis', 'metastases'], 1)
    log(result_2)
        # --[/]: test word_search_and_split_front: case no word found
    result_3 = TextTools.word_search_and_split_front(text, ['metastatic'], 6)
    log(result_3)
        # --[/]: test word_search_and_split_front: handle case with '.' at the end of the word
    text = "no definite evidence of bone metastasis. degenerative change at lower cervical."
    result_4 = TextTools.word_search_and_split_front(text, ['metastasis', 'metastases'], 6)
    log(result_4)
        # --[ ]: test word_search_and_split_front: None input; user should not input None
