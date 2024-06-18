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
        # handling of misspelled words
        if text1 not in text:
            text1 = "impresions"
            if text1 not in text:
                text1 = "impreesion"
                if text1 not in text:
                    text1 = "impresssion"
                    if text1 not in text:
                        text1 = "impressoin"
        if (text2.lower() == "end of report"):
            # split text between text1 and end of text
            text = text.split(text1)[1]   
        else:     
            try:
                text = text.split(text1)[1].split(text2)[0]
            except:
                text = None
        return text
        
    @staticmethod
    def word_search_and_split(text, word, length):
        '''
        function that search for a word in a text and split the text before and after the word for length characters
        '''
        text = text.lower()
        word = word.lower()
        try:
            index = text.index(word)
            word_length = len(word)
            text = text[index-length:index+word_length+length]
        except:
            text = None
        return text
    
    @staticmethod
    def search_gender(text):
        '''
        function that search for gender in a text (HISTORY section)
        '''
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
        function that search for metastasis in a text (IMPRESSION section)
        '''
        text = text.lower()
        
        
    
        



if __name__ == '__main__':
    # --[ ]: test split_text function
    text = "This is HISTORY section. This is fsfklgnlkansfv IMPRESSION sectionuhhkjkjjk;j;k;."
    result = TextTools.split_text(text, 'HISTORY', 'END OF REPORT')
    log(result)
    
    # --[/]: test word_search_and_split function
    text = "This is HISTORY section. meta This is fsfklgnlkansfv IMPRESSION section."
    result = TextTools.word_search_and_split(text, 'meta', 5)
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