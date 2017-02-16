#!/usr/bin/env python

from distutils.core import setup

setup(name='QTdata',
      version='0.1',
      description='QT database',
      author='Phil G',
      email = 'areseye@163.com',
      packages=['QTdata'],
      package_data = {'QTdata': ['QTdb_full/*',
          'ContinousExpertMarkRangeList/*',
          'QT_TestRegions/*',
          'QTwhiteMarkList/*']},
     )
