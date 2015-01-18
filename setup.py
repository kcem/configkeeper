#!/usr/bin/env python

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = ''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)


setup(
    name='configkeeper',
    version='0.1',
    description='Config file keeper',
    author='Konrad Cempura',
    author_email='kcem@op.pl',
    url='https://github.com/kcem/configkeeper',
    packages=['configkeeper'],
    tests_require=['tox'],
    cmdclass={'test': Tox},
)
