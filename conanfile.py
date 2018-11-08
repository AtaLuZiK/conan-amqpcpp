import os

from conans import ConanFile, CMake, tools


class AmqpcppConan(ConanFile):
    name = "amqpcpp"
    version = "3.2.0"
    license = "MIT"
    url = "https://github.com/AtaLuZiK/conan-amqpcpp"
    description = "C++ library for asynchronous non-blocking communication with RabbitMQ"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "with_internal_tcp_module": [True, False],
    }
    default_options = "shared=False", "with_internal_tcp_module=False"
    exports_sources = "amqpcpp-config.cmake"
    generators = "cmake"

    @property
    def zip_folder_name(self):
        return "AMQP-CPP-%s" % self.version

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.shared
            del self.options.with_internal_tcp_module

    def requirements(self):
        if self.settings.os == "Linux" and self.options.with_internal_tcp_module:
            self.requires("OpenSSL/1.1.1@conan/stable")

    def source(self):
        zip_name = "v%s.tar.gz" % self.version
        tools.download("https://github.com/CopernicaMarketingSoftware/AMQP-CPP/archive/%s" % zip_name, zip_name)
        tools.check_md5(zip_name, "f5e8548bebcc076831eaa4c06c271d3d")
        tools.unzip(zip_name)
        os.unlink(zip_name)

        with tools.chdir(self.zip_folder_name):
            tools.replace_in_file("CMakeLists.txt", "project(amqpcpp)", '''project(amqpcpp)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        if self.settings.os != "Windows":
            cmake.definitions["AMQP-CPP_BUILD_SHARED"] = "ON" if self.options.shared else "OFF"
        if self.settings.os == "Linux":
            cmake.definitions["AMQP-CPP_LINUX_TCP"] = "ON" if self.options.with_internal_tcp_module else "OFF"
        cmake.configure(source_folder=self.zip_folder_name)
        cmake.build()

    def package(self):
        exclude_headers = None
        if self.settings.os != "Linux" or not self.options.with_internal_tcp_module:
            exclude_headers = "amqpcpp/linux_tcp/*"
        self.copy("*.h", dst="include", src=os.path.join(self.zip_folder_name, "include"), excludes=exclude_headers)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("amqpcpp-config.cmake", "cmake", ".")

    def package_info(self):
        self.cpp_info.libs = ["amqpcpp"]
