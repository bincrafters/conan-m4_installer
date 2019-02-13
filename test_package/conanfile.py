#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conans import ConanFile
import os


class TestPackageConan(ConanFile):

    def test(self):
        test_file = os.path.join(self.source_folder, "test_package.m4")
        self.run("m4 --version")
        self.run("m4 -P %s" % test_file)
        self.run("m4 -P %s > out" % test_file)
