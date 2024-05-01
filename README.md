# Older, Smarter, Richer: Streamlit Dashboard

This repository contains the code that runs the [website](https://older-smarter-richer.streamlit.app/)
 
* The main file is Interactive_Charts.py
  * Subpages can be found in the pages folder
* For more information about raw data, EDA, and the general project proposal check out the website and our [data cleaning repository](https://github.com/justinreed23/investingBackend)

## Want to run this dashboard natively?

```
# download files (you can do this via github desktop too)
cd <path to your preferred folder> # don't put a repo inside a repo!
git clone https://github.com/justinreed23/Older-Smarter-Richer.git

# move the terminal to the new folder
cd Older-Smarter-Richer

# set up the packages you need for this app to work 
conda env create -f streamlit_env.yml

# activate the environment created by env-config.yml
conda activate streamlit-env

# start the app in a browser window
streamlit run Interactive_Charts.py

```

## Running after first install
```
# In Conda
cd <path to Older-Smarter-Richer folder>
conda activate streamlit_env
```