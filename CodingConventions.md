# Coding Conventions

The following standards apply to all development platforms. Specific standards can be found in explicitly named readmes and extend/override general ones:

* [Java](./codingConventions/java.md)
* [C#](./codingConventions/csharp.md)
* [Unity](./codingConventions/unity.md)
* [C++](./codingConventions/cpp.md)
* [JavaScript](./codingConventions/javascript.md)
* [Python](./codingConventions/python.md)

## Indentation

4 spaces. No tabs.

## New Lines and Blocks

* Opening Braces ({) are on the same line of the statement which opens the block.
* Closing braces (}) are on a new line after the last statement of the block.

## TODOs

TODO comments are always welcome to keep track for all devs on what people are currently working on/what is to come. But all TODOs should always reference the issue number it will be part of. 

### Bad
```java
// TODO Remove the setter, since id should later be constant.
public void setId(int id) {
  this->id = id;
}
```

One does not know who might be working on that TODO, or if it became redundant.

### Good
```java
// TODO #69 Remove the setter, since id should later be constant.
public void setId(int id) {
  this->id = id;
}
```
In this case the GitLab issue provides context and meta information on the TODO.


Always check if all your TODOs are finished before finishing a issue.

## General Naming

Naming is specific the development language. The following points are to be adhered for Java and C#

* All identifiers are written in CamelCase
  * Do not use "_" in identifiers
  * Do not use Hungarian notation (i.e. iCount for int counter or dFactor for a double factor)
* constants are written in UPPERCASE
  * "_" is allowed in constants instead of CAMEL_CASE
* casing:
  * Namespaces, classes, interfaces, properties and methods start with an uppercase letter.
  * Fields, method parameters and local variables start with a lowercase letter

## Unit Tests

* Generally there should be a unittest for each public method that is not a getter or setter in a class.
  * Non-complex methods do not need a unittest. The decision is at the developers discretion.
  * Complex getters or setters may require unittests.
* Unittests should not depend on each other (sometimes they may have to though).
* One Unittest should only test one specific feature.

Unittests must be structured in given/when/then notation:

```java
@Test
public void sampleUnittest() {
  // given (assignments here)
  PatientDao patientDao = new PatientDaoJdbcImpl();
  PatientId id = new PatientId("123");

  // when (execution here)
  Patient p = patientDao.retrievePatientById(id);

  // then (asserts here and never above, no assignments or executions allowed)
  Assert.assertNotNull(p);
}
```
