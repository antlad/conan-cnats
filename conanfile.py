from conans import ConanFile, CMake, tools
import os


class CnatsConan(ConanFile):
    name = "cnats"
    version = "1.4.4"
    license = "MIT"
    url = "https://github.com/ebostijancic/conan-cnats"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "tls": [True, False]}
    default_options = "shared=False", "tls=False"
    generators = "cmake"
    exports = "*"

    def source(self):
       self.run("git clone https://github.com/nats-io/cnats.git")
       self.run("cd cnats && git checkout v%s" % self.version)

    def build(self):
        cmake = CMake(self.settings)
        opts = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        opts += " -DNATS_BUILD_WITH_TLS=OFF" if self.options.tls == False else ""
        self.run('cmake cnats %s %s' % (cmake.command_line, opts))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include/cnats", src="cnats/src")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["nats_static"]
