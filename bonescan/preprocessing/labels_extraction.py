# extract labels and properties of the samples from bone scan report
# the report is typically consists of 3 main sections; HISTORY, FINDINGS, IMPRESSION
# labels and properties to be extracted are:
# 1. gender
# 2. age
# 3. type of cancer
# 4. is_metastasis
# 5. is degenerative infection
# 6. is fracture

class LabExtraction:
    def __init__(self, report):
        self.report = report
        self
