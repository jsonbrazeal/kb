from io import BytesIO
import os
import subprocess
import sys
from zipfile import ZipFile

import magic
import requests


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
    ex_path = ex_dir().pop()
    web_ex_path = os.path.join(ex_path, '.web')
    return kb_dirs(pretty_print=pretty_print) - ex_dir(pretty_print=pretty_print) - {web_ex_path}


def list_resources(scope='examples', pretty_print=False, include_web=False):
    """Lists the available resources"""

    if scope == 'examples':
        root_set = ex_dir()
    elif scope == 'notes':
        root_set = note_dirs()
    elif scope == 'all':
        root_set = kb_dirs()
    else:
        return None

    ex_path = ex_dir().pop()
    web_ex_path = os.path.join(ex_path, '.web/')

    resources = []
    for root_dir in root_set:
        for root, directories, files in os.walk(root_dir):
            for f in files:
                if f.startswith('.') or f.startswith('__'):
                    continue
                resources.append((f, os.path.join(root, f)))

    resources = sorted(resources, key=lambda kv: str.lower(kv[0]))

    if include_web:
        for root, directories, files in os.walk(web_ex_path):
            for f in files:
                if f.startswith('.') or f.startswith('__'):
                    continue
                resources.append((f, os.path.join(root, f)))

    if not len(resources):
        return None

    if not include_web:
        resources = [r for r in resources if web_ex_path not in r[1]]

    if scope == 'notes':
        resources = [(r, p) for r, p in resources if r.endswith(('md', 'txt'))]

    if pretty_print:
        resources_output = ''
        for r in resources:
            resources_output += f'{r[0][:40]:<45} {r[1][:80]}\n'
        return resources_output

    return set(resources)


def search(term, scope='examples', include_web=False):
    """Searches all resources for the term in the scope"""
    resources = list_resources(scope=scope, include_web=include_web)
    # if not include_web:
    #     ex_path = ex_dir().pop()
    #     web_ex_path = os.path.join(ex_path, '.web/')
    #     resources = [r for r in resources if web_ex_path not in r[1]]

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


def colorize(content, resource_name):
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
        lexer = get_lexer_by_name(resource_name)
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


def edit(file_path, notes=False):
    """Open `file_path` using sublime"""
    edit_path = ''
    # check examples path first (kb html)
    examples = list_resources(scope='examples')
    local_examples = [e for e in examples if '.web' not in e[1]]
    if file_path in [e[0] for e in local_examples]:
        edit_path = os.path.join(ex_dir().pop(), file_path)
    # check notes path next, full path required (kb "$KB_PATH/dev/html")
    notes = list_resources(scope='notes')
    if file_path in [e[1] for e in notes] and is_text_file(file_path):
        edit_path = file_path
    if not edit_path:
        die(f'Unable to open {file_path} for editing.')

    subprocess.run(['subl', '-n', edit_path])


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


def read(resource):
    """Returns the contents of the resource as a string. Searches examples path
    first, then considers notes paths.
    """
    output = ''
    for r, p in list_resources('examples', include_web=True):
        if r == resource and os.path.exists(p):
            with open(p) as f:
                output += f.read() + '\n'
    if output:
        return output

    for r, p in list_resources('notes'):
        if p == resource and os.path.exists(p):
            with open(p) as f:
                return f.read()


def fetch():
    """Fetch and build example resources from the web in KB_EX_PATH/.web"""
    ex_path = ex_dir().pop()
    web_ex_path = os.path.join(ex_path, '.web/')
    if not os.path.exists(web_ex_path):
        try:
            os.mkdir(web_ex_path)
        except Exception as e:
            print(e)
            die(f'{web_ex_path} did not exist and an error occurred when trying to create it.')

    # fork all these to my github and point these links there
    # Dict[url: zip_target_dir]
    URLS = {'https://github.com/jsonbrazeal/cheat.sheets/archive/master.zip': 'cheat.sheets-master/sheets/',
            'https://github.com/jsonbrazeal/cheat/archive/master.zip': 'cheat-master/cheat/cheatsheets/',
            'https://github.com/jsonbrazeal/tldr/archive/master.zip': 'tldr-master/pages/',
            'https://github.com/jsonbrazeal/eg/archive/master.zip': 'eg-master/eg/examples/'}

    for url in URLS.keys():
        print(f'fetching data from {url}...')
        response = requests.get(url)
        if 'tldr' in url:
            with ZipFile(BytesIO(response.content), 'r') as repo_file:
                for info in repo_file.infolist():
                    if not info.filename.startswith(URLS[url]):
                        continue
                    resource = info.filename.replace(URLS[url], '')
                    if not resource:
                        continue # skip zip_target_dir/URLS[url]
                    if resource in ('common/', 'linux/', 'osx/', 'windows/'):
                        continue # skip category dirs
                    target_file_name, _ = os.path.splitext(os.path.basename(info.filename))
                    target_file_path = os.path.join(web_ex_path, target_file_name)
                    if target_file_path == web_ex_path:
                        continue
                    data = repo_file.read(info)
                    category = resource.split(os.sep)[0]
                    if category == 'common':
                        notes = ''
                    elif category == 'linux':
                        notes = ' (linux)'
                    elif category == 'osx':
                        notes = ' (macos)'
                    elif category == 'windows':
                        notes = ' (windows)'
                    with open(target_file_path, 'a') as f:
                        lines = data.decode('utf-8').splitlines()
                        lines[0] = lines[0] + notes
                        if f.tell(): # f.tell() == 0 means the file has no content
                            f.write('\n\n')
                        f.write('\n'.join(lines))
        else:
            with ZipFile(BytesIO(response.content), 'r') as repo_file:
                for info in repo_file.infolist():
                    if not info.filename.startswith(URLS[url]):
                        continue
                    resource = info.filename.replace(URLS[url], '')
                    if not resource:
                        continue # skip zip_web_ex_path
                    if len(resource.split(os.sep)) > 1:
                        continue # skip directories inside zip_web_ex_path
                    if not resource[0].isalnum():
                        continue # skip files beginning with non alphanumeric chars
                    file_name, file_ext = os.path.splitext(resource)
                    if file_ext not in ('', '.md'):
                        continue # only allow files with no extension or .md files
                    data = repo_file.read(info)
                    data_str = data.decode('utf-8')
                    first_line = data_str.splitlines()[0]
                    target_file_path = os.path.join(web_ex_path, os.path.basename(file_name))
                    with open(target_file_path, 'a') as f:
                        if f.tell(): # f.tell() == 0 means the file has no content
                            f.write('\n\n') # add space before adding more content
                        elif f'# {file_name}' not in first_line:
                            f.write(f'# {file_name}\n\n') # add md header as the first thing in the file if not present
                        # if 'cheat.sheets-master' in z or 'cheat-master' in z:
                        #     f.write('```bash\n')
                        #     f.write(data_str)
                        #     f.write('```\n')
                        # else:
                        f.write(data_str)
    return('done!')
