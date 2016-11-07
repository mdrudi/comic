#! /usr/bin/env python

# SAMPLE:
#
# $>jmonth.py "197001" +20
# 197109
# $>


import sys
import datetime
from dateutil.relativedelta import relativedelta

out = datetime.datetime.strptime(sys.argv[1], "%Y%m") + relativedelta(months=int(sys.argv[2]))
print out.strftime("%Y%m")
