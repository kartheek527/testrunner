from __future__ import absolute_import

import time
import unittest
import importlib

from StringIO import StringIO
from celery import shared_task

from .models import TestCase



@shared_task
def run_test(task):
    """
    TO run the tests.

    Step1:
      Here this task wait for 60 sec to give real feel user.
    Step2:
      Read the test form test module(test dir) based on seleted tests.
    Step3:
      Create test suite and run the tests using unittest module.
    Step4:
      Create log file to capture log and save the logs after test runs.
    Step5:
      Update the status(success/fail) of test record. 

    """

    time.sleep(60)
    module = importlib.import_module('tests.'+task.testcase)
    alltests = unittest.findTestCases(module)
    log_file = 'test_logs/log_file_' + str(task.id)+'.txt'
    with open(log_file, "w") as log_obj:
        runner = unittest.TextTestRunner(log_obj)
        result = runner.run(alltests)

    if result.errors or result.failures:
        task.status = "failed"
    else:
        task.status = "success"
    task.success = result.testsRun - (len(result.errors)+len(result.failures))
    task.fail = (len(result.errors)+len(result.failures))
    task.log_file = log_file
    task.save()
    return "successfully runned tests"
   

@shared_task
def schedule_tests():
    """
    To check and run waiting tests every 30 secs.

    step1:
      Get all waiting records in DB.
    step2:
      run the tset case if env is not running by any tests
    """
    waiting_tests = TestCase.objects.filter(status = 'waiting')

    for test in waiting_tests:
        print test.requester+' '+test.status+' '+test.environment
        if not TestCase.objects.filter(environment = test.environment, status = "running"):
            test.status = "running"
            test.save()
            run_test.delay(test)
    return "finally am done."
