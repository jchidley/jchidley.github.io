---
date: "2017-10-23"
title: "Testing and FParsec"
---

# Testing and FParsec

**TL;DR** Follow the [FParsec Tutorial](http://www.quanttec.com/fparsec/tutorial.html).

## Introduction
Parsing, it's one of those computer sciencey things.  I avoided Computer Science at University because I knew that I'd be doing computing for the rest of my life so I wanted to study something else.  It seems silly on the surface but I guess I didn't want to derail things, or be bored, by studying it too.  I think, on reflection, that I would have been bored out of my mind, judging by my reaction to reading CS textbooks or watching CS videos.  I have digressed.

Anyway, I have always been in awe of parsing because that's the first step to writing your own compiler.  Compiling languages is  one foundations of modern computing.  If you can write a compiler, you're a god in my view.

Once again, I've decided to make myself uncomfortable and do something that seems magical to me.  Parsing.

## FParsec

If you're using F\# then [FParsec](http://www.quanttec.com/fparsec/) is the way to go.  Like many other libraries in F\#, this one is based on a Haskell original: [parsec](https://hackage.haskell.org/package/parsec).  That means that there's lots of material produced that will be easy to adapt to FParsec.

## Getting Started
I just followed the [tutorial](http://www.quanttec.com/fparsec/tutorial.html).  Rather than download the tutorial's source code, I decided to follow along and write it all myself.

## Testing, testing

I recently discovered *proper* testing with xUnit and FsCheck so I wanted to use those tools instead of just printing out things to stdout.  But I couldn't, for the life of me, get the values out of the parser to test.  [Fog Creek's FParsec blog entry](https://blog.fogcreek.com/fparsec/) came to the rescue.  I borrowed some of their code:

```fsharp
    exception ParseError of string
    let parse parser input = 
        match run parser input with 
            | Success (result, _, _) -> result 
            | Failure (error, _, _) -> raise (ParseError error) 
```

Then wrote my first test like this:

```fsharp
    [<Fact>]
    let ``"1.25" is parsed as 1.25f`` () =
        let r = parse pfloat "1.25"
        Assert.Equal(1.25, r)
```

The very next test showed me that I had to handle expected failures.  Once again a couple of bloggers to the rescue:

First up, [Björn Rochel](http://www.bjoernrochel.de/about/)'s [one liner](http://www.bjoernrochel.de/2010/04/19/testing-f-code-with-xunit-net-on-net-4-0/):

```fsharp
    [<Fact>]
    let ``pfloat "1.25E 3" fails`` () = 
        Assert.Throws<ParseError>(fun () -> parse pfloat "1.25E 3" |> ignore)
```

**Note:** pfloat normally return a float which needs to be ignored.

[Richard Banks](https://www.richard-banks.org/about/) suggests a different approach, [one that's more AAA (that's Arrange-Act-Assert) like](https://www.richard-banks.org/2015/07/stop-using-assertthrows-in-your-bdd.html).


```fsharp
    [<Fact>]
    let ``pfloat "1.25E 3" fails`` () = 
        let ex = Record.Exception(fun () -> parse pfloat "1.25E 3" |> ignore)
        Assert.IsType<ParseError>(ex)
```

I like the terseness of Björn's version but I also like the consistency of Richard's.  I can't decide which I prefer.

Now my tests all work as I would like.  Kind of professional, in my view.

## Useful Links
* [FParsec](http://www.quanttec.com/fparsec/) 
* [FParsec Tutorial](http://www.quanttec.com/fparsec/tutorial.html)
* [Phil's practical and easy to understand example using turtles - turtles is a very computer science thing](http://trelford.com/blog/post/FParsec.aspx)
* [Fog Creek's interesting introduction to FParsec from people who use it in production](https://blog.fogcreek.com/fparsec/)
* [Scott's entry on parsing theory](https://fsharpforfunandprofit.com/posts/understanding-parser-combinators/)

## More Links
* [FsCheck](https://fscheck.github.io/FsCheck/)
* [xUnit](https://xunit.github.io/) 

## Parsec Links
* [Parsec Wiki](https://wiki.haskell.org/Parsec)
* [Hackage entry for parsec](https://hackage.haskell.org/package/parsec)