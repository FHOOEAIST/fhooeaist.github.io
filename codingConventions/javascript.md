# JavaScript

The following readme describes the coding conventions especially for JavaScript.

## Naming

* Always use lower case filenames!
* Classes should have getters and setters for any field
   * getFIELDNAME() -> if not bool
   * isFIELDNAME() -> if bool
   * setFIELDNAME(fieldname)
* We don't use namespaces

Good examples of JS Naming can be found [here](http://www.w3schools.com/js/js_conventions.asp).

## Unit Tests

We use [Jasmine](http://jasmine.github.io/) for JS Unittests because it has a maven-plugin that allows us to use CI on HTML/JS projects!

* Unittests are to be included in a separate folder called "test".
* The Naming convention for unit test classes is [Prefix] ClassName "Test".
* Naming convention for unit tests is "test" [MethodName] [CaseDescription].

## JavaScript and Maven

TODO