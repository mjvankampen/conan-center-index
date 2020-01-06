cmake_minimum_required(VERSION 2.8.12)
project(test_package)

set (CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_MINSIZEREL ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})

set(CMAKE_VERBOSE_MAKEFILE TRUE)

find_package(FSeam REQUIRED)

add_executable(simpleFreeFunction DependencyToMock.cpp DependencyToMock.hpp main.cpp)

target_include_directories(simpleFreeFunction PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

enable_testing()
addFSeamTests(
        DESTINATION_TARGET ${PROJECT_NAME}
        TST_SRC 
                ${CMAKE_CURRENT_SOURCE_DIR}/test_package.cpp
        TO_MOCK
                ${CMAKE_CURRENT_SOURCE_DIR}/DependencyToMock.hpp #Give header to mock
		TARGET_AS_SOURCE simpleFreeFunction
		MAIN_FILE main.cpp
)
