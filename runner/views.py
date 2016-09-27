import os
import json

from profiler import settings
from runner import models

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View


class TestCaseView(View):
 
    def get(self, request, test_id=None):
        """
        To get testcase(s) from DB.

        if user requests single record(try to access log file from table by
        requesting id value) will give log file. else will give all testcase
        records present in DB.

        Args:
            request: HTTP request obj
            test_id: pk of testcase db record that user interested defaults None.

        Return:
            HTTPResponse: returns log data stream/all testcases as json response.
        """
        try:
            if test_id:
                test = models.TestCase.objects.get(id = test_id)
                log_content = ''
                with open(test.log_file, "r") as input_file:
                    log_content = input_file.read()
                return HttpResponse(log_content, content_type='text/plain')
            else:
                tests = models.TestCase.objects.values(
                    'id','requester', 'environment', 'interface', 'testcase',
                    'status', 'fail', 'success')
                data = json.dumps(list(tests), cls=DjangoJSONEncoder)
                return HttpResponse(data)
        except Exception as e:
            return HttpResponse('Opps! something wrong try again after some time.')

    def post(self, request):
        """
        To save new testcase request.
        
        Note: It will create testcase record with respective to test cases select.

        Args:
            request: HTTP request obj.

        Return:
            HTTPResponse: returns success/fail message as json response.

        """
        try:
            for test in request.POST.getlist('testcase[]'):
                obj = models.TestCase.objects.create(
                    requester=request.POST.get('requester'),
                    environment=request.POST.get('environment'),
                    interface=request.POST.get('interface'),
                    testcase=test)
                obj.save()
            return HttpResponse('success')
        except Exception as e:
            return HttpResponse('Opps! something wrong')
