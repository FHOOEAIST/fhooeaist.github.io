# Unity

The following readme describes the coding conventions especially for Unity. Please read the [C#](/chsarp.md) readme before.

## Project Structure

Unity projects must use the project structure of the Unit Archetype, i.e.:

```
...
  Assets/
    AIST/
      ProjectName/
        Prefabs/
        Scenes/
        Scripts/
      ProjectName.Tests/
        Scripts/
```

Additional folders with AIST code may be added inside of the `AIST` directory to better separate different parts of the project. Every such folder has to follow the same type-wise partitioning of files that is seen above (with folders for `Scripts`, `Prefabs`, etc.). Of course, if a folder would be empty (e.g. because there aren't any scenes in the corresponding part of the project), it doesn't have to be created. In a similar vein, if other types of files are used, additional folders may be added for them.

Files from external libraries which are imported through the Unity Asset Store or through *.unitypackage files must not be moved to different directories after being imported. This is to ensure that imported packages which make assumptions about the directories in which they are contained don't break due to being moved away from their original locations.

Files from external libraries which are imported through other means than the Unity Asset Store or *.unitypackage files have to be added to new directories inside of the `Assets` directory, creating one directory per library.

## Assembly Definition Files

[Assembly Definition Files](https://docs.unity3d.com/Manual/ScriptCompilationAssemblyDefinitionFiles.html) have to be used to define custom assemblies for the project, both for AIST code as well as for external libraries that don't define any assemblies on their own. Unity's default assemblies (Assembly-CSharp, Assembly-CSharp-Editor, ...) must not contain any code, because code inside of custom assemblies cannot access code in the default assemblies.

Beware that Unity distinguishes 3 different types of assemblies ("normal" assemblies, editor assemblies and test assemblies). If these are not used correctly, the Unity project will not build and/or will not recognize the unit tests in the project.

## Coding Convention

Having business-logic in MonoBehaviours should be avoided whenever possible. Instead, all logic should be contained in "normal" (i.e. non-MonoBehaviour) C# classes and accessed by MonoBehaviours through calls to objects of these classes. This makes the code much easier to reuse and test, because the logic can be accessed without having to first create a GameObject to which the corresponding MonoBehaviour can be added.

Fields must not be made public just to make them show up in the Unity Editor. Instead, [SerializeField] attributes must be used if private fields should be made visible in the Unity Editor => `[SerializeField] private <Type> <Name>;`.

## Tools to preserve conventions

To make it easier to write code that follows the defined conventions, the Unity Archetype employs the following "tools":

[StyleCop Analyzers](https://github.com/DotNetAnalyzers/StyleCopAnalyzers), which are added to the Unity Archetype through NuGet, are used to highlight code style violations right inside of the IDE. A full list of StyleCop's rules can be found in the [StyleCop Analyzers Documentation](https://github.com/DotNetAnalyzers/StyleCopAnalyzers/blob/master/DOCUMENTATION.md).

To ensure that code is correctly formatted (i.e. in conformance with StyleCop's rules) when first writing it, an [EditorConfig](https://editorconfig.org/) file is used to set the code style settings for the project. The file is part of the Unity Archetype and should work out-of-the-box for all IDEs / editors that support EditorConfig files (VisualStudio, VS Code, Rider, ...).

## Unit Tests

Unit tests must be added in test assemblies inside of the Unity project. Instructions on how to create test assemblies can be found in the [Unity Test Runner](https://docs.unity3d.com/Manual/testing-editortestsrunner.html) documentation.

For each non-test assembly "[AssemblyName]", one test assembly "[AssemblyName].Tests" must created. Directories for test assemblies must be added to the same parent directory ("AIST") as directories for non-test assemblies.

For example, given two assemblies "ProjectName.Foo" and "ProjectName.Bar", the project structure should be the following:
```
...
  Assets/
    AIST/
      ProjectName.Foo/
        ...
      ProjectName.Foo.Tests/
        ...
      ProjectName.Bar/
        ...
      ProjectName.Bar.Tests/
        ...
```

When creating test classes / methods, the same (naming) conventions as for C# test classes / methods apply.

Since the Unity Test Runner uses [NUnit](https://nunit.org/) in the background, all the usual NUnit attributes ([SetUp], [Test], ...) are available, plus some additional [Unity-specific functionalities](https://docs.unity3d.com/Manual/PlaymodeTestFramework.html) which you probably won't need. Note that Unity distinguishes between two different types of tests: Edit mode tests and Play mode tests. What you want to use are (usually) Edit mode tests.

To run your tests, use the [Unity Test Runner](https://docs.unity3d.com/Manual/testing-editortestsrunner.html) or an IDE that supports execution of Unity unit tests.

VisualStudio **CANNOT** run Unity unit tests.
JetBrain's Rider CAN run Unity unit tests (through a built-in integration with the Unity Test Runner).

The Unity Test Runner DOES NOT report any Code Coverage. Don't try to get it to work, it'll just make you sad. :cry:
