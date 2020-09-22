# Java

The following readme describes the coding conventions especially for Java.

## Naming

* Packages must be lowercase.
* Interfaces should be separated from implementations by package name. For Example the interface at.fh.hagenberg.aist.PatientDao should have its implementation in at.fh.hagenberg.aist.impl.PatientDaoJdbcImpl
* Abstract classes should have the prefix "Abstract"
* ALL Java projects have to be in the namespace at.fh.hagenberg.aist.*
* The name of a project has to be identical with the project name and the at.fh.hagenberg.aist namespace (i.e. Project Wire = at.fh.hagenberg.aist.wire.*)
* Different Implementations can be structured hierarchically (i.e at.fh.hagenberg.aist.wire.operators and at.fh.hagenberg.aist.wire.operators.programmable)

## Unit Tests

We use TestNg for Unittests

```xml
<dependency>
  <groupId>org.testng</groupId>
  <artifactId>testng</artifactId>
  <version>6.1.1</version>
  <scope>test</scope>
</dependency>
```

* Unit tests are to be pushed to the src/test/java folder.
* All unit tests are named after the class they are testing with the suffix "Test"
* Unittets must be in the same package as the tested class.
* Integration and benchmark tests should be in the sub packages "it" and "benchmark" respectively.
* All dependencies needed for tests only (see Java and Maven) must be annotated with ``<scope>test</scope>``
* Unittests should work with mvn clean install. Meaning all requirements (starting servers for example) should be handled in pom.xml.

## Java and Maven

