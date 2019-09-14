import re

def strip_comments(code):
    # Find all block comments.  Make sure . matches newline
    # and use non-agressive capture to sure we don't grab
    # across multiple independent blocks
    block_comments = re.compile(r'\s*""".*?"""', re.DOTALL)
    code = block_comments.sub('', code)

    #
    # Strip all one line comments.
    one_line_comments = re.compile(r'\n\s*#.*')
    code = one_line_comments.sub('', code)

    # 
    # Strip any trailing comments that are not embedded
    # within a string
    trailing_comments = re.compile(r'#[^\'"]*$')
    code = trailing_comments.sub('', code)
    return code