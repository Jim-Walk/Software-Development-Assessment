# Software-Development-Assessment
Repo for the assessment for Software Development Course at the University of Edinburgh 2018

## Requirements
* [mongodb](https://docs.mongodb.com/manual/installation/#tutorials)
* [python3](https://www.python.org/downloads/)
* packages: pymongo, flask_pymongo, config, helpers

Setup on a Debian-based system:
```
sudo apt install python3 python3-pip mongodb-server
```


For use with python3. Install necessary python packages with 
```
pip install website/requirements.txt
```

## Quick Start

After you've installed mongodb and you're sure it's up and running, simply import the data using the import script.
```
cd db/ && unzip dump.zip && mongorestore && cd ..
```

We have also included the import script we used for the original import. We have modified it so that you can specify how many records are included. We recommend importing at least 20000 records. Please note that this method is much slower than using `mongorestore`
```
python3 database.py 20000
```
Whilst we have implemented a web crawler for institution images, this requires an API key. Get a key from [this page](https://developers.google.com/custom-search/v1/overview) and place it in a file named config.py, in the following format:

```
API_KEY = '&key=$YOUR_KEY'
```

You can then run the server. 
```
python3 routes.py local
```

Visit the website at http://127.0.0.1:5000. We have also hosted an [instance of the website](http://ec2-18-130-215-119.eu-west-2.compute.amazonaws.com) on Amazon Web Services if you want to simply use the site without installing it.

