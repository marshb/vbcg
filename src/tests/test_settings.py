#!/usr/bin/env python
# -*- coding: ascii -*-
"""test_settings.py - tests for src/settings.py"""

import nose
import settings
import numpy as np
import threading
import os
import os.path

from defines import *

from nose.tools import assert_equal, assert_not_equal, assert_true


class Test(object):

    def setUp(self):
        # Backup current options
        self.backup_settings = settings.get_parameters()

    def tearDown(self):
        for i in range(0, np.size(self.backup_settings)):
            settings.change_parameter(i, self.backup_settings[i])

    def test_flip_parameter(self):

        # Get current settings
        self.curr_settings = settings.get_parameters()

        # Flip parameter in settings
        settings.flip_parameter(IDX_CURVES)

        # Flip parameters on local copy
        self.curr_settings[IDX_CURVES] = 1 - self.curr_settings[IDX_CURVES]

        # Check if both are equal
        assert_equal(np.count_nonzero(self.curr_settings - settings.get_parameters()), 0)

    def test_change_parameter(self):
        # Get current settings
        self.curr_settings = settings.get_parameters()

        # Get current value
        curr_value = self.curr_settings[IDX_FPS]

        # Change parameter in settings
        settings.change_parameter(IDX_FPS, curr_value + 1)

        # Check if both are equal
        assert_not_equal(np.count_nonzero(self.curr_settings - settings.get_parameters()), 0)

        # Change parameter in settings
        settings.change_parameter(IDX_FPS, curr_value + 1)

    def test_determine_if_under_testing(self):
        # Check if currently under testing
        assert_true(settings.determine_if_under_testing())

    def test_enforce_file_not_found(self):
        """Check if settings.py writes settings.ini file if it does not exist"""

        # Backup settings and remove file
        os.rename('settings.ini', 'settings_backup.ini')
        # Let settings find no file
        settings.get_parameters()
        # Check if file has been written
        ret = os.path.exists('settings.ini')
        # Remove file created by settings.py()
        os.remove('settings.ini')
        # Restore backup file
        os.rename('settings_backup.ini', 'settings.ini')

        assert_true(ret)

    def test_enforce_exception_when_reading_file(self):
        """Call multiple threads so that the settings file can not be read"""

        # Get number of lines in logfile
        num_lines_before = sum(1 for line in open('data/LOGFILE'))

        for x in range(0, 10000):
            curr_settings = settings
            t = threading.Thread(target=curr_settings.get_parameters)
            t.start()

        # Get number in files in logfile
        num_lines_after = sum(1 for line in open('data/LOGFILE'))

        # Has warning has been written to logfile?
        assert_not_equal(num_lines_before, num_lines_after)


if __name__ == '__main__':
    nose.main()
