# Software-Development-Assessment
Repo for the assessment for Software Development Course at the University of Edinburgh 2018

## Requirements
* [mongodb](https://docs.mongodb.com/manual/installation/#tutorials)
* [python3](https://www.python.org/downloads/)
* packages: pymongo, flask_pymongo, config, helpers

For use with python3. Install necessary packages in either the website or the crawler folder with `pip install -r website/requirements.txt`

## Quick Start

After you've installed mongodb and you're sure it's up and running, simply import the data using the import script in the db folder.
```
python3 db/import.py
```

You can then run the server 
```
python3 website/routes.py
```


Visit the website at http://127.0.0.1:5000

pymongo
