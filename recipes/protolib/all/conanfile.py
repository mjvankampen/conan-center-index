import os
from conans import ConanFile, tools, CMake


class ProtolibConan(ConanFile):
    name = "protolib"
    homepage = "https://github.com/USNavalResearchLaboratory/protolib"
    description = "Protolib is a library focussed on providing a platform-independent network interface"
    topics = ("conan", "cross-platform", "protocol library", "socket", "networking")
    url = "https://github.com/conan-io/conan-center-index"
    license = "Custom"
    exports_sources = "CMakeLists.txt"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    generators = "cmake", "cmake_find_package"

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("protolib-{}".format("cmake"), self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE*", src=self._source_subfolder, dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "protolib"
        self.cpp_info.names["cmake_find_package_multi"] = "protolib"
        self.cpp_info.libs = ["protolib"]
        if self.settings.os == "Windows":
            self.cpp_info.system_libs = ["ws2_32", "iphlpapi", "user32", "gdi32", "Advapi32", "ntdll"]
        elif self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread", "rt", "dl"]
        else:
            self.cpp_info.system_libs = ["pthread"]
