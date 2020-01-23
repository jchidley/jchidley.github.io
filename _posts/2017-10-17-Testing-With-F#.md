---
date: "2017-10-17"
title: "Testing With F#"
---

# Testing with F\#

**TL;DR** I now use [xUnit](https://xunit.github.io/) and [FsCheck](https://fscheck.github.io/FsCheck/) which I run through Visual Studio's Test Explorer.  Setting-up and using this has been surprisingly straight-forward and a *massive* leap forward for my programming.

## Introduction

I have been writing tests for a long time but these have been ad-hoc in-line additions to my programs.  Like adding `printfn "This is the current value of variable f"` statements.  This  has hurt the readability and thus maintainability of my programs.  There was no clear distinction between tests and working code.  

I knew that I needed something more as I firmly believe in testing.  From my research a 'proper' system seemed difficult.

I have been attracted to property testing since reading [Scott Wlaschin's excellent blog](http://fsharpforfunandprofit.com/posts/property-based-testing/) and watching [Kit Eason's illuminating web cast](https://skillsmatter.com/skillscasts/9726-a-gazillion-ways-to-test-with-f-sharp).  

## Picking FsCheck and XUnit

Earlier this week, I took the plunge and invested time into learning [FsCheck](https://fscheck.github.io/FsCheck/) and, by extension, [xUnit](https://xunit.github.io/) and [nUnit](http://nunit.org/). 

[NCrunch](http://www.ncrunch.net/) is really attractive but £125.10 is a lot for a hobbyist like me but must be peanuts for a professional so I haven't decided.  I think I need to do more testing of testing before I can decide if the time saved will be worth it.

FsCheck, which is based on Haskell's [QuickCheck](https://hackage.haskell.org/package/QuickCheck), is attractive to me as thinking up properties and testing with random data strikes me as a really good way to fix bugs and think deeply about the production code, leading to refactoring.  However, there are times when I just want to test a specific known cases and for that a unit testing framework is necessary.  

I looked at NUnit and xUnit and both seem excellent.  Either would do as they're both well supported, work in similar ways and are extensively used.  I chose xUnit because if the slightly stronger support for FsCheck, its cleaner design and implementation and the fact it's newer.

xUnit has a console runner - which I am sure I will use - but I like IDEs so I have gone for the Visual Studio integration.

## Learning How to Test Properly
I just followed the Kit's and Scott's guidance, the specific instructions on the products' web sites and spent some time trying it out.  There were lot of extra web sites that I found useful: see the links below.  

In all I spent several days on it.  Well worth the time as now I have a more effective testing system and my tests are clearly marked in the source code.

## Useful Links
* [FsCheck](https://fscheck.github.io/FsCheck/)
* [xUnit](https://xunit.github.io/) 
* [http://fsharpforfunandprofit.com/posts/property-based-testing/](http://fsharpforfunandprofit.com/posts/property-based-testing/) Scott's blog about property testing.  Look at [this entry](https://fsharpforfunandprofit.com/posts/low-risk-ways-to-use-fsharp-at-work-3/) too 
* [https://skillsmatter.com/skillscasts/9726-a-gazillion-ways-to-test-with-f-sharp](https://skillsmatter.com/skillscasts/9726-a-gazillion-ways-to-test-with-f-sharp) Kit's webcast about testing in F#
* [http://blog.ploeh.dk/tags/#F%23-ref](http://blog.ploeh.dk/tags/#F%23-ref) There's an FsCheck section in these tags
* [http://blog.mavnn.co.uk/fscheck-breaking-your-code-in-new-and-exciting-ways/](http://blog.mavnn.co.uk/fscheck-breaking-your-code-in-new-and-exciting-ways/) 
* [http://www.navision-blog.de/blog/2016/03/21/property-based-testing-in-the-real-world/](http://www.navision-blog.de/blog/2016/03/21/property-based-testing-in-the-real-world/) 
* [http://jackfoxy.com/gaining-fscheck-fluency-through-transparency/](http://jackfoxy.com/gaining-fscheck-fluency-through-transparency/) 
* [https://stackoverflow.com/questions/38839721/how-do-i-implement-multiple-argument-generation-using-fscheck/38841255#38841255](https://stackoverflow.com/questions/38839721/how-do-i-implement-multiple-argument-generation-using-fscheck/38841255#38841255) stackoverflow has useful stuff
* [https://fscheck.github.io/FsCheck/LearningResources.html](https://fscheck.github.io/FsCheck/LearningResources.html) 

## More Links
* [http://www.ncrunch.net/](http://www.ncrunch.net/) Very interesting Visual Studio integration, potentially high productivity gains.
* [https://github.com/haf/expecto](https://github.com/haf/expecto) A fully F#'d testing framework
* [https://github.com/hedgehogqa/fsharp-hedgehog](https://github.com/hedgehogqa/fsharp-hedgehog) Another F# implementation of QuickCheck.
* [http://smallcheck.codeplex.com/](http://smallcheck.codeplex.com/) Exhaustive small scale testing.

## QuickCheck Links
There's a lot of information about QuickCheck.  QuickCheck has been around for a long time and FsCheck is based on it.  All of this is useful background
* [https://begriffs.com/posts/2017-01-14-design-use-quickcheck.html](https://begriffs.com/posts/2017-01-14-design-use-quickcheck.html) QuickCheck information
* [https://www.stackbuilders.com/news/a-quickcheck-tutorial-generators](https://www.stackbuilders.com/news/a-quickcheck-tutorial-generators) Generators are the core of property testing
* [https://www.stuartgunter.org/posts/intro-to-quickcheck/](https://www.stuartgunter.org/posts/intro-to-quickcheck/) QuickCheck
