# C # #

The following readme describes the coding conventions especially for C#.

Visual Studio Settings can be found [here](https://aist.fh-hagenberg.at/git/Internal/collaborationconventions/blob/master/templates/AIST_VSCode.vssettings)

Generally speaking we do follow the [official Microsoft standard](https://docs.microsoft.com/en-us/dotnet/standard/design-guidelines/), if any definitions below clash with their standard our convention is to be preferred. 

If something is generally off please refer to Johann or Rainer; One of them will provide clarification and update these conventions

## Naming

* Interfaces start with the prefix I (i.e. IItem, IOperator)
* Abstract base classes are not suffixed by Base.
* The name of a C# solution should be the name of the project in the AIST Gitlab (i.e Project Wire = Wire in C#)
* The name of a project of the solution has to be identical with the project name and the name of the component (i.e. Wire.Copper)
* Namespaces always start with AIST
* Sub-namespaces should be used to structure the source files in component (Aist.Copper.Welder.WelderImplementation)
* Data components that correspond to a property should have the same name as the property and are not prefixed by anything (no _, no my, no whatsoever)

## Indentation 

* Classes/Interfaces are PascalCase
* Methods are PascalCase
* private fields are camelCase
* Properties are PascalCase
* public members are PascalCase
* parameters are camelCase
* Delegates and events are PascalCase

Refer to [Microsoft naming convention](https://docs.microsoft.com/en-us/dotnet/standard/design-guidelines/capitalization-conventions) for further details


## Inline Comments
We use the XML notation for comments, refer to [this example](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/xmldoc/how-to-use-the-xml-documentation-features). It also has a tag reference. 

* All Interface/Classes **MUST HAVE** a documentation header. This include
  - a summary
  - any generic typeparameter
  - any _seealso_ specifications for baseclasses, or important subclasses

```csharp
namespace Aist.Dictionary.Core 
{
    /// <summary>
    /// This class decides where to put an item in the Dictionary.
    /// </summary>
    /// <typeparam name="T">The type of the domain class this Service can handle, e.g. Book</typeparam>
    public class DictionaryService<T>
    { }
}
```

* All interface methods **MUST HAVE** a documentation header similar as above, but with further details in xmls such as
  - parameter descritions
  - return types
  - implementation hints, possibly in the remark element
* All public methods should have a similar header to the one specified for the interface methods
  - Frequently used/Logic heavy methods need to be documented in more detail
  - Simpler methods, with readable names(FileReader), are allowed to have brief headers
* We write **READABLE** code. Per default your code design should aim to eliminate the necessity of writing inline comments on certain statements. But if you have some complex calculation or similar **write comments describing what happens**. 


## New Lines and Blocks

As per [Microsoft Coding Guidelines](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/inside-a-program/coding-conventions) **each brace gets a new line**

## Unit Tests


* Unit test framework is xunit. It can be selected when creating the testproject.
* Unittests are to be included in a seperate testproject called project_nameTests. The project is organized in folders corresponding to tested namespacese.
* The Naming convention for unit test classes is [Prefix] ClassName "Test".
* Naming convention for unit tests is "test" [MethodName] [CaseDescription].

### Example

```csharp
using AIST.SimilarityMetrics;
using System;
using Xunit;

namespace AIST.Dictionary.Test
{
    public class TestJaroSimilarety
    {

        [Fact]
        public void EqualStrings()
        {
            //given
            ISimilarityMetric similarityMetric = new JaroSimilarity();

            //when
            double actual = similarityMetric.CalculateSimilarity("Wasser", "Wasser");

            //then
            Assert.Equal(1, actual);
        }
    }
}

```

## Extended Coding Guidelines

If you ever need some distraction from your actual work tasks, https://csharpcodingguidelines.com/ are definitely worth a read. They go beyond the usual naming and formatting rules, listing suggestions for class and member design, mainainability and performance guidelines, error handling, and a few others.

The guidelines are also available in PDF format and in a short Cheatsheet version through the corresponding [GitHub Repository](https://github.com/dennisdoomen/CSharpGuidelines/releases).

In case you want to enforce these suggestions / guidelines more strictly, you can add the provided [Roslyn Analyzers](https://github.com/bkoelman/CSharpGuidelinesAnalyzer) to your project through NuGet. A full list of included rules can be found [here](https://github.com/bkoelman/CSharpGuidelinesAnalyzer/blob/master/docs/Overview.md).
