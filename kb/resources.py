import os
import sys
import subprocess

import magic


def read(resource):
    """Returns the contents of the resource as a string"""
    for r, p in list_resources('all'):
        if r == resource and os.path.exists(p):
            with open(p) as f:
                return f.read()


def is_text_file(file_path):
    """Returns true if a file's mimetype is text/whatever"""
    if not os.path.exists(file_path) or os.path.isdir(file_path) or not os.access(file_path, os.R_OK):
        return False
    mimetype = magic.from_file(file_path, mime=True)
    if mimetype.startswith('text/'):
        return True
    return False


def ex_dir(pretty_print=False):
    """Returns a set with one member, the default example path"""
    example_dir = os.environ.get('KB_EX_PATH')
    if not example_dir:
        die('Please set the environment variable KB_EX_PATH.')
    example_dir = os.path.expanduser(os.path.expandvars(example_dir))
    if not os.path.isdir(example_dir):
        die('Please set the environment variable KB_EX_PATH to an existing directory.')
    # assert that the KB_EX_PATH is readable and writable
    if not os.access(example_dir, os.R_OK):
        die('The KB_EX_PATH (' + example_dir +') is not readable.')
    if not os.access(example_dir, os.W_OK):
        die('The KB_EX_PATH (' + example_dir +') is not writable.')

    if example_dir.endswith('/'):
        example_dir = example_dir.rstrip('/')

    if pretty_print:
        example_dir += ' (KB_EX_PATH)'
    return {example_dir}


def kb_dirs(pretty_print=False):
    """Assembles the set of all directories containing resources"""

    kb_path =os.environ.get('KB_PATH')
    if not kb_path:
        die('The KB_PATH environment variable must be set.')

    kb_path = os.path.expanduser(os.environ['KB_PATH'])
    if not os.path.isdir(kb_path):
        die('The KB_PATH must be a directory.')

    dirs = [kb_path]
    for root, directories, files in os.walk(kb_path):
        dirs.extend([os.path.join(root, d) for d in directories])

    if pretty_print:
        for i, p in enumerate(dirs[:]):
            kb_ex_path = os.path.expanduser(os.environ['KB_EX_PATH'])
            if p.rstrip('/') == kb_ex_path.rstrip('/'):
                dirs[i] = f'{p} (KB_EX_PATH)'
            if p.rstrip('/') == kb_path.rstrip('/'):
                dirs[i] = f'{p} (KB_PATH)'

    return set(dirs)


def note_dirs(pretty_print=False):
    """Assembles the set of all directories in the knowledge base that don't
    contain examples.
    """
    return kb_dirs(pretty_print=pretty_print) - ex_dir(pretty_print=pretty_print)


def get(root_dirs):
    """Assembles a dictionary of resources as name => file-path recursively
    throughout root_dir
    """
    resources = {}
    for root_dir in root_dirs:
        for root, directories, files in os.walk(root_dir):
            for f in files:
                if f.startswith('.') or f.startswith('__'):
                    continue
                resources.update({f: os.path.join(root, f)})
    return resources


def list_resources(scope='examples', pretty_print=False):
    """Lists the available resources"""

    if scope == 'examples':
        root = ex_dir()
    elif scope == 'notes':
        root = note_dirs()
    elif scope == 'all':
        root = kb_dirs()
    else:
        return None

    resources = sorted(get(root).items(), key=lambda kv: str.lower(kv[0]))
    if not len(resources):
        return None

    if scope == 'notes':
        resources = [(r, p) for r, p in resources if r.endswith(('md', 'txt'))]

    if pretty_print:
        resources_output = ''
        for r in resources:
            resources_output += f'{r[0][:40]:<45} {r[1][:80]}\n'
        return resources_output

    return resources


def search(term, scope='examples'):
    """Searches all resources for the term in the scope"""
    resources = list_resources(scope=scope)

    result = ''

    for r, p in resources:
        match = ''
        if not is_text_file(p):
            continue
        with open(p) as f:
            for line in f:
                if term in line:
                    match += '  ' + line

        if match != '':
            result += f'*****{r}*****:\n{match}\n'

    return result


def colorize(content, resource):
    """Colorizes resource content if so configured"""

    # only colorize if so configured
    if not 'KB_COLORS' in os.environ or os.environ.get('KB_COLORS', '').lower() == 'false':
        return content

    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import Terminal256Formatter

    # if pygments can't load, just return the uncolorized text
    except ImportError:
        return content

    # default to markdown
    lexer = get_lexer_by_name('md')

    # try to get a lexer by the same name as the file
    try:
        lexer = get_lexer_by_name(resource)
    except Exception:
        pass

    # check if the entire content is a code block and if so get the correct lexer
    first_line = content.splitlines()[0]
    if first_line.startswith('```'):
        content = '\n'.join(content.splitlines()[1:]).rstrip('`\n')
        try:
            lexer = get_lexer_by_name(first_line[3:])
        except Exception:
            pass

    return highlight(content, lexer, Terminal256Formatter(style='monokai'))


def die(message):
    """Prints a message to stderr and then terminates"""
    print((message), file=sys.stderr)
    exit(1)


def edit(file_path):
    """Open `file_path` using sublime"""
    if is_text_file(file_path):
        subprocess.run(['subl', '-n', file_path])
    else:
        examples = list_resources(scope='examples')
        if file_path in [e[0] for e in examples]:
            subprocess.run(['subl', '-n', os.path.join(ex_dir().pop(), file_path)])
        else:
            print(f'Unable to open {file_path}. Full path is required except for examples.')


def create(resource):
    """Create example resource using sublime"""
    ex_path = ex_dir().pop()
    if os.path.exists(os.path.join(ex_path, resource)):
        die(f'Unable to create {resource} because it already exists. Try editing it instead.')
    else:
        subprocess.run(['subl', '-n', os.path.join(ex_path, resource)])


def delete(resource):
    """Delete example resource"""
    ex_path = ex_dir().pop()
    file_path = os.path.join(ex_path, resource)
    if not os.path.exists(file_path):
        die(f'Unable to delete {resource} because it does not exist.')
    else:
        os.remove(file_path)
