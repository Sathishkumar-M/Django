from __future__ import absolute_import, unicode_literals
from celery import task
import random
@task()
def task_number_two(x,y):
    # Do another thing...
    total = x * (y * random.randint(3, 100))
    return total
