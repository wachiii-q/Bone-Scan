# BoneScan project
"Bone AI Classification" or "Bone Scan" project is a explainable prediction project. There are 2 main parts; data cleaning and classification model. Additionally, this project is the milestone of Wachiii-Raya's Internship.

## Getting started
This repository consists of 2 parts
1. Package: this includes modules, sources and utils for the "Bone Scan Project"
2. Main program: main program for executing

### Prerequisites
 - miniconda: python virtual environment

 ### Installation
 1. Clone this repository; if error existing in this step, recheck your authorize (did u add ssh-key?)

 2. get to project directory

        cd ./bone-scan

3. create new virtual environment using `conda`

        conda create --name bone-scan python=3.11

4. activate virtual environment 

        conda activate bone-scan

5. install packages

        pip install -e .

### Environments update

        pip install -e .

### Reinstallation

        pip install -e . --force-reinstall

## Usage
1. Clean data by selecting Anterior Posterior file. Execute clean_dicom.sh file

        bash clean_dicom.sh

2. Crop image and rename. Run dicom_handler.py file in folder bonescan/preprocessing

        python bonescan/preprocessing/dicom_handler.py

3. Extract the lable from nuclear medicians' report -> config filename in label_extraction.py file in bonescan/preprocessing
-- The extracted label will be saved as .csv format in data/report path (default - can be changed in label_extraction.py file)

        python bonescan/preprocessing/labels_extraction.py

4. Next, the modalities (device name, e.g. Discovery NM 870 DR, Discovery MI (PET) etc) can be extracted by running modality_extraction.py in bone/preprocessing

        python bonescan/preprocessing/modality_extraction.py

5. Merge extracted labels and modalities using merge_modality.py 

        python bonescan/preprocessing/merge_modality.py

6. Map labels with images using ACC 

        python bonescan/preprocessing/images_labels_mapping.py