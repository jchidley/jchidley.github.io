---
---
<!-- markdownlint-disable MD025 -->
# GitHub Pages & Jekyll
<!-- markdownlint-enable MD025 -->

## GitHub Pages
(Static pages)[https://jekyllrb.com/docs/pages/] are the basic building block of any website. These can be [Markdown](https://daringfireball.net/projects/markdown/) `.md` or html `.html` and can be arranged into subfolders. 

(Posts)[https://jekyllrb.com/docs/posts/] are for blogs. These are kept in a `_posts` directory, the name of which is in the following format `YEAR-MONTH-DAY-title.MARKUP`. The top of the post must include [front matter](https://jekyllrb.com/docs/front-matter/).

[Front matter](https://jekyllrb.com/docs/front-matter/) looks like this:

```html
---
layout: post
title: Blogging Like a Hacker
---
```

which is `yaml` and the variables defined are used in liquid markup.

The minimum is this:

```html
---
---
```

Predefined variables for Jekyll include: `layout`, `permalink` and `published`. Post specific variables include: `date`, `category`, `categories` and `tags`; these variables (apart from date) can be yaml lists like this:

```yaml
--- # Favorite movies
- Casablanca
- North by Northwest
- The Man Who Wasn't There
```

or this:

```yaml
--- # Shopping list
[milk, pumpkin pie, eggs, juice]
```

Draft posts are kept in a `_drafts` directory and are not published.

### Relative links

Use the name of the file, say `2022-08-04-GitHub-Pages-Jekyll.md`, and it will automagically be given the right link when the site is generated. Like this:

[This page](2022-08-04-GitHub-Pages-Jekyll.md)

## Jekyll

Jekyll is used by GitHub to publish and manage the website.

## Spelling or Misspelling

It turns out that spell checking any kind of code is problematic. The only tool on an iPad that will do this automatically is the keyboard (this is often annoying as it'll autocorrect words it doesn't recognise, like names or technical terms).

The only tool that I've found that might do this is [CSpell](https://cspell.org). For more information see this [blog entry](https://tjaddison.com/blog/2021/02/spell-checking-your-markdown-blog-posts-with-cspell/) and more information about a [Visual Studio Code version](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)

Yet another argument for a seperate linux box, like a Raspberry Pi, in addition to iPad.

## Process

Write a draft document, using the filename for correct date and document title. Push to github. 

Pull from github on a linux box to:
* spell check
* move to _posts
* push to github

## Links

<!-- markdownlint-disable MD034 -->
<!-- markdownlint-enable MD034 -->
* [GitHub Pages Documentation](https://docs.github.com/en/pages)
* [Quickstart | Jekyll • Simple, blog-aware, static sites](https://jekyllrb.com/docs/)