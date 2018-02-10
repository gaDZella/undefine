![Build status](https://api.travis-ci.org/gaDZella/undefine.svg?branch=master)
[![codecov.io](https://codecov.io/github/gaDZella/undefine/coverage.svg?branch=master)](https://codecov.io/github/gaDZella/undefine)
[![Maintainability](https://api.codeclimate.com/v1/badges/276111ca7e859d7af472/maintainability)](https://codeclimate.com/github/gaDZella/undefine/maintainability)


# undefine - C# Preprocessor tool

This is analog of standard C Preprocessor tools: [unifdef](http://manpages.ubuntu.com/manpages/xenial/man1/unifdef.1.html), [coan](http://coan2.sourceforge.net/) ported for C# syntax specifics.
All of standard C tools are not completely compatible with C# code syntax.

### How it works
This tool parses provided C# code file with a view to build file C# preprocessor internal syntax model.
Further the conditional directives in the model are analyzed and the model is modified based on provided conditional symbol values.
The resulting condition is simplified and the overall model is simplified too.
Take a look at this in action:

Input Foo.cs file:
```
...
#if A && Z
    #if X
        return 1;
    #elif Y && Z
        return 2;
    #else
        return -1;
    #endif
#endif
...
```

Say, the user wants to remove A and Y symbols defining it values as:
 ```
 A = True
 Y = False
 ```

Output Foo.cs file:
```
...
#if Z
    #if X
        return 1;
    #else
        return -1;
    #endif
#endif
...
```

This example looks a bit synthetic but it demonstrates directive condition and structural modification in detail.

### Usage

The tool has 2 working modes: `check` and `apply`

In `check` mode it silently makes all work in memory and shows the resulting message.
In `apply` mode it makes the same work but overrides the source files.

Use `undefine --help` command to show tool man page:

```
undefine [command] [-d symbol] [-u symbol] [path]
```

Command arguments -d and -u provides target symbol values:

* `-d` defines the symbol (True value)
* `-u` undefines the symbol (False value)

For the previous example the command looks in a following manner:

```
undefine apply -d A -u Y Foo.cs
```

The `path` argument can also mean the folder path.


