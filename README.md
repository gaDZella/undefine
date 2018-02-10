[![Build Status](https://travis-ci.org/gaDZella/undefine.svg?branch=master)](https://travis-ci.org/gaDZella/undefine)
[![codecov.io](https://codecov.io/github/gaDZella/undefine/coverage.svg?branch=master)](https://codecov.io/github/gaDZella/undefine)
[![Maintainability](https://api.codeclimate.com/v1/badges/276111ca7e859d7af472/maintainability)](https://codeclimate.com/github/gaDZella/undefine/maintainability)


# undefine - C# Preprocessor tool

This is an analog of the standard C Preprocessor tools: [unifdef](http://manpages.ubuntu.com/manpages/xenial/man1/unifdef.1.html), [coan](http://coan2.sourceforge.net/) ported for C# syntax specifics.
Unlike the standard C tools **undefine** is fully compatible with the C# code syntax.

### How it works
This tool parses C# code files in order to build an internal preprocessor directives model.
Then the model's conditional directives are analyzed and the model is modified based on provided conditional symbol values.
The resulting condition is simplified and the overall model is simplified as well.
See how it works in action:

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

Say, the user wants to remove the A and Y symbols defining their values as:
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

This example looks a bit synthetic but it demonstrates a directive condition and a structural modification in detail.

### Usage

The tool has 2 working modes: `check` and `apply`

In `check` mode it silently does all the work in memory and shows the resulting message.
In `apply` mode it does the same but overrides source files.

Use `undefine --help` command to show the tool man page:

```
undefine [command] [-d symbol] [-u symbol] [path]
```

Command arguments -d and -u provide target symbol values:

* `-d` defines the symbol (True value)
* `-u` undefines the symbol (False value)

For the previous example the command looks as follows:

```
undefine apply -d A -u Y Foo.cs
```

The `path` argument can also mean the folder path.


