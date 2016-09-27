from __future__ import unicode_literals

from django.db import models


class TestCase(models.Model):
    """
    TestCase model to save the requested testcases by the user.
    """

    requester = models.CharField(max_length=30)
    environment = models.CharField(max_length=30)
    interface = models.CharField(max_length=30)
    testcase = models.CharField(max_length=30)
    status = models.CharField(max_length=30, default="waiting")
    log_file = models.CharField(max_length=30, null=True)
    fail = models.CharField(max_length=30, null=True)
    success = models.CharField(max_length=30, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.requester
