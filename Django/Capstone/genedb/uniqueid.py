#!/usr/bin/python
import time, random, md5
import sys, string
import os
import random
from datetime import timedelta
from datetime import date
from datetime import datetime

#keep username field 20 charavters long
#datetime 15 characters
d1= datetime.now().strftime("%Y%m%d%H%M%S")
seed1 = str(random.randint(1, 9));
seed2 = str(random.randint(1, 9));
seed3 = str(random.randint(1, 9));
seed4 = str(random.randint(1, 9));
seed5 = str(random.randint(1, 9));
seed6 = str(random.randint(1, 9));

str=d1+seed1+seed2+seed3+seed4+seed5+seed6;

####str has the value of the unique userid 

print("%s" %str);
