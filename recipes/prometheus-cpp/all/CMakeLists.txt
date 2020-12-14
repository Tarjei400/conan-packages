#message("INIT")
#
#cmake_minimum_required(VERSION 2.8.12)
#project(cmake_wrapper)
#
#include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
#conan_basic_setup()
#
## Download automatically, you can also just copy the conan.cmake file
#if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
#    message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
#    file(DOWNLOAD "https://github.com/conan-io/cmake-conan/raw/v0.15/conan.cmake"
#            "${CMAKE_BINARY_DIR}/conan.cmake"
#            TLS_VERIFY ON)
#endif()
#
#include(${CMAKE_BINARY_DIR}/conan.cmake)
#
#conan_cmake_run(REQUIRES
#        civetweb
#        BASIC_SETUP
#        CMAKE_TARGETS
#        OPTIONS
#        BUILD missing
#        GENERATORS cmake_find_package)
#
#set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR} ${CMAKE_MODULE_PATH})
#set(CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR} ${CMAKE_PREFIX_PATH})
#
#message("PATHS ${CMAKE_BINARY_DIR} ${CMAKE_MODULE_PATH} ")
#find_package(civetweb REQUIRED)
#
#if(UNIX AND NOT APPLE)
#    if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
#        if(CMAKE_CXX_COMPILER_VERSION VERSION_LESS 5.0)
#            add_definitions("-DGBM_BO_USE_CURSOR=2")
#        endif()
#    endif()
#endif()
#
#add_subdirectory(source_subfolder)

cmake_minimum_required(VERSION 3.0)

project(cmake_wrapper)
message(STATUS "Conan CMake Wrapper")

if(EXISTS ${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
    include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
    conan_basic_setup()
else()
    message(WARNING "The file conanbuildinfo.cmake doesn't exist, you have to run conan install first")
endif()

include(CMakeListsOriginal.txt)
