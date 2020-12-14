import os
from conans import ConanFile, CMake, tools

class PpconsulConan(ConanFile):
    name = "ppconsul"
    license = "Boost Software License 1.0"
    author = "oliora"
    url = "https://github.com/oliora/ppconsul"
    description = "A C++ client library for Consul. Consul is a distributed tool for discovering and configuring services in your infrastructure."
    topics = ("Consul")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": False,
        "libcurl:shared": True
    }
    generators = "cmake"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("ppconsul-{}".format(self.version), self._source_subfolder)


    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src=self._source_subfolder)
        self.copy("*.h", dst="include", src="build")
        self.copy("*ppconsul.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("LICENSE_1_0.txt", dst="licenses")


    def package_info(self):
        self.cpp_info.libs = ["ppconsul"]
        self.cpp_info.includedirs.append(os.path.join( "include", "include"))

    def requirements(self):
        self.requires("boost/[>1.55]")
        self.requires("libcurl/[>7.00]")