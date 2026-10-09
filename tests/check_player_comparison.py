"""Mutation checks ensure fallback copy exceptions cannot hide player changes."""
import unittest
from check_final_polish import normalize_fallback_copy

URL = 'https://example.test/video'
PLAYER = ('<div class="video-shell" data-video="original">'
          '<iframe src="original" allowfullscreen></iframe>'
          '<button class="play-button">Play</button>'
          '<a class="film-watch-link" href="' + URL + '" target="_blank" rel="noopener">'
          'Watch <span aria-hidden="true">↗</span></a></div>')


class StrictPlayerComparison(unittest.TestCase):
    def normalized(self, value):
        return normalize_fallback_copy(value, URL)

    def test_only_fallback_class_and_text_are_excluded(self):
        changed = PLAYER.replace('class="film-watch-link"', 'class="film-watch-link outline"')
        changed = changed.replace('Watch ', '觀看影片 ').replace('↗', 'Open')
        self.assertEqual(self.normalized(PLAYER), self.normalized(changed))

    def test_player_and_link_mutations_remain_visible(self):
        for before, after in [
            ('data-video="original"', 'data-video="different"'),
            ('src="original"', 'src="different"'),
            ('class="play-button"', 'class="play-button changed"'),
            ('<iframe', '<video'),
            ('allowfullscreen', 'allow="autoplay"'),
            ('href="' + URL + '"', 'href="https://example.test/other"'),
            ('target="_blank"', 'target="_self"'),
            ('rel="noopener"', 'rel="opener"'),
            ('aria-hidden="true"', 'aria-hidden="false"'),
            ('<span aria-hidden="true">↗</span>', '↗'),
        ]:
            with self.subTest(change=after):
                self.assertNotEqual(self.normalized(PLAYER), self.normalized(PLAYER.replace(before, after)))


if __name__ == '__main__':
    unittest.main()
