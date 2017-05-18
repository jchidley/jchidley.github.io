---
date: "2017-05-18"
title: Git Epilogue
---

Git Epilogue
============

I reread the [Pro Git book](https://git-scm.com/book/en/v2) and *actually*
understood it.

Fixing Problems
---------------

I messed up my git log during a rebase: I orphaned a branch and then merged it
back into the master. If you’ve done this, you’ll know how ugly the history
becomes.

In frustration, I “fixed” the dirty history by deleting .git and starting fresh.
The good news is that my data was completely unaffected. The bad news was I lost
my git history. What I have learnt since then would have allowed me to fix
things properly without losing my history.

Rewriting History
-----------------

To clean up my public history, I just did a

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
git commit --amend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

on a branch, followed by a

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
git reset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

on the master and finished with a

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
git push -f
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I *knew* the pitfalls with public commits and I *knew* that it was no problem!

Line Ending Wrinkles
--------------------

When using *bash on ubuntu on Windows* all of my files appeared to have changed.
This is owing to the different way that line endings are handled in Linux and
Windows. The solution was to run this command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
git config --global core.autocrlf true
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
