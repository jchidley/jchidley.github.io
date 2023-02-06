---
---

<!-- markdownlint-disable MD025 -->
# Template
<!-- markdownlint-enable MD025 -->

## Introduction

I have been using shells since the 1980s - over 40 years. If you are, or aspire to be, a systems administrator using shells is required for professional use. 

Almost all of my working life had beeen spent on DOS and then Windows (I loved PowerShell). I had been using 'nix shells like very powerfull DOS/Windows ones. I was wrong. To be really effective on 'nix requires a deep understanding of the shell (ideally a POSIX one), shell quoting rules, `sed`, `awk`, 'here documents' and `tee`. This is because the unix was first used on text terminals and the primary user interface was the shell. 

Everything on 'nix is a file and almost all 'nix shell programs are designed to take text input and deliver text output.

### Quoting

"I highly recomment you get in the habit of using "echo" as a way to check what is going to happen with the meta-characters." (https://www.grymoire.com/Unix/Quote.html)

to see what is happening inside a script
```bash
sh -v script # verbose
sh -x script # variables
```

[Difference Between grep, sed, and awk | Baeldung on Linux](https://www.baeldung.com/linux/grep-sed-awk-differences)
Using `diff` to create an editing script for `ed`  [Linux diff command help and examples](https://www.computerhope.com/unix/udiff.htm)

### diff, patch and ed

[Linux diff – How to Compare Two Files and Apply Changes with the Patch Command](https://www.freecodecamp.org/news/compare-files-with-diff-in-linux/)

[How to Apply a Patch to a File (and Create Patches) in Linux](https://www.howtogeek.com/415442/how-to-apply-a-patch-to-a-file-and-create-patches-in-linux/)

```bash
sed '1i this is a new line' original > changed
diff -u original changed > patch.original
patch -u -b original < patch.original # -b make a backup copy
diff -s original changed
```

```text
Files orginal and changed are identical
```

Note: `diff -u` to be the standard output of `busybox` `diff`. 

`diff -e` is for the editor `ed`. `patch -U` undo a patch

[ed Scripts (Comparing and Merging Files)](https://www.gnu.org/software/diffutils/manual/html_node/ed-Scripts.html)

### sed

Never forget that `sed` stands for "stream editor" and should be treated like an automated editor. The process should be to write a script and test the outputs before commiting to final version. Another way to use `sed` is to treat it like a programming language with a REPL (Read Evaluate Print Loop).

Edit input files line by line and output them to a new file. Proably best to test on a small representative sample that fits on one screen. `sed -n 'l'` will show you what is in your data. Use `diff` to compare the before and after versions. Once the output file is perfected, use `mv` to replace the original. This is the safest way to use `sed`.

`gsed` has the extremely useful `--debug` switch.

Ensure that you have single line actions at the script top before any multiline ones. Have single line actions as well as multiple line actions for the same change. Specific to general. Multiline actions have a tendency to eat your input.

* [sed very basics](https://www.pement.org/sed/sed_basics.htm)
* "sed & awk, 2nd Edition" by Dale Dougherty and Arnold Robbins
* [Sed - An Introduction and Tutorial](https://www.grymoire.com/Unix/Sed.html)
* Revision [Linux sed command help and examples](https://www.computerhope.com/unix/used.htm)
* [sed, the stream editor]( https://www.pement.org/sed/index.htm)
* [HANDY ONE-LINE SCRIPTS FOR sed](https://www.pement.org/sed/sed1line.txt)
* [Sed One-Liners Explained](https://catonmat.net/sed-one-liners-explained-part-one)
* [Frequent 'sed' Questions - Stack Overflow](https://stackoverflow.com/questions/tagged/sed?tab=Frequent)
* [Seder's grab bag](http://sed.sourceforge.net/grabbag/)
* [Introduction to sed, written in 1978](http://sed.sourceforge.net/grabbag/tutorials/sed_mcmahon.txt)
* Proof that `sed` is Turing Complete [Implementation of a Turing Machine as Sed Script](http://sed.sourceforge.net/grabbag/scripts/turing.txt) & [turing.sed](http://sed.sourceforge.net/grabbag/scripts/turing.sed)
* [Sed script that converts Markdown to HTML](https://github.com/stamby/md-to-html) 
* [Minimised sed](http://www.guckes.net/sed/)

### awk

* [awk](https://www.pement.org/awk.htm)
* [Chart of similar operations with sed and awk](https://www.pement.org/awk/awk_sed.txt)
* [How to Use awk](https://sparky.rice.edu//~hartigan/awk.html)
* [Guide to awk](https://web.archive.org/web/20040805135014/http://www.canberra.edu.au/~sam/whp/awk-guide.html)
* [printf() usage   -   formatted printing in awk](https://www.pement.org/awk/printf.txt)
* [HANDY ONE-LINE SCRIPTS FOR AWK](https://www.pement.org/awk/awk1line.txt)
* [Awk One-Liners Explained](https://catonmat.net/awk-one-liners-explained-part-one)
* [Title](https://web.mit.edu/gnu/doc/html/gawk_3.html)
* [Don’t MAWK AWK – the fastest and most elegant big data munging language! | AI and Social Science – Brendan O'Connor](https://brenocon.com/blog/2009/09/dont-mawk-awk-the-fastest-and-most-elegant-big-data-munging-language/)
* [The state of the AWK [LWN.net]](https://lwn.net/Articles/820829/)
* [Command-line-text-processing/gnu_awk.md at master · learnbyexample/Command-line-text-processing · GitHub](https://github.com/learnbyexample/Command-line-text-processing/blob/master/gnu_awk.md)
* Not really a parser [GitHub - step-/JSON.awk: Practical JSON parser written in awk](https://github.com/step-/JSON.awk)
* [Solene'% : Minimalistic markdown subset to html converter using awk](https://dataswamp.org/~solene/2019-08-26-minimal-markdown.html)
* [GitHub - knazarov/markdown.awk: A pure awk implementation of markdown-to-html](https://github.com/knazarov/markdown.awk)
* [Awk script to generate HTML documentation from markdown text in source code comments. · GitHub](https://gist.github.com/wernsey/eb1525876ca5519822ab48e68207970f)

### make

[Makefile Tutorial By Example](https://makefiletutorial.com)
[Make](https://www.grymoire.com/Unix/Make.html)

### test

* [Bash Test Operators Cheat Sheet - Kapeli](https://kapeli.com/cheat_sheets/Bash_Test_Operators.docset/Contents/Resources/Documents/index)

## Links

<!-- markdownlint-disable MD034 -->
* https://example.com
<!-- markdownlint-enable MD034 -->

* "Unix for Poets" by Kenneth Ward Church
* "The Linux Command Line" by William Shotts
* [LinuxCommand.org: Learn The Linux Command Line. Write Shell Scripts.](http://linuxcommand.org)
shell
* [POSIX Shell Tutorial](https://www.grymoire.com/Unix/Sh.html#toc_Sh_-_the_POSIX_Shell_)
* [UNIX Shell Quotes - a simple tutorial](https://www.grymoire.com/Unix/Quote.html)
* [sed very basics](https://www.pement.org/sed/sed_basics.htm)

Linux
* [Linux Tutorials ](https://www.grymoire.com/Unix/index.html)
* ["Unix for Poets" by Ken Church](https://www.cs.upc.edu/~padro/Unixforpoets.pdf)
* [Command-line Tools can be 235x Faster than your Hadoop Cluster - Adam Drake](https://adamdrake.com/command-line-tools-can-be-235x-faster-than-your-hadoop-cluster.html)