#define CATCH_CONFIG_MAIN

#include <catch2/catch.hpp>
#include <FSeamMockData.hpp>
#include "DependencyToMock.hpp"

TEST_CASE("Test FreeFunction") {
    auto mockFreeFunc = FSeam::getFreeFunc();

    SECTION("simple call") {
        REQUIRE(true == freeFunctionSimple());
        CHECK(mockFreeFunc->verify(FSeam::FreeFunction::freeFunctionSimple::NAME, 1));
        freeFunctionSimple();
        freeFunctionSimple();
        freeFunctionSimple();
        freeFunctionSimple();
        CHECK(mockFreeFunc->verify(FSeam::FreeFunction::freeFunctionSimple::NAME, 5));

    } // End section : simple call

    SECTION("Test free function method dupe") {
        bool hasBeenCalled = false;
        mockFreeFunc->dupeMethod(FSeam::FreeFunction::freeFunctionSimple::NAME, [&hasBeenCalled](void *data) {
            hasBeenCalled = true;
        });

        freeFunctionSimple();
        REQUIRE(hasBeenCalled);
        REQUIRE(mockFreeFunc->verify(FSeam::FreeFunction::freeFunctionSimple::NAME, 1));

    } // End section : Test static method dupe

    SECTION("Dupe return value") {
        mockFreeFunc->dupeReturn<FSeam::FreeFunction::freeFunctionSimple>(false);
        REQUIRE(false == freeFunctionSimple());
        REQUIRE(mockFreeFunc->verify(FSeam::FreeFunction::freeFunctionSimple::NAME, 1));

    } // End section : Dupe return value
	
	SECTION("Dupe return value true") {
        mockFreeFunc->dupeReturn<FSeam::FreeFunction::freeFunctionSimple>(true);
        REQUIRE(true == freeFunctionSimple());
        REQUIRE(mockFreeFunc->verify(FSeam::FreeFunction::freeFunctionSimple::NAME, 1));

    } // End section : Dupe return value

    FSeam::MockVerifier::cleanUp();
} // End TestCase : Test FreeFunction