from conans import ConanFile, CMake, tools
import os

class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = ["cmake_find_package"]
    requires = "catch2/2.11.0"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if tools.cross_building(self.settings):
            if self.settings.os == "Emscripten":
                exe_name = "test_package.js"
            elif self.settings.os == "Windows":
                exe_name = "test_package.exe"
            else:
                exe_name = "test_package"
            assert(os.path.exists(os.path.join("bin", exe_name)))
        else:
            self.run(os.path.join("bin", "test_package"), run_environment=True)
