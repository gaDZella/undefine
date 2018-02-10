![Build status](https://api.travis-ci.org/gaDZella/undefine.svg?branch=master)

# undefine - C# Preprocessor refactoring tool

This is small analog of standard C Preprocessor tools: [unifdef](http://manpages.ubuntu.com/manpages/xenial/man1/unifdef.1.html), [coan](http://coan2.sourceforge.net/) optimized for C# syntax.

### How it works
This tool parses provided C# code file with a view to build file C# preprocessor internal syntax model.
Further the conditional directives in the model are analyzed and the model is modified based on provided conditional symbol values.
The resulting condition is simplified and the overall model is simplified too.
Take a look at this in action:

Input file:
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

Say, the user wants remove symbols A and Y and set it:
 ```
 A = True
 Y = False
 ```

The tool output file:
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

This example looks a bit synthetic but it demonstrates the preprocessor directive condition and structural modification.