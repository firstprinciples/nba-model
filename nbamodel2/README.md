nbamodel2
==============================

cleaner project folder

Apeel Data Science Project Organization
------------

```
.
├── README.md                   <-- This README
├── apeel_nbamodel2  <-- package, named `apeel_<repo-name>` to avoid PyPI naming conflicts
│   ├── __init__.py             <-- Specify version number of package. <major>.<minor>.<build>
│   │                               Increments correspond to <API change>.<Feature addition>.<Improvement>    
│   ├── data                    <-- All data files
│   │   ├── external            <-- Outside data goes here
│   │   ├── raw                 <-- raw, immutable data file
│   │   └── transformed         <-- transformed, merged, etc version of raw data in `transformed.csv`
│   ├── figures                 <-- .png etc files.
│   ├── notebooks               <-- Jupyter notebooks, including EDA and formal reports.
│   ├── predict                 <-- API code for trained models. Use base class `TrainedModel`.
│   │   ├── __init__.py 
│   │   └── predict.py          
│   ├── train                   <-- Transform raw data and use transformed data to train models          
│   │   ├── __init__.py
│   │   ├── train.py            <-- Code that uses data in `transformed.csv` to train ML models and serialize them
│   │   │                           in `trained_models`. Use base class `ModelTrainer`. 
│   │   └── preprocess.py        <-- Transform data using DataTransformer
│   │                           <-- Optional: if needed, add module `dataset.py` to make/query dataset
│   └── trained_models          <-- Serialized trained models.
├── requirements.txt            <-- `pip freeze > requirements.txt` your vrtl env so that results can be reproduced. 
├── setup.py                    <-- make package installable with `pip install -e` and define `install_requirements`
│                                   `setup.py` = abstract requirements,  requirements.txt => concrete (versioned)
└── unit_tests
    └── test_environment.py
```
--------

