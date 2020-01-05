from conans import ConanFile, CMake, tools
import os, subprocess, sys

class FseamConan(ConanFile):
    name = "fseam"
    description = "Mocking library using link seams"
    topics = ("mock", "unit test", "link seam")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/FreeYourSoul/FSeam"
    license = "MIT" 
    exports_sources = ["CMakeLists.txt"]
    generators = ["cmake"]

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    
    def system_requirements(self):
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ply'])

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["FSEAM_BUILD_TESTS"] = False
        cmake.configure(build_folder=self._build_subfolder, source_folder=self._source_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.name = "FSeam"
        base_path = os.path.join("share", "cmake", "FSeam")
        self.cpp_info.build_modules = [os.path.join(base_path, "FSeamModule.cmake")]
        self.cpp_info.builddirs.append(os.path.join("bin"), base_path)
        self.cpp_info.includedirs = [os.path.join("share", "include")]