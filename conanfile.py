from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class M4Conan(ConanFile):
    name = "m4_installer"
    version = "1.4.18"
    description = "GNU M4 is an implementation of the traditional Unix macro processor"
    topics = ("conan", "m4", "macro", "macro processor")
    url = "https://github.com/bincrafters/conan-m4_installer"
    homepage = "https://www.gnu.org/software/m4/"
    license = "GPL-3.0-only"
    exports = ["LICENSE.md"]
    exports_sources = ["secure_snprintf.patch", "msvc.patch"]
    settings = "os_build", "arch_build", "compiler"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    @property
    def _is_mingw_windows(self):
        return self.settings.os_build == "Windows" and self.settings.compiler == "gcc" and os.name == "nt"

    def build_requirements(self):
        if self._is_mingw_windows:
            self.build_requires("msys2/20190524")

    def source(self):
        source_url = "http://ftp.gnu.org/gnu/m4/m4-%s.tar.bz2" % self.version
        tools.get(source_url, sha256="6640d76b043bc658139c8903e293d5978309bf0f408107146505eca701e67cf6")
        os.rename("m4-" + self.version, self._source_subfolder)
        tools.patch(patch_file="secure_snprintf.patch", base_path=self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            env_build = AutoToolsBuildEnvironment(self, win_bash=self._is_mingw_windows)
            env_build.configure()
            env_build.make()
            env_build.install()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)

    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        m4 = "m4.exe" if self.settings.os_build == "Windows" else "m4"
        self.env_info.M4 = os.path.join(self.package_folder, "bin", m4).replace("\\", "/")
