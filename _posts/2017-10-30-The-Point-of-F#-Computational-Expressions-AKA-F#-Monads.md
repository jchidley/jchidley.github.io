---
date: "2017-10-30"
title: "The Point of F# Computational Expressions AKA F# Monads"
---

# What's the Point of a F# Computational Expression AKA F# Monad?
**TL;DR** To make ugly, complex, repetitive code simpler and more elegant to write.  In this sense, it's like the reason why you'd write a function.

e.g. 
```
query {
    for customer in db.Customers do
        select customer
}
```
Looks like a SQL query to me.  


## Introduction
I could not, for the life of me, understand the point of F# Computational Expressions (which can, [as I understand it now](https://cs.stackexchange.com/questions/29210/is-computation-expression-the-same-as-monad), also be used to write a Monad).  I agree with what [Scott wrote about monads](https://fsharpforfunandprofit.com/posts/why-i-wont-be-writing-a-monad-tutorial/). 

My current understanding is that you use a computational expression when you want to:
1. Express a solution to a problem in an elegant domain specific way.
2. Hide complex, repetitive, side-effect-ridden code into something easy to use.

The examples that spring to mind are
``async { expression }`` or ``seq { expression }``.  Both are simple to use and written as computational expressions.  They are all, effectively, mini domain specific languages (DSLs).

Here's another, easy to understand, example from [this post](http://richardminerich.com/2011/02/the-road-to-functional-programming-in-f-from-imperative-to-computation-expressions/):

[Project Euler](https://projecteuler.net/) Problem 1: Find the sum of all the multiples of 3 or 5 below 1000.

F# computational expression solution:
```fsharp
let pe1 limit = eb2 { for x = 0 to limit - 1 do yield x }

let computationalSolution = pe1 1000
```

The original imperative solution looked like this:

```fsharp
let pe1_while limit =
    let mutable acc = 0
    let mutable x = 0
    while x < limit do
        if x % 5 = 0 || x % 3 = 0 then acc <- acc + x
        x <- x + 1
    acc

let imperativeSolution = pe1_while 1000
```

## Simple to Use Doesn't Mean Simple to Write

It is straightforward to use a computational expression but it is not obvious, to me now, how to write one.  See below for the source for eb2 above.  I don't think that it'll be worth it for a one-off problem like Project Euler 1.

```
type Euler1Builder2() =
    member b.Yield(x) = if x % 5 = 0 || x % 3 = 0 then x else 0
    member b.For(generated, f) = generated |> Seq.map (fun x -> f x)
    member b.Run(filtered: int seq) = filtered |> Seq.sum 

let eb2 = new Euler1Builder2()
```

Using ``seq { 0 .. 10 .. 100 }`` is simple enough to use everywhere.   I bet the [source code](https://stackoverflow.com/questions/24875805/where-is-the-source-code-for-the-sequence-expression-builder) for a sequence expression is a whole lot more complicated than that line of code implies.

## Links
* [The Road to Functional Programming in F# – From Imperative to Computation Expressions](http://richardminerich.com/2011/02/the-road-to-functional-programming-in-f-from-imperative-to-computation-expressions/)
* [Computation expressions: Introduction](https://fsharpforfunandprofit.com/posts/computation-expressions-intro/) 
* [Monads as computation](https://wiki.haskell.org/Monads_as_computation)


