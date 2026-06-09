import unittest

from bs4 import BeautifulSoup, Tag

from extractor.utils import Utils


class MarkdownConversionTest(unittest.TestCase):
    def div_from_html(self, html: str) -> Tag:
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div')
        self.assertIsNotNone(div)
        if not isinstance(div, Tag):
            raise AssertionError('Expected a div tag')
        return div

    def test_does_not_drop_first_characters_when_no_leading_blank_lines(self):
        div = self.div_from_html(
            '<div id="liturgia-2"><p>Salmo</p><p>Resposta</p></div>',
        )

        markdown = Utils.convert_liturgy_soup_to_markdown(div)

        self.assertEqual(markdown, 'Salmo\n\nResposta')

    def test_merges_adjacent_strong_tags_in_titles(self):
        div = self.div_from_html(
            '<div><p><strong>Primeira Leitura (</strong><strong>1Rs 17,1-6)</strong></p></div>',
        )

        markdown = Utils.convert_liturgy_soup_to_markdown(div)

        self.assertEqual(markdown, '**Primeira Leitura (1Rs 17,1-6)**')

    def test_adds_space_between_adjacent_strong_words(self):
        div = self.div_from_html(
            '<div><p><strong>Responsório</strong><strong>Sl 120</strong></p></div>',
        )

        markdown = Utils.convert_liturgy_soup_to_markdown(div)

        self.assertEqual(markdown, '**Responsório Sl 120**')

    def test_removes_audio_embed_noise(self):
        div = self.div_from_html(
            '<div><p><div class="embeds-audio"><iframe src="x"></iframe></div></p><p>Texto</p></div>',
        )

        markdown = Utils.convert_liturgy_soup_to_markdown(div)

        self.assertEqual(markdown, 'Texto')

    def test_normalizes_non_breaking_spaces_and_line_padding(self):
        markdown = Utils.normalize_markdown('  **Responsório\xa0Sl 120**  \n\n  — Palavra  ')

        self.assertEqual(markdown, '**Responsório Sl 120**\n\n— Palavra')


if __name__ == '__main__':
    unittest.main()
