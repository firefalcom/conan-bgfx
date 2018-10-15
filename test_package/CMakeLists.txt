cmake_minimum_required(VERSION 2.8)
project(bgfx_test)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

#include_directories(${CMAKE_CURRENT_SOURCE_DIR})

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

conan_basic_setup()
conan_define_targets()

set(CMAKE_CXX_FLAGS "-ObjC++")

add_executable(bgfx_test bgfx_test.cpp)
set_target_properties(bgfx_test PROPERTIES LINK_FLAGS ${CONAN_EXE_LINKER_FLAGS})
message(STATUS "Linker flags")
message(STATUS ${CONAN_EXE_LINKER_FLAGS} )
conan_target_link_libraries(bgfx_test)
target_link_libraries( ${CONAN_EXE_LINKER_FLAGS} )