* All Java Projects must use maven. A base project which contains a skeleton can be found in the archetype java project (https://aist.fh-hagenberg.at/git/Development/archetype)
* All projects must have the groupId "at.fh.hagenberg.aist.PROJECTNAME"
* Projects are structured in modules. Meaning any project can have child-projects that it builds with the ``<modules>`` tag.
* Child projects must always referece their parent proejct.
* The projects "at.fh.hagenberg.aist.jfuck" and "at.fh.hagenberg.aist.commons" contains source code commonly used in several or all of (the e-Health lab) projects. It and/or its sub-projects may be used as ``<dependency>`` anywhere. It is not to be used as parent for any other project.

**To access the local nexus for our local artifacts the settings xml in the .m2 folder is required. This is described in [Nexus](../DevelopmentNexus.md).**

## IntelliJ Templates

Most of us are using IntelliJ for Java. So, have a look at the following templates. Those are used and tested with IntelliJ Version `2019.1`.

### Class comment template

The following template should be used for classes, interfaces and enums.

To use it go to the "File Menu" -> "Settings" -> "Editor" -> "File and Code Templates".
Search for the already existing class template and replace it with:

```
#if (${PACKAGE_NAME} && ${PACKAGE_NAME} != "")package ${PACKAGE_NAME};#end
#parse("File Header.java")
/**
 * <p>Created by <Your name here> on ${DATE}</p>
 * <p>TODO insert documentation for this class</p>
 *
 * @author <Your name here> <Your mail adress here>
 */
public class ${NAME} {
}
```

If you are working on a Open Source project make sure to not publish your email address. In addition, we also decided to not add the date to the header, but instead
make use of the `@since` javadoc tag. For this, an adapted version of the class comment template exists:

```
#if (${PACKAGE_NAME} && ${PACKAGE_NAME} != "")package ${PACKAGE_NAME};#end
#parse("File Header.java")
/**
 * <p>TODO insert documentation for this class</p>
 *
 * @author <Your name here> <Your mail adress here>
 * @since x.y
 */
public class ${NAME} {
}
```

Make your adaptions (add your name and email address) and do the same for the interface and the enum template. For those you also have to change the keyword after `public` :wink:

### Getter/Setter templates
We are using [Project Lombok](https://projectlombok.org/) for creating boiler plate code like Getter and Setters!

If Lombok is not used (then you are mostly doing something wrong!!!111eleven), you need at least one class with at least one property for creating the following getter/setter templates.
Otherwise the Generate Getter/Setter menu won't show up.

#### Getter template

The following template auto generates a linked Java-Doc comment for the getter.

To add the template go to "Code Menu" -> "Generate" -> "Getter" -> "..." (next to the `Template` dropdown menu) -> "+".
Enter some name for the template and add the following code:

```
#set($paramName = $helper.getParamName($field, $project))
/**
* gets value of field {@link $class.name#$paramName}
*
* @return value of field $paramName
* @see $class.name#$paramName
*/
#if($field.modifierStatic)
static ##
#end
$field.type ##
#set($name = $StringUtil.capitalizeWithJavaBeanConvention($StringUtil.sanitizeJavaIdentifier($helper.getPropertyName($field, $project))))
#if ($field.boolean && $field.primitive)
is##
#else
get##
#end
${name}() {
return $field.name;
}
```

Don't forget to select the new template when generating a getter :wink:

#### Setter template

The following template auto generates a linked Java-Doc comment for the setter.

To add the template go to "Code Menu" -> "Generate" -> "Setter" -> "..." (next to the `Template` dropdown menu) -> "+".
Enter some name for the template and add the following code:

```
#set($paramName = $helper.getParamName($field, $project))
/**
* sets value of field {@link $class.name#$paramName}
*
* @param $paramName value of field $paramName
* @see $class.name#$paramName
*/
#if($field.modifierStatic)
static ##
#end
void set$StringUtil.capitalizeWithJavaBeanConvention($StringUtil.sanitizeJavaIdentifier($helper.getPropertyName($field, $project)))($field.type $paramName) {
#if ($field.name == $paramName)
    #if (!$field.modifierStatic)
    this.##
    #else
        $classname.##
    #end
#end
$field.name = $paramName;
}
```

Don't forget to select the new template when generating a setter :wink:

#### Builder / Fluent Setter template

The following template is an alternative template for the setter which should be used if the object for which the setter is called should be returned for some fluent usage. The template is created 1:1 similar as the setter template or you can replace the existing `Builder` template with the following, adapted version.

```
#set($paramName = $helper.getParamName($field, $project))
/**
* sets value of field {@link $class.name#$paramName}
*
* @param $paramName value of field $paramName
* @see $class.name#$paramName
* @return this
*/
#if($field.modifierStatic)
static ##
#end
$class.name set$StringUtil.capitalizeWithJavaBeanConvention($StringUtil.sanitizeJavaIdentifier($helper.getPropertyName($field, $project)))($field.type $paramName) {
#if ($field.name == $paramName)
    #if (!$field.modifierStatic)
    this.##
    #else
        $classname.##
    #end
#end
$field.name = $paramName;
return this;
}
```

Don't forget to select the new template when generating a fluent setter :wink:

### TestNG template
We are using TestNG for testing in Java. IntelliJ allows us to auto generate test class and method stubs with `"Code" --> "Generate..." (Alt + Insert) --> "Tests..."` (in the according implementation class).

The following IntelliJ template adds automatically the class doc with a link to the implementation class
To add the test class template go to: `Settings --> Editor --> File and Code Templates --> Code menu --> TestNG Test class`

```
import static org.testng.Assert.*;
#parse("File Header.java")
/**
 * <p>Created by <your name> on ${DATE}</p>
 * <p>Test class for {@link ${PACKAGE_NAME}.${NAME.replace("Test", "")}}</p>
 *
 * @author <your name> <your mail address>
 */
public class ${NAME} {
    ${BODY}
}
```

With the following IntelliJ templates it also creates the given/when/then-pattern comments.
To add the template go to: `Settings --> Editor --> File and Code Templates --> Code menu --> TestNG Test method`
and change it to:

```
@org.testng.annotations.Test
public void test${NAME}() {
  // given
  
  // when
  ${BODY}
  
  // then
}
```

