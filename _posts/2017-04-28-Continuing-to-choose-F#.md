---
date: "2017-04-28"
title: "Continuing to choose F#"
---

Continuing to choose F\#
========================

One of my life-long passions is Information Technology (others include my wife,
family, exercise, photography, food and drink). I love investigating and trying
out new things. My 25 year career in IT hasn't included any significant
programming but I’ve dabbled in a few languages.

I chose F\# a while back as it seemed both interesting and logical to me but no
language choice is permanent or exclusive. I wanted to see what alternatives
there are now.

After a long search and much reflection, I made two choices. Firstly, it had to
be a functional language and secondly that language would be F\#. Why those
choices? I am glad you asked.

Why a Functional Language
-------------------------

[Functional languages](http://www.defmacro.org/ramblings/fp.html) generally, and
F\# in particular, *feel right* to me. Feel is [this
author](https://jamesmccaffrey.wordpress.com/2015/03/01/why-i-dont-like-the-f-language/)’s
primary reason why he doesn't like F\#.

I don't like other languages because:

-   x = x + 1 *is nonsense*.

-   Shared state, global variables and mutability make things hard to understand
    and difficult to debug.

-   While objects are easy to use, I find them difficult to understand and
    construct.

-   I understand things better by layout and not by {}; and other tokens.

My first "real" program project was modifying a FORTRAN77 application for
identifying crystal structures from X-ray diffraction photographs. I changed the
source to move from global mutable shared state to passing data between
functions. I did this because I couldn't work out what was going on. The
original application was probably faster but mine was easier to understand.

Of course, immutability requires recursion. I still don't fully understand
recursion but I can use it effectively. [It's turtles all the way
down](https://en.wikipedia.org/wiki/Discworld).

Why F\#
-------

F\# is functional first but still allows all the [other programming models and
styles](http://theburningmonk.com/fsharp-exercises-in-programming-style/). I
love the fact that it is very strict about types and does type inference. It
certainly makes you focus on types. My programs break early at compile time and
then I can work out why. I love the REPL.

My other language needs are that it has to have a future, to be industrial
strength, to be highly functional, to have broad support, strong libraries and a
good community. For me, F\# is simply stronger in all of these things than the
alternatives (e.g. Haskell, OCaml, Scala).

For the foreseeable future, Microsoft Windows is a viable platform. Some kind of
.net will always be a choice and they are, very slowly, moving .net to other
platforms. Mono is being actively upgraded. F\# is the only mainstream .net
language that is fully functional. You can even program iPhone/iPad and Android
devices in F\# using Xamarin.

As for community there are still a lot of .net developers out there and people
are going to be maintaining .net systems for a long time to come. Many of the
libraries used in F\# programs are just ordinary .net ones. All of the advice
for .net is transferable: C\# has a huge community that is also relevant for
F\#.

The F\# community itself is a very friendly place full of scarily smart people.
It has one of the larger communities on stackoverflow for a functional language.
Because it is based on ML and OCaml basic language concepts are shared with
those communities too.

### Other Links

See why [Colin Bull](http://www.colinbull.net/2015/03/24/Why-I-Like-FSharp/)
likes the language. If you’re interested in learning F\# then check [Biarity
log](http://biarity.me/2016/11/30/An-unassuming-F-study-plan/).
