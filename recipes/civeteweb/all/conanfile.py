#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os

class civetwebConan(ConanFile):
    name = "civetweb"
    description = "Embedded C/C++ web server"
    topics = ("conan", "civetweb", "webserver")
    url = "https://github.com/civetweb/civetweb"
    homepage = "https://github.com/civetweb/civetweb"
    author = "Zinnion <mauro@zinnion.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "compiler", "build_type", "arch"
    short_paths = True
    generators = "cmake"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    options = {
        "shared"            : [True, False],
        "fPIC"              : [True, False],
        "enable_ssl"        : [True, False],
        "enable_websockets" : [True, False],
        "enable_ipv6"       : [True, False],
        "enable_cxx"        : [True, False]
    }
    default_options = {
        "shared"            : False,
        "fPIC"              : True,
        "enable_ssl"        : True,
        "enable_websockets" : True,
        "enable_ipv6"       : True,
        "enable_cxx"        : True
    }

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def configure(self):
        if not self.options.enable_cxx:
            del self.settings.compiler.libcxx

    def requirements(self):
        if self.options.enable_ssl:
            self.requires("openssl/1.1.1c")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.verbose = True
        cmake.definitions["CIVETWEB_ENABLE_SSL"] = self.options.enable_ssl
        cmake.definitions["CIVETWEB_ENABLE_WEBSOCKETS"] = self.options.enable_websockets
        cmake.definitions["CIVETWEB_ENABLE_IPV6"] = self.options.enable_ipv6
        cmake.definitions["CIVETWEB_ENABLE_CXX"] = self.options.enable_cxx
        cmake.definitions["CIVETWEB_BUILD_TESTING"] = False
        cmake.definitions["CIVETWEB_ENABLE_ASAN"] = False
        cmake.configure(build_dir="build_subfolder")
        return cmake

    def build(self):
        #tools.replace_in_file(file_path="CMakeLists.txt",
        #                      search="project (civetweb)",
        #                      replace="""project (civetweb)
        #                         include(conanbuildinfo.cmake)
        #                         conan_basic_setup()""")
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE.md", dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.filenames["cmake_find_package"] = "civetweb"
        self.cpp_info.filenames["cmake_find_package_multi"] = "civetweb"
        self.cpp_info.names["cmake_find_package"] = "Civetweb"
        self.cpp_info.names["cmake_find_package_multi"] = "Civetweb"

        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["dl", "rt", "pthread"])
            if self.options.enable_cxx:
                self.cpp_info.libs.append("m")
        elif self.settings.os == "Macos":
            self.cpp_info.exelinkflags.append("-framework Cocoa")
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
            self.cpp_info.defines.append("USE_COCOA")
        elif self.settings.os == "Windows":
            self.cpp_info.libs.append("Ws2_32")
        if self.options.enable_websockets:
            self.cpp_info.defines.append("USE_WEBSOCKET")
        if self.options.enable_ipv6:
            self.cpp_info.defines.append("USE_IPV6")
        if not self.options.enable_ssl:
            self.cpp_info.defines.append("NO_SSL")
