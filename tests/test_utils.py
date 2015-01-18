import unittest

from configkeeper import utils


class TestUtils(unittest.TestCase):
    def test_caller_module_default(self):
        caller_module = utils.caller_module()
        self.assertIn(caller_module, ('_pytest.config', 'nose.core',
                                      'distutils.core', 'nose2.main'))

    def test_caller_module_func_localisation(self):
        caller_module = utils.caller_module(0)
        self.assertEqual(caller_module, 'configkeeper.utils')

    def test_caller_module_who_import(self):
        caller_module = utils.caller_module(1)
        self.assertEqual(caller_module, __name__)

    def test_caller_module_main(self):
        caller_module = utils.caller_module(-1)
        self.assertEqual(caller_module, None)

    def test_caller_module_index_error(self):
        caller_module = utils.caller_module(50)
        self.assertEqual(caller_module, None)
