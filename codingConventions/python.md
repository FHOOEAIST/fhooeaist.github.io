# Python

The following readme describes the coding conventions especially for Python.

__use Python 3.6+__

### Formatting

* Use 4 spaces for indentation.
* Use Literal String Interpolation `f"Hallo {foo}"` for string formatting.
* Use [black](https://github.com/psf/black) to format code.

### Packages & Modules

* Use `snake_case` names for packages and modules.
* Prefer one-word names for packages and modules.
* Add a `__init__.py` file to all package folders to ensure that they are accessible from other packages.
* Create packages with modules to separate logic and to avoid files with hundreds of lines (=> reusability, maintainability, readability).

### Interfaces & Abstract Classes

* Use abstract classes to map interfaces from other languages.
* Use `abc.ABC` as the parent class of abstract classes, e.g. `class AbstractFoo(abc.ABC)` (don't forget to `import abc`).
* Prefix names of abstract classes with `Abstract`.
* Annotate abstract methods with `@abc.abstractmethod`.

### Classes 

* Use `UpperCamelCase` names for classes.
* Initialize properties/member-variables in the constructor/init function (`def __init__(self):`) like `self.bar = None`.
* Use `self` as the first argument of instance methods.
* Annotate static class methods with `@staticmethod` (keep in mind that static class methods do not have the self variable).
* Document classes with docstrings (see <a href="#user-content-documentation-example">example</a> below).

### Methods & Functions

* Use `snake_case` names for methods & functions.
* Add type hints for parameters and return values of methods and functions, e.g. `def foo(name: str, age: int) -> float:` or `… -> (float, int)`.
* Prefix non-public methods with one underscore, e.g. `_method_name`.
* Prefix very private methods with two underscores, e.g. `__method_name`.
* Document public methods and functions with docstrings (see <a href="#user-content-documentation-example">example</a> below).

### Instance Variables

* Use `snake_case` names for instance variables.
* Prefix non-public instance variables with one underscore, e.g. `_variable_name`.
* Prefix very private instance variables with two underscores, e.g. `__variable_name`.

### Constants

* Use `UPPER_SNAKE_CASE` names for constants.
* Document constants with python comments (see <a href="#user-content-documentation-example">example</a> below).

### Public Variables (e.g.: flask-http-server model instance)

* Use `snake_case` names for public variables.
* Document the variable like a constant and add information where it belongs to.

### Function & Class spacing

* Keep two blank lines between classes and functions and other stuff.
* Keep one blank line between methods inside of classes.

## Unit Tests

We use [unittest](https://docs.python.org/3/library/unittest.html) for unit tests.

* Add unit tests for a module inside of a sub-folder called `tests`.
* Name unit test classes after the classes that they are testing, suffixed with `Test`. For example, the test class for `class Foo` must be named `class FooTest(unittest.TestCase)`.
* Structure unit tests according to the _given_-_when_-_then_ convention.
* Ensure that unit tests work with `python -m unittest`.

Example unit test class:

```python
import unittest


class FooTest(unittest.TestCase):
    def test_bar(self):
        # given
        foo = Foo()
        # when
        res = foo.bar()
        # then
        self.assertEqual(res, True)
```

## PyPi

* Use VirtualEnv with a `requirements.txt` file to declare required packages.
* Declare specific package versions in the `requirements.txt` file, e.g. `numpy==1.17.1`.
* Don't mess with your global package store (#dll_hell).

<a id="documentation"></a>
## Documentation Example

```python
# Set the run environment to development.
PYTHON_ENV = "development"


class Foo:
    """
    The awesome example class.

    :param world: This is where you are.
    """

    def __init__(self, world: str = "world"):
        self.hello = world

    def print(self, name: str) -> str:
        """
        Builds a "Hello world `name`" string and returns it.

        :param name: Some content that should stand behind the world.
        :return: String with the formatted result.
        """
        return f"Hello {self.hello} to {name}"

    @staticmethod
    def bar():
        """
        Returns the perfect result.

        :return: True.
        """
        return True


# Main function (this is executed only if the current py-file is directly called).
# If the py-file is imported to another py-file then the content in the statement is not executed.
if __name__ == "__main__":
    foo = Foo("mars")
```

