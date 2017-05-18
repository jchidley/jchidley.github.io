---
date: "2017-05-08"
title: Git Epiphany
---

Git Epiphany
============

I only started to use [Git](https://git-scm.com/) because I was using
[GitHub](https://github.com/). My journey started with GitHub’s Windows software
and the [git bash shell](https://git-scm.com/downloads). I followed the
[tutorials](https://try.github.io/) and read the whole of the [Pro Git
Book](https://git-scm.com/book/en/v2). I was confident that I understood things.

In reality, I understood almost nothing and I was frightened all the time.

Today I understand things better. I don’t think that I will ever understand it
completely but I can use it effectively. Below you’ll see how I learned to love
git and stop worrying.

Git Started: Don’t Worry, Use Git
---------------------------------

The best thing I can tell you is this: git doesn’t lose stuff and you can
recover from almost anything. Just follow the [everyday
advice](https://git-scm.com/docs/everyday) and you’ll be fine.

This sounds wrong but you are far safer using git without understanding it than
not using git because you don’t understand.

Losing Photographs
------------------

My attempts to manage my photographs led me to build a system that is based on
the same principles as Git. That experience, combined with [this
article](http://nfarina.com/post/9868516270/git-is-simpler), were the keys that
unlocked git for me.

I have taken thousands of photographs over the years, most of which, even the
actual film ones, are now files on my various home computers. I have managed
them using normal file system tools (e.g file manager and command-line tools)
and Lightroom. I have tried to protect them as best as I can. You would think
that because I am an IT professional this would be no problem.

Sadly I have lost images, sometimes over a thousand at a time, along the way.
Each loss still hurts today and each took a long time to mostly recover from.
Memorably one took about a year fix.

My losses have fallen into 2 categories:

1.  Hardware. Either disk failure or loss of a disk.

2.  User error.

3.  Both of the above.

I have tried several systems to cope with this. Multiple disks,
[RAID](https://en.wikipedia.org/wiki/RAID)s, batch files, various little
utilities, procedures, specialized applications etc. Over the years I grew a
system that would protect my images and, as an interesting by product, helped me
understand git.

Core Design
-----------

Hardware failures are the easiest to solve. I use multiple disks and keep copies
of those disks in separate locations. Each disk has a complete snapshot of my
files which are in various states of synchronicity.

Hard disks are increasing in size faster than the growth of my files so trading
up to the newest disks is always a great idea. I get more space, better
performance and an as new service life (for those that don’t know, every disk
will eventually wear out and fail. If you’re not using it, switch it off).

User and software errors are harder to fix. What I needed was:

1.  Uniquely identify files

2.  Ensure that files remained uncorrupted

3.  Track changes over time, so that when I discovered that I’d done something
    stupid, I could revert things.

Eventually I realised that a [hash](https://en.wikipedia.org/wiki/Hash_function)
of the file would be perfect for both 1 and 2. The hash had to be complex enough
to make duplicate file names nearly impossible, short enough to be quick to
calculate and a public standard for longevity. Cryptographic security is an
irrelevance as I am unworried about malicious intent. SHA1 fitted the bill.

For 3 I needed a small human-readable file with the status of all of the files
that would be timestamped: a census of the files. I could then look through my
censuses and find a known state to recover from.

With both of the above it is easy to track files over time, including name and
location changes. Spotting a corrupted file is trivial because its hash will
change – same name, different hash = corruption.

With this in place, I knew that I would never lose a file again. What I needed
to develop was a bunch of utilities to manage the process. This is hard. This is
where Git comes in.

Git to the Rescue
-----------------

It turns out, my core design [is exactly how Git
works](http://nfarina.com/post/9868516270/git-is-simpler). When I realized that,
I stopped worrying and started to use git aggressively. Git has a wealth of
utilities to help you manage your files.

So, this is how I manage my photography sources today:

1.  Create a top level directory for all of my images.

2.  Run git init on this directory.

3.  Copy my files into the directory.

4.  Use git to manage it.

5.  Copy the whole repository to additional disks.

6.  No longer worry.

The joy and curse of [git](https://git-scm.com/docs/everyday) is that its
utilities have grown organically over time. They can, and do, have bizarre
names, conflicting and duplicating functionality and use different names for the
same basic idea (cache, stage).

The main differences with a programming source control vs a photographic source
control are that you need to track changes within text files and manage multiple
authors. Git has a lot of functionality for those things.

Selected Links
--------------

[Git Is Simpler Than You
Think](http://nfarina.com/post/9868516270/git-is-simpler) is the source of my
epiphany

[Blogging Like a
Hacker](http://tom.preston-werner.com/2008/11/17/blogging-like-a-hacker.html) by
the guy that created GitHub and Jekyll

[Git Magic](http://www-cs-students.stanford.edu/~blynn/gitmagic/ch01.html) is my
current favourite academic style explanation

[just a simple guide for getting started with git. no deep shit
;)](http://rogerdudler.github.io/git-guide/) is a friendlier version of the [git
everyday documentation](https://git-scm.com/docs/everyday)

When I read [Think Like (a) Git](http://think-like-a-git.net/) I no longer felt
like an idiot

[Git for Ages 4 and Up - Video](Git%20for%20Ages%204%20and%20Up%20-%20Video) is
git illustrated with a physical model

I love the pictures in [A Visual Git
Reference](http://marklodato.github.io/visual-git-guide/index-en.html)

I especially like *The Tangled Working Copy Problem* in [The Thing About
Git](https://2ndscale.com/rtomayko/2008/the-thing-about-git)

[Getting
Started](https://www.atlassian.com/git/tutorials/setting-up-a-repository) is an
attractive and helpful site from bitbucket.
