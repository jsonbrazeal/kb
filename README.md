[![PyPI](https://img.shields.io/pypi/v/cheat.svg)](https://pypi.python.org/pypi/cheat/)

cheat
=====
`cheat` allows you to create and view interactive resources on the
command-line. It was designed to help remind \*nix system administrators of
options for commands that they use frequently, but not frequently enough to
remember.

![The obligatory xkcd](http://imgs.xkcd.com/comics/tar.png 'The obligatory xkcd')


Example
-------
The next time you're forced to disarm a nuclear weapon without consulting
Google, you may run:

```sh
cheat tar
```

You will be presented with a resource resembling:

```sh
# To extract an uncompressed archive:
tar -xvf '/path/to/foo.tar'

# To extract a .gz archive:
tar -xzvf '/path/to/foo.tgz'

# To create a .gz archive:
tar -czvf '/path/to/foo.tgz' '/path/to/foo/'

# To extract a .bz2 archive:
tar -xjvf '/path/to/foo.tgz'

# To create a .bz2 archive:
tar -cjvf '/path/to/foo.tgz' '/path/to/foo/'
```

To see what resources are available, run `cheat -l`.

Note that, while `cheat` was designed primarily for \*nix system administrators,
it is agnostic as to what content it stores. If you would like to use `cheat`
to store notes on your favorite cookie recipes, feel free.


Installing
----------
It is recommended to install `cheat` with `pip`:

```sh
[sudo] pip install cheat
```

[Other installation methods are available][installing].


Modifying Cheatsheets
---------------------
The value of `cheat` is that it allows you to create your own resources - the
defaults are meant to serve only as a starting point, and can and should be
modified.

Cheatsheets are stored in the `~/.cheat/` directory, and are named on a
per-keyphrase basis. In other words, the content for the `tar` resource lives
in the `~/.cheat/tar` file.

Provided that you have a `VISUAL`, or `EDITOR` environment
variable set, you may edit resources with:

```sh
cheat -e foo
```

If the `foo` resource already exists, it will be opened for editing.
Otherwise, it will be created automatically.

After you've customized your resources, I urge you to track `~/.cheat/` along
with your [dotfiles][].


Configuring
-----------

### Setting a KB_EX_PATH ###
Personal resources are saved in the `~/.cheat` directory by default, but you
can specify a different default by exporting a `KB_EX_PATH` environment
variable:

```sh
export KB_EX_PATH='/path/to/my/cheats'
```

### Setting a KB_PATH ###
You can additionally instruct `cheat` to look for resources in other
directories by exporting a `KB_PATH` environment variable:

```sh
export KB_PATH='/path/to/my/cheats'
```

You may, of course, append multiple directories to your `KB_PATH`:

```sh
export KB_PATH="$KB_PATH:/path/to/more/cheats"
```

You may view which directories are on your `KB_PATH` with `cheat -d`.

### Enabling Syntax Highlighting ###
`cheat` can optionally apply syntax highlighting to your resources. To enable
syntax highlighting, export a `KB_COLORS` environment variable:

```sh
export KB_COLORS=true
```

#### Specifying a Syntax Highlighter ####
You may manually specify which syntax highlighter to use for each resource by
wrapping the sheet's contents in a [Github-Flavored Markdown code-fence][gfm].

Example:

<pre>
```sql
-- to select a user by ID
SELECT *
FROM Users
WHERE id = 100
```
</pre>

If no syntax highlighter is specified, the `bash` highlighter will be used by
default.


See Also:
---------
- [Enabling Command-line Autocompletion][autocompletion]
- [Related Projects][related-projects]


[autocompletion]:   https://github.com/chrisallenlane/cheat/wiki/Enabling-Command-line-Autocompletion
[dotfiles]:         http://dotfiles.github.io/
[gfm]:              https://help.github.com/articles/creating-and-highlighting-code-blocks/
[installing]:       https://github.com/chrisallenlane/cheat/wiki/Installing
[related-projects]: https://github.com/chrisallenlane/cheat/wiki/Related-Projects
