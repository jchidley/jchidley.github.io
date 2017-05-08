---
layout: default
title: Continuing to choose F\#
date: 2017-04-28
---
Continuing to choose F\#
========================

Last year, at the age of 48, I retired.

I retired because I wanted to make my own choices and spend time on stuff that
mattered to me. Working for anyone else, even for customers, is restricting.
Had I still loved the company that I worked for and
the job that I was doing, this wouldn't have been an issue.

Now I can pursue my passions without external compromises. One of those passions
has always been Information Technology (others include my wife, family,
exercise, photography, food and drink). I can investigate and do anything that I
want in IT, including programming. My long career in IT as a practitioner hasn't
included any significant programming but I’ve dabbled in a few languages, including C,
Pascal, BASIC, Fortran and C#.

I chose F\# a while back, it seemed interesting and logical to me but no
language choice is permanent or exclusive. I wanted to see what alternatives
there are now.

After a long search and much reflection, it came down to two things. Firstly, it
had to be a functional language and secondly that language would be F\#. Why
those choices? I am glad you asked.

Why a Functional Language
-------------------------

[Functional languages](http://www.defmacro.org/ramblings/fp.html) generally, and
F\# in particular, *feel right* to me. For [this
author's](https://jamesmccaffrey.wordpress.com/2015/03/01/why-i-dont-like-the-f-language/)
is the primary reason why he doesn't like F\#.

I don't like other languages because:
* x = x + 1 *is nonsense*.
* Shared state, global variables and mutability make things hard to understand and difficult to debug. 
* While objects are easy to use, I find them difficult to understand and construct.
* I understand things better by layout and not by {}; and other tokens.

My first "real" program was modifying an existing Fortran77 application – used
to identify crystal structures from X-ray diffraction photographs. I changed the
source to move from global mutable shared state to passing data between
functions. I did this because I couldn't work out what was going on. The
original was probably faster but mine was easier to understand.

Of course, immutability requires recursion. I still don't fully understand it
but I can use it effectively. [It's turtles all the way down](https://en.wikipedia.org/wiki/Discworld).

Why F\#
-------

F\# is functional first but still allows all of the other programming models. I
love the fact that it is very strict about types and does type inference. My
programs break early at compile time and then I can work out why. I use the
interpreter to quickly check how things work, REPL is amazing.

My other language needs are that it has to have a future, to be industrial
strength, to be highly functional, to have broad support, strong libraries and a
good community. For me, F\# is simply stronger in all of these things than the
alternatives (e.g. Haskell, OCaml, Scala). 

For the foreseeable future, Microsoft Windows is a viable platform. Some kind of
.net will always be a choice. F\# is the only mainstream .net language that is
fully functional. Microsoft is working hard to extend .net to other platforms
and Mono is being actively updated and improved. You can even program
iPhone/iPad and Android devices in F\# using Xamarin.

As for community, firstly, there are still a lot of .net developers out there
and people are going to be maintaining .net systems for a long time to come.
Many of the libraries used in F\# programs are just ordinary .net ones.
All of the advice for .net is transferable: C\# has a huge community that is
also relevant for F\#.

The F\# community itself is a very friendly place full of scarily smart people.
It has one of the larger communities on stackoverflow for a functional language.
Because it is based on ML and OCaml basic language concepts are shared with
those communities too.

### Other Links

See why [Colin Bull](http://www.colinbull.net/2015/03/24/Why-I-Like-FSharp/)
likes the language. If you’re interested in learning F\# then check [Biarity
Blog](http://biarity.me/2016/11/30/An-unassuming-F-study-plan/).
