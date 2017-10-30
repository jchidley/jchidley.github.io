---
date: "2017-10-30"
title: "What's the Point of a F# Computational Expression AKA F# Monad"
---

# What's the Point of a F# Computational Expression AKA F# Monad
**TL;DR** [FsCheck](https://fscheck.github.io/FsCheck/) documentation does cover what you need to know and is probably enough for experienced people. For those that need more detail, like me, read below.

## Introduction

I really like [FsCheck](https://fscheck.github.io/FsCheck/)'s property based testing, which is based on Haskell's [QuickCheck](https://hackage.haskell.org/package/QuickCheck), with its randomised inputs. But I have found it tricky to  understand and use it effectively.  I wrote these notes to help other novice F\# and FsCheck users to get started.

## Basic principles
In essence, the whole idea around FsCheck, and property based testing is this: find properties of your program that should always be true (or false) for all of its valid, or invalid respectively, data.  The canonical example is associativity for addition ```(a + b) + c = a + (b + c)``` i.e. the brackets make no difference.  So the process of building the tests falls into 2 parts:

1. Build the test, including the test execution's framework, for the property under question.
2. Generate the right kind of data. 


## Building and Running Tests
The [tutorial](https://fscheck.github.io/FsCheck/QuickStart.html) is very good for this but I will stress a few things.

Here the property under test is that a list, when reversed and reversed again should be identical to the original list.  Here's a function that does just that:

```
let revRevIsOrig (xs:list<int>) = List.rev(List.rev xs) = xs
```

To make this really explicit, I'm going to turn it into a AAA (Arrange, Act, Assert) pattern.  *Arrange* means initializing things, in this case getting the data.  *Act* means running the function (program) with the data.  *Assert* means verifying that the expected result matches the actual result. 

```fsharp
// Arrange - partial, note the restriction of the list to <int>
let revRevIsOrig (xs:list<int>) = 
    // Act
    let actual = List.rev(List.rev xs)
    let expected = xs
    // Assert
    actual = expected // should be true
```

The other part of this pattern is to run the function with the data:

```fsharp
\\ The other part of Arrange, and the test execution.
Check.Quick revRevIsOrig
```

Which gives this result:
```
Ok, passed 100 tests.
```

The magical or hidden bit here is ```Check.Quick``` has inspected the function, in particular looked at the type of the parameter ```xs:list<int>``` and automatically generated 100 random lists of integers and run the function 100 times, inputting the unique data - one of the 100 integer lists - each time.  Clearly all 100 versions of this must have ended with true (i.e. expected  = actual).  More on the data generation later.

You can use the above arrangement in your programs and just inspect the results on the output.  No test runner required.

To turn this into a form suitable for the various testing frameworks, e.g. xUnit, is relatively easy.  You need to enclose the entire test above in another let binding that takes no arguments and change ``Check.Quick revRevIsOrig`` line to ``Check.QuickThrowOnFailure revRevIsOrig``, which throws an exception on failure which both nUnit and xUnit treat as a test fail.

```fsharp
[<Fact>]
let ``Reversing a reversed list is identical to the original list``() = 
    let revRevIsOrig (xs:list<int>) = 
        let actual = List.rev(List.rev xs)
        let expected = xs
        actual = expected
    Check.QuickThrowOnFailure revRevIsOrig
```

Use one of the test suite's runners.  I like to use the one that integrates with Visual Studio's test explorer.

FsCheck has extended xUnit.  We can can decorate the original form of the test with the ```[<Property>]```.  The ```Check.Quick revRevIsOrig``` is redundant but you might want to leave it in if you're going to be running the tests from a command line runner too.

```fsharp
[<Property>]
let revRevIsOrig (xs:list<int>) = 
    let actual = List.rev(List.rev xs)
    let expected = xs
    actual = expected
```

Test results appear in the output window, as expected.

```
[28/10/17 17:47:09 Informational] ------ Run test started ------
[28/10/17 17:47:10 Informational] [xUnit.net 00:00:00.3866276] Received 1 results from 1 requests
[28/10/17 17:47:10 Informational] [xUnit.net 00:00:00.3874000]   Starting:    Experiments
[28/10/17 17:47:10 Informational] [xUnit.net 00:00:00.7217074]   Finished:    Experiments
[28/10/17 17:47:10 Informational] ========== Run test finished: 1 run (0:00:00.7749113) ==========
```

So we have seen 3 ways to run the test:

1. Inside the code printing to the standard output using ```Quick.Check```
2. Using the standard method of your testing framework and including  ```Check.QuickThrowOnFailure``` as part of the test definition.
3. Using the FsUnit's extension of the framework to simplyfy 2. above, if the extension exists (i.e. xUnit and FsUnit)

## Standard Types Aren't Enough

I've been learning [FParsec](http://www.quanttec.com/fparsec/) and using FsCheck at the same time to investigate some properties.  I wanted to check that that FParsec parses just like the standard parsing the .net framework.  Silly me.

Firstly, here's some helpers for FParsec.

```fsharp
open FParsec

exception ParseError of string
let parse parser input = 
    match run parser input with 
        | Success (result, _, _) -> result
        | Failure (error, _, _) -> raise (ParseError error) 
```

And I wrote this little function and ran it with quick check.

```fsharp
let ``FParsec correctly parses floats`` (x:float) = 
    let str = x.ToString()
    let expected = System.Double.Parse(str)
    let actual = parse pfloat str
    expected = actual

Check.Quick ``FParsec correctly parses floats``
```
This produces a successful result like this:

```
Falsifiable, after 8 tests (0 shrinks) (StdGen (1042719141,296369266)):
Original:
-infinity
with exception:
FSI_0005+ParseError: Exception of type 'FSI_0005+ParseError' was thrown.
   at FSI_0005.parse[a](FSharpFunc`2 parser, String input) in C:\Users\jackc\Documents\Git\fsharpExperiments\Experiments\FsCheck.fs:line 31
   at FSI_0006.FParsec correctly parses floats(Double x) in C:\Users\jackc\Documents\Git\fsharpExperiments\Experiments\FsCheck.fs:line 169
   at FSI_0006.it@171-1.Invoke(Double x) in C:\Users\jackc\Documents\Git\fsharpExperiments\Experiments\FsCheck.fs:line 171
   at FsCheck.Testable.evaluate[a,b](FSharpFunc`2 body, a a) in C:\Users\Kurt\Projects\FsCheck\FsCheck\src\FsCheck\Testable.fs:line 151
val ( FParsec correctly parses floats ) : x:float -> bool
val it : unit = ()
```


Oh.

Well then.

First things first.  Let me turn this into an xUnit *Fact*:

```fsharp
[<Fact>]
let ``FParsec correctly parses floats - Fact``() =  
    let floatParser (x:float) = 
        let str = x.ToString()
        let expected = System.Double.Parse(str)
        let actual = parse pfloat str
        expected = actual
    Check.QuickThrowOnFailure floatParser
```
and turn that into an xUnit *Property*:

```fsharp
[<Property>]
let ``FParsec correctly parses floats - Property``(x:float) =  
    let str = x.ToString()
    let expected = System.Double.Parse(str)
    let actual = parse pfloat str
    expected = actual
```
So now we have 3 versions of the same test:
1. \``FParsec correctly parses floats`` (x:float)
2. \``FParsec correctly parses floats - Fact``()
3. \``FParsec correctly parses floats - Property``(x:float)

All the test fail in the same way as pfloat is unable to parse ``infinity`` (also it can't handle ``-infinity`` or ``nan``).  This is surprising to me.  This result alone will affect how I use ``pfloat`` in the future.  I would not have found this out using my previous testing techniques.

Clearly I need to handle the above facts in any code I write.  But I also want to make sure that pfloat **does** handle all of the other kinds of floats.

So the type ``float`` just isn't going to work for these tests.  I need a closely related type to work with, a custom one that doesn't produce infinities or things which aren't numbers.  This is where custom types and generators come in handy.  That I'll talk about in my next post.



## Useful Links
* [FsCheck](https://fscheck.github.io/FsCheck/)
* [http://blog.ploeh.dk/tags/#FsCheck-ref](http://blog.ploeh.dk/tags/#FsCheck-ref) 
* [http://blog.mavnn.co.uk/fscheck-breaking-your-code-in-new-and-exciting-ways/](http://blog.mavnn.co.uk/fscheck-breaking-your-code-in-new-and-exciting-ways/) 
* [http://www.navision-blog.de/blog/2016/03/21/property-based-testing-in-the-real-world/](http://www.navision-blog.de/blog/2016/03/21/property-based-testing-in-the-real-world/) 
* [http://jackfoxy.com/gaining-fscheck-fluency-through-transparency/](http://jackfoxy.com/gaining-fscheck-fluency-through-transparency/) 

## More Links
* [http://www.ncrunch.net/](http://www.ncrunch.net/) Very interesting Visual Studio integration, potentially high productivity gains.

