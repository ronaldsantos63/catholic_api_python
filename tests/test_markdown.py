import unittest

from bs4 import BeautifulSoup

from extractor.utils import Utils


class MarkdownConversionTest(unittest.TestCase):
    def test_does_not_drop_first_characters_when_no_leading_blank_lines(self):
        soup = BeautifulSoup(
            '<div id="liturgia-2"><p>Salmo</p><p>Resposta</p></div>',
            'html.parser',
        )

        markdown = Utils.convert_liturgy_soup_to_markdown(soup.div)

        self.assertEqual(markdown, 'Salmo\n\nResposta')

    def test_merges_adjacent_strong_tags_in_titles(self):
        soup = BeautifulSoup(
            '<div><p><strong>Primeira Leitura (</strong><strong>1Rs 17,1-6)</strong></p></div>',
            'html.parser',
        )

        markdown = Utils.convert_liturgy_soup_to_markdown(soup.div)

        self.assertEqual(markdown, '**Primeira Leitura (1Rs 17,1-6)**')

    def test_adds_space_between_adjacent_strong_words(self):
        soup = BeautifulSoup(
            '<div><p><strong>Responsório</strong><strong>Sl 120</strong></p></div>',
            'html.parser',
        )

        markdown = Utils.convert_liturgy_soup_to_markdown(soup.div)

        self.assertEqual(markdown, '**Responsório Sl 120**')

    def test_removes_audio_embed_noise(self):
        soup = BeautifulSoup(
            '<div><p><div class="embeds-audio"><iframe src="x"></iframe></div></p><p>Texto</p></div>',
            'html.parser',
        )

        markdown = Utils.convert_liturgy_soup_to_markdown(soup.div)

        self.assertEqual(markdown, 'Texto')

    def test_normalizes_non_breaking_spaces_and_line_padding(self):
        markdown = Utils.normalize_markdown('  **Responsório\xa0Sl 120**  \n\n  — Palavra  ')

        self.assertEqual(markdown, '**Responsório Sl 120**\n\n— Palavra')


if __name__ == '__main__':
    unittest.main()
