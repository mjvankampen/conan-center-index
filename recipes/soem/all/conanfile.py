import glob
import os
import shutil
from conans import ConanFile, CMake, tools

required_conan_version = ">=1.28.0"

class SoemConan(ConanFile):
    name = "soem"
    license = "GPLv2"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://openethercatsociety.github.io"
    topics = ("ethercat", "fieldbus", "master", "rpc", "json-parser")
    description = "Simple Open EtherCAT Master"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = {"shared": False,
                       "fPIC": True}
    exports_sources = ["CMakeLists.txt", "patches/**"]
    generators = "cmake"

    _cmake = None
    _header_only = False

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def requirements(self):
        if self.settings.os == "Windows":
            self.requires("winpcap/4.1.3@bincrafters/stable")

    def _patch_sources(self):
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)

    def configure(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

        if self.options.shared:
            del self.options.fPIC
            
    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure()
        return self._cmake

    def build(self):
        self._patch_sources()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
        tools.rmdir(os.path.join(self.package_folder, "bin"))

    def package_info(self):
        self.cpp_info.filenames["cmake_find_package"] = "soem"
        self.cpp_info.filenames["cmake_find_package_multi"] = "soem"
        self.cpp_info.names["cmake_find_package"] = "soem"
        self.cpp_info.names["cmake_find_package_multi"] = "soem"
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = [os.path.join("include", "soem")]
        if self.settings.os == "Windows":
            self.cpp_info.system_libs = ["Packet", "Ws2_32", "Winmm"]
        elif self.settings.os == "Macos":
            self.cpp_info.system_libs = ["pthread", "pcap"]
        else:
            self.cpp_info.system_libs = ["pthread ", "rt"]
