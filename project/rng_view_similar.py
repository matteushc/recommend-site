# -*- coding: utf-8 -*-
"""
  Locust swarm test using generated random users and urls for similar and view
  routes.
"""

import random
import numpy

from locust import HttpLocust, TaskSet, task

random.seed(13)


class UrlAccessTaskSet(TaskSet):

    @task(46)  # temos 46 vezes mais requests de view do que similar
    def view(self):
        url_id = numpy.random.binomial(n=10000, p=0.48)
        user_id = random.randint(1, 1000000)
        url = '/url.com.br/%s/view' % url_id
        self.client.post(url, json={"userId": url_id})

    @task(1)
    def similar(self):
        url_id = numpy.random.binomial(n=10000, p=0.48)
        url = '/url.com.br/%s/similar' % url_id
        self.client.get(url)


class UrlAccessLocust(HttpLocust):

    weight = 1
    task_set = UrlAccessTaskSet
    min_wait = 0
    max_wait = 5