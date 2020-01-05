cmake_minimum_required(VERSION 2.8.12)
project(test_package)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

find_package(fseam REQUIRED)
find_package(catch2 REQUIRED)

# Create aliasses for Catch2 and FSeam as these are expected by addFSeamTests
set_target_properties(fseam::fseam PROPERTIES IMPORTED_GLOBAL TRUE)
set_target_properties(catch2::catch2 PROPERTIES IMPORTED_GLOBAL TRUE)

add_library(FSeam ALIAS fseam::fseam)
add_library(Catch2::Catch2 ALIAS catch2::catch2)

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

target_link_libraries(${PROJECT_NAME} fseam::fseam catch2::catch2)