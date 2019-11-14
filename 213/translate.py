import re


def replace_all(trans_text, src_texts, replacement_texts):
    for i, src_text in enumerate(src_texts):
        trans_text = trans_text.replace(src_text, replacement_texts[i])
    return trans_text


def fix_translation(org_text, trans_text):
    """Receives original English text as well as text returned by translator.
       Parse trans_text restoring the original (English) code (wrapped inside
       code and pre tags) into it. Return the fixed translation str
    """
    pre_matcher = re.compile(r'(<pre>[^<]*</pre>)', re.DOTALL)
    trans_text = replace_all(trans_text, pre_matcher.findall(
        trans_text), pre_matcher.findall(org_text))
    code_matcher = re.compile(r'(<code>[^<]*</code>)', re.DOTALL)
    trans_text = replace_all(trans_text, code_matcher.findall(
        trans_text), code_matcher.findall(org_text))
    return trans_text
