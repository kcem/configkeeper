import unittest
from mock import patch

from configkeeper.config_keeper import ConfigKeeper, ConfigKeeperError


class TestConfigKeeper(unittest.TestCase):
    def setUp(self):
        self.test_modules = ('_pytest.config', 'nose.core')

        self.s_config = """\
        general:
          option1: value1
          option2: value2
          option3: value3

        # comment
        module1:
          option1: value11
          option4: value14

        module2:
          option2: value22
          option4: value24

        module3:
          list_of_options:
            - opt1
            - opt1
            - opt2
          json_hash: {"key1": "val1",
                      "key2": "val2"}
        """

    def test_read_default_resource_filename_importerror(self):

        with patch('configkeeper.config_keeper.resource_filename',
                   side_effect=ImportError('Not found')) as res:

            with self.assertRaises(ConfigKeeperError) as exc_ctx:
                ConfigKeeper()

            self.assertEqual(str(exc_ctx.exception), 'ImportError: Not found')

        res.assert_called_once()
        self.assertEqual(res.call_args[0][1], 'config.yaml')
        self.assertIn(res.call_args[0][0], self.test_modules)

    def test_read_default_resource_string_ioerror_and_notfound(self):
        with patch('configkeeper.config_keeper.resource_string',
                   side_effect=IOError('Cannot read')) as res:

            with self.assertRaises(ConfigKeeperError) as exc_ctx:
                ConfigKeeper()

            self.assertEqual(str(exc_ctx.exception),
                             'Cannot load default config file')

            res.assert_called()
            self.assertEqual(res.call_args_list[0][0][1], 'config.yaml')
            self.assertIn(res.call_args_list[0][0][0], self.test_modules)

            test_modules = ['.'.join(mod.split('.')[:-1])
                            for mod in self.test_modules]
            self.assertEqual(res.call_args_list[1][0][1], 'config.yaml')
            self.assertIn(res.call_args_list[1][0][0], test_modules)

    def test_read_default_resource_string_ioerror_and_found(self):
        with patch('configkeeper.config_keeper.resource_string',
                   side_effect=[IOError('Cannot read'), self.s_config]) as res:

            ConfigKeeper()

            res.assert_called()
            self.assertEqual(res.call_args_list[0][0][1], 'config.yaml')
            self.assertIn(res.call_args_list[0][0][0], self.test_modules)

            test_modules = ['.'.join(mod.split('.')[:-1])
                            for mod in self.test_modules]
            self.assertEqual(res.call_args_list[1][0][1], 'config.yaml')
            self.assertIn(res.call_args_list[1][0][0], test_modules)

    def test_read_default_resource_string_ok(self):
        with patch('configkeeper.config_keeper.resource_string',
                   return_value=self.s_config) as res:

            ConfigKeeper()

            res.assert_called_once()
            self.assertEqual(res.call_args[0][1], 'config.yaml')
            self.assertIn(res.call_args[0][0], self.test_modules)
