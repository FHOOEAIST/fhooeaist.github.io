# C++

The following readme describes the coding conventions especially for C++.

Visual Studio Settings can be found [here](../../templates/AIST_VSCode.vssettings)

## Naming

* namespaces start with a lower letter
* all projects have to be under the namespace aist
* each individual project has to have its own namespace with its corresponding name
* new code has to be in header implementations (.hpp)
* otherwise definition and implementation should be seperated (.cpp and .h files)
* Abstract base classes should have the prefix "Base"
* classes have to be preferred over structs, although small structs should be used inside classes
* filenames are _lowerCamelCase.hpp_, class names are UpperCamelCase

## New Lines and Blocks

As per [Microsoft Coding Guidelines](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/inside-a-program/coding-conventions) each brace gets a new line

## Unit Tests

We use [Google Test](https://github.com/google/googletest)

* Unit tests are in a new project on the same level as the main project.
  * MainProject: foo/bar 
  * TestProject: foo/bar\_tests
* All unit tests are named after the class they are testing with the suffix "Test"
* Testing with Macros:
  * EXPECT_xx: can fail but does __not abort__ the current test
  * ASSERT_xx: when failing, it __aborts__ the current test

Before & After test example for the class `FooBar`
```c++
namespace aist {
namespace garden {

class FooBarTest : public ::testing::Test {
public:
    FooBarTest(){}
    ~FooBarTest(){}

    void SetUp() {
        // some setup before each test
    }

    void TearDown(){
        // clean up
    }
private:
    ...
};

TEST_F(FooBarTest, create) {
    aist::foo::Bar b("Hello");

    ASSERT_EQ("Hello", b.getName());
}
}
}
```

## Repo Architecture 
* root has gitignore, and lib and include folders for shared libraries (libraries which are used in multiple subprojects)
* each subproject has its own directory with its own gitignore
* contents of said subproject are the direct solution/.pro with include and lib folders for local project and (obviously) code