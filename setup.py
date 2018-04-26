#!/usr/bin/python
# -*- coding: UTF-8 -*-
from setuptools import setup

from oshino_zmq.version import get_version


setup(name="oshino_zmq",
      version=get_version(),
      description="ZeroMQ consumer for Oshino",
      author="Šarūnas Navickas",
      packages=["oshino_zmq"],
      install_requires=[
        'oshino',
        'pyzmq'
      ],
      test_suite="pytest",
      tests_require=["pytest", "pytest-cov"],
      setup_requires=["pytest-runner"]
      )
