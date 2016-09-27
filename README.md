Profiler
====
```
This web application is to run tests in diffrent environments, also to view historical test runs.
```
**How to use?**
* **Step1:** To setup & run development environment follow the instructions #1, #2, #3 in getting setup section. Open application in browser by accessing the url http://localhost:8000/.
* **Step2:** Request/create new test run by using **Create new test** form in aplication. The requested test run is displayed in the table under **Test execution requests** section.
* **Step3:** User can get the live status by hitting the refresh button(also automatically updated by every one min).
* **Step4:** User can access the log by clicking on the id of the test case.

**How it works?**
* **Step1:** The initial state of the test run will be in waiting when user requets a new test run.
* **Step2:** A celery worker is scheduled to run every 30 secs to pull all the waiting test runs from the database and puts them into a redis queue (**run_test**). If the requested environment is already running in the queue it gets discarded.
* **Step3:** The **run_test** worker gets the test run, waits for 60 sec (to simulate the real time processing), executes the tests and updates the status of the tests run and writes to a log file.

## Getting Started
#### 1. Using virtual Environment(virtualenv):
* Download & cd to project_repo
* `cd Project`
* If virtualenv is not installed do `pip install virtualenv`, `virtualenv venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`
* Set up DB, present am using sqlite3
* `python manage.py makemigrations`(not required every time)
* `python manage.py migrate`(not required every time)
* `python manage.py runserver`

### 2. Setting up Redis
* [Download](http://redis.io/download) and [install](http://redis.io/download#installation) Redis
* To run `cd path_to_redis_folder` and `src/redis-server`

### 3. Setting up celery
* `cd Project_dir`
* `source venv/bin/activate`
* `celery -A profiler.celery worker -B --loglevel=info`


About folders/files
----
 ```
    profiler
    │   └───profiler
    │       │   celery.py, settings.py, urls.py, etc.
    │   manage.py
    │   README.md
    │   └───app
    │       │   models.py, migrations(dir), templatetags(dir),  views.py, tasks.py, etc.
    │   └───test
    │       │   test.py, test1.py
    │   └───test_logs
    │       │   log_file_<id*>.txt
    │   └───sample_screens
    │       │   *.png
```    

**Some imp files/folders :**

> - `profiler/celery.py` main celery configuration. 
> - `profiler/settings.py` Project related django settings.
> - `runner(dir)` this is django app contains models, views, celery tasks, templatetags.
> - `test(dir)` Contains tests to choose one or more files to test in request form.
> - `test_logs(dir)` . contains log files that generated while executing tests.
> - `requirements.txt` Contains depenedecy packeges/modules used for this tool.


### Tech stack used:
* **python**
* **django**
* **celery**
* **redis**
* **unittest**
* **Angular Material**
