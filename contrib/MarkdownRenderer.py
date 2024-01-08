import misaka as m
from pygments import highlight
from pygments.formatters import HtmlFormatter, ClassNotFound
from pygments.lexers import get_lexer_by_name

class HighlighterRenderer(m.HtmlRenderer):
    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = None

        if lexer:
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)
        # default
        return f'\n<pre class="highlight"><code class="highlight">{text.strip()}</code></pre>\n'
    
renderer = HighlighterRenderer()
markdown_to_html = m.Markdown(renderer, extensions=('fenced-code',))

