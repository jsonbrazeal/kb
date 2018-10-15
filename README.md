kb
==
View and manage knowledge base resources on the command line. kb recognizes
3 types of resources: examples, notes, and other. The path to examples
is set with the environment variable KB_EX_PATH, and commands like search and list
default to the examples path. To expand these command to more paths, pass a flag
for notes only or all resources. The root path for all resources is set with the
environment variable KB_PATH.

```bash
Usage:
  kb <resource>
  kb -e <resource>
  kb -c <resource>
  kb -x <resource>
  kb -l [-a] [-n] [-w]
  kb -d [-a] [-n] [-w]
  kb -s <keyword> [-a] [-n] [-w]
  kb -f
  kb -v
  kb -h

Options:
  -e --edit         Edit example resource; searches for resource by file name in
                    KB_EX_PATH first, then searches for resource by full path in KB_PATH
  -c --create       Create example resource in KB_EX_PATH
  -x --delete       Delete example resource in KB_EX_PATH

  -d --directories  List KB_EX_PATH by default; may be used with -a and -n
  -l --list         List resources in KB_EX_PATH by default; may be used with -a and -n
  -s --search       Search for <keyword> in KB_EX_PATH by default; may be used with -a and -n

  -a --all          Apply action to all resources
  -n --notes        Apply action to plain text notes only (.md or .txt files)
  -w --web          Include resources fetched from web

  -f --fetch        Fetch and build example resources from the web in KB_EX_PATH/_web
  -v --version      Print version
  -h --help         Print help

Examples:

  To view the examples for `tar`:
    kb tar

  To list all available examples:
    kb -l

  To list all available notes:
    kb -l -n

  To list all available resources:
    kb -l -a

  To search for "ssh" among all examples:
    kb -s ssh

  To search for "ssh" among all resources:
    kb -s -a ssh

  To create the `bar` example resource:
    kb -c bar

  To edit the `bar` example resource:
    kb -e bar

  To delete the `bar` example resource:
    kb -x bar

  To edit the `foo` note (text files only, full path required with -n option):
    kb -e /path/to/foo/note -n

  To fetch and build example resources from the web:
    kb -f
```

kb is forked from cheat (https://github.com/chrisallenlane/cheat). It also draws inspiration and content from eg (https://github.com/srsudar/eg), tldr (https://github.com/tldr-pages/tldr), and cheat.sh (https://github.com/chubin/cheat.sheets).
