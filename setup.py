from distutils.core import setup

setup(
    name="kb",
    version="1.0.0",
    author="Jason Brazeal",
    author_email="jsonbrazeal@gmail.com",
    description="kb is forked from cheat (https://github.com/chrisallenlane/cheat). "
    "It also draws inspiration and content from eg (https://github.com/srsudar/eg), "
    "tldr (https://github.com/tldr-pages/tldr), and cheat.sh (https://github.com/chubin/cheat.sheets)"
    "It is a command line interface for a knowledge base consisting of text files and more. "
    "kb allows viewing of plain text resources, examples, and notes in a terminal and can launch "
    "a browser for viewing other file types.",
    url="https://github.com/jsonbrazeal/kb",
    packages=["kb", "kb.test"],
    scripts=["bin/kb"],
    install_requires=["docopt >= 0.6.1", "pygments >= 1.6.0", "python-magic >= 0.4.15"],
)
