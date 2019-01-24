from   conans       import ConanFile, CMake, tools
from   conans.tools import download, unzip, os_info
from   distutils.dir_util import copy_tree
import os
import shutil

class BgfxConan(ConanFile):
    name            = "bgfx"
    version         = "master"
    description     = "Conan package for bgfx."
    url             = "https://github.com/bkaradzic/bgfx"
    license         = "BSD"
    settings        = "arch", "build_type", "compiler", "os"
    generators      = "cmake"
    options         = {"shared": [True, False]}
    default_options = "shared=False"

    def source(self):
        #self.run("git clone git://github.com/bkaradzic/bx.git")
        #self.run("git clone git://github.com/bkaradzic/bimg.git")
        #self.run("git clone git://github.com/bkaradzic/bgfx.git")
        self.run("git clone git@github.com:firefalcom/bgfx.cmake.git")
        self.run("cd bgfx.cmake && git checkout feature/opengl-version")
        copy_tree("bgfx.cmake", ".")
        self.run("git submodule update --init --recursive" )

    def build(self):
        cmake          = CMake(self)
        shared_options = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else "-DBUILD_SHARED_LIBS=OFF"
        fixed_options  = "-DBGFX_BUILD_EXAMPLES=OFF"
        tool_options   = "-DBGFX_BUILD_TOOLS=OFF" if self.settings.os == "Emscripten" else ""
        opengl_version = "-DBGFX_OPENGL_VERSION=33"
        self.run("cmake %s %s %s %s %s" % (cmake.command_line, shared_options, fixed_options, tool_options, opengl_version))
        self.run("cmake --build . %s" % cmake.build_config)

    def collect_headers(self, include_folder):
        self.copy("*.h"  , dst="include", src=include_folder)
        self.copy("*.hpp", dst="include", src=include_folder)
        self.copy("*.inl", dst="include", src=include_folder)

    def package(self):
        self.collect_headers("bgfx/include")
        self.collect_headers("bimg/include")
        self.collect_headers("bx/include"  )
        self.copy("*.a"  , dst="lib", keep_path=False)
        self.copy("*.so" , dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["bgfxd", "bimgd", "bxd"] if self.settings.build_type == "Debug" else ["bgfx", "bimg", "bx"]
        if self.settings.os == "Macos":
            self.cpp_info.exelinkflags = ["-framework Cocoa", "-framework QuartzCore", "-framework OpenGL", "-weak_framework Metal"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["GL", "X11"])
