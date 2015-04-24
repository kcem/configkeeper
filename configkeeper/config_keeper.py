# -*- coding: utf-8 -*-

"""
Copyright (c) Konrad Cempura, All rights reserved.
This library is free software; you can redistribute it and/or
modify it under t he terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3.0 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public
License along with this library.
"""

import logging
import yaml

from pkg_resources import resource_filename, resource_string
try:
    from yaml import CLoader as Loader

except ImportError:
    from yaml import Loader  # lint:ok

from .utils import caller_module

LOG = logging.getLogger(__name__)


class ConfigKeeperError(Exception):
    """ Usage errors """
    pass


class ConfigKeeper(object):
    def __init__(self, name='config.yaml', from_module=None,
                 strict_keys=False):
        self.name = name
        self.module = from_module or caller_module()

        self.strict_keys = strict_keys

        self._config = {}
        self._collapsed_sections = None

        self._load_default()

    def _cut_last(self, name):
        idx = name.rfind('.')
        if idx < 0:
            return None
        prev = name[:idx]
        LOG.debug('Search %s in precedent module: %s -> %s',
                  self.name, name, prev)
        return prev

    def _read_default(self):
        """
        Returns:
            default configuration file content
        """
        module = self.module
        try:
            fn_default = resource_filename(module, self.name)

        except ImportError as err:
            raise ConfigKeeperError('ImportError: {}'.format(err))

        while True:
            try:
                default = resource_string(module, self.name)
                LOG.debug('Loaded default config values; file: %s', fn_default)
                break

            except IOError as err:
                LOG.debug('%s: IOError: %s', fn_default, str(err))

            module = self._cut_last(module)
            if module is None:
                raise ConfigKeeperError('Cannot load default config file')

        return default

    def _load_default(self):
        c_default = self._read_default()

        self._config = yaml.load(c_default, Loader=Loader)
        self._collapsed_sections = None

    def save_default(self, config_file):
        c_default = self._read_default()

        with open(config_file, 'wb') as f_hndl:
            f_hndl.write(c_default)

        LOG.info('Config saved; file: %s', config_file)

    def load_config(self, config_file):
        LOG.info('Loading config; file: %s', config_file)

        with open(config_file) as f_hnd:
            c_user = yaml.load(f_hnd.read(), Loader=Loader)

        key_error = []
        for key in c_user.viewkeys():
            if key in self._config:
                continue

            LOG.warning('Unrecognized config key: {}'.format(key))
            key_error.append(key)

        if self.strict_keys and key_error:
            raise ConfigKeeperError('Unrecognized config key: {}'
                                    .format(', '.join(key_error)))

        self._config.update(c_user)
        self._collapsed_sections = None

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value

    def __getattr__(self, name):
        try:
            return self._config[name]

        except KeyError:
            raise AttributeError(
                "'{}' object has no attribute '{}'".format(
                    self.__class__.__name__, name
                )
            )
