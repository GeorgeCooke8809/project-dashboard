import pytest
import projects

class TestRenderMarkdown:
    def test_render_empty_string(self):
        assert projects.utils.render_markdown("") == ""

    def test_render_none(self):
        assert projects.utils.render_markdown(None) == ""

    def test_render_plain_text(self):
        html = projects.utils.render_markdown("Hello")

        assert "<p>Hello</p>" in html

    def test_render_line_break(self):
        html = projects.utils.render_markdown("Line 1\nLine 2")

        assert "<br />" in html

    def test_render_heading(self):
        html = projects.utils.render_markdown("## Overview")

        assert "<h2>Overview</h2>" in html

    def test_render_bold_and_italic(self):
        html = projects.utils.render_markdown("**bold** and *italic*")

        assert "<strong>bold</strong>" in html
        assert "<em>italic</em>" in html

    def test_render_bullet_list(self):
        html = projects.utils.render_markdown("- One\n- Two")

        assert "<ul>" in html
        assert "<li>One</li>" in html

    def test_render_numbered_list(self):
        html = projects.utils.render_markdown("1. One\n2. Two")

        assert "<ol>" in html
        assert "<li>Two</li>" in html

    def test_render_link(self):
        html = projects.utils.render_markdown("[GitHub](https://github.com)")

        assert "<a href=\"https://github.com\">GitHub</a>" in html

    def test_render_inline_code(self):
        html = projects.utils.render_markdown("`x = 1`")

        assert "<code>x = 1</code>" in html

    def test_render_table(self):
        html = projects.utils.render_markdown("| Name | Language |\n| --- | --- |\n| Dashboard | Python |")

        assert "<table>" in html
        assert "<th>Name</th>" in html
        assert "<td>Python</td>" in html

    def test_render_code_block_python(self):
        html = projects.utils.render_markdown("```python\ndef test():\n    pass\n```")

        assert "class=\"highlight\"" in html
        assert "<span class=\"k\">def</span>" in html

    def test_render_code_block_other_language(self):
        html = projects.utils.render_markdown("```powershell\nWrite-Host \"Hi\"\n```")

        assert "class=\"highlight\"" in html
        assert "<span class=\"nb\">Write-Host</span>" in html

    def test_render_code_block_no_language(self):
        html = projects.utils.render_markdown("```\ndef test():\n    pass\n```")

        assert "class=\"highlight\"" in html
        assert "<span class=\"k\">" not in html

    def test_render_code_block_language_label(self):
        html = projects.utils.render_markdown("```python\nprint(\"Hi\")\n```")

        assert "<pre><code data-language=\"python\">" in html

    def test_render_code_block_other_language_label(self):
        html = projects.utils.render_markdown("```ps1\nWrite-Host \"Hi\"\n```")

        assert "data-language=\"ps1\"" in html

    def test_render_code_block_no_language_label(self):
        html = projects.utils.render_markdown("```\nHello\n```")

        assert "data-language=\"text\"" in html

    def test_render_code_block_keeps_pre(self):
        html = projects.utils.render_markdown("```python\nprint(\"Hi\")\n```")

        assert html.count("<pre>") == 1

    def test_render_html_passed_through(self):
        html = projects.utils.render_markdown("<b>Hi</b>")

        assert "<b>Hi</b>" in html