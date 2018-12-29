#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class M4Conan(ConanFile):
    name = "m4_installer"
    version = "1.4.18"
    description = "GNU M4 is an implementation of the traditional Unix macro processor"
    topics = ("conan", "m4", "macro", "macro processor")
    url = "https://github.com/bincrafters/conan-m4_installer"
    homepage = "https://www.gnu.org/software/m4/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "GPL-3.0-only"
    exports = ["LICENSE.md"]
    exports_sources = ["secure_snprintf.patch"]
    settings = "os_build", "arch_build", "compiler"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    @property
    def _is_msvc(self):
        return self.settings.compiler == "Visual Studio"

    @property
    def _is_mingw_windows(self):
        return self.settings.os_build == "Windows" and self.settings.compiler == "gcc" and os.name == "nt"

    def build_requirements(self):
        if self._is_msvc or self._is_mingw_windows:
            self.build_requires("msys2_installer/latest@bincrafters/stable")

    def source(self):
        source_url = "http://ftp.gnu.org/gnu/m4/m4-%s.tar.bz2" % self.version
        tools.get(source_url, sha256="6640d76b043bc658139c8903e293d5978309bf0f408107146505eca701e67cf6")
        os.rename("m4-" + self.version, self._source_subfolder)
        tools.patch(patch_file="secure_snprintf.patch", base_path=self._source_subfolder)

    def build(self):
        if self._is_msvc:
            with tools.vcvars(self.settings):
                self._build_configure()
        else:
            self._build_configure()

    def _build_configure(self):
        with tools.chdir(self._source_subfolder):
            args = []
            if self._is_msvc:
                args.extend(['CC=$PWD/build-aux/compile cl -nologo',
                             'CXX=$PWD/build-aux/compile cl -nologo',
                             'LD=link',
                             'NM=dumpbin -symbols',
                             'STRIP=:',
                             'AR=$PWD/build-aux/ar-lib lib',
                             'RANLIB=:'])
            env_build = AutoToolsBuildEnvironment(self, win_bash=self._is_msvc or self._is_mingw_windows)
            env_build.configure(args=args)
            env_build.make()
            env_build.install()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)

    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        m4 = "m4.exe" if self.settings.os_build == "Windows" else "m4"
        self.env_info.M4 = os.path.join(self.package_folder, "bin", m4)
