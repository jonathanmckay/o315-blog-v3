#!/usr/bin/env python3
import unittest
from pathlib import Path


BLOG_ROOT = Path(__file__).resolve().parents[1]
REVIEWS = BLOG_ROOT / "content/reviews"


MISDATED_2008_IMPORTS = [
    "grown-up-digital-how-the-net-generation-is-changing-your-world.md",
    "eon.md",
    "first-in-an-insiders-account-of-how-the-cia-spearheaded-the-war-on-terror-in-afg.md",
    "from-russia-with-love.md",
    "imperial-life-in-the-emerald-city-inside-iraqs-green-zone.md",
    "in-defense-of-the-nation-dia-at-forty-years.md",
    "legacy-of-ashes-the-history-of-the-cia.md",
    "halo-contact-harvest.md",
    "naked-economics-undressing-the-dismal-science.md",
    "realities-of-foreign-service-life.md",
    "smart-mobs-the-next-social-revolution.md",
    "state-of-denial.md",
    "the-gamble-general-david-petraeus-and-the-american-military-adventure-in-iraq-20.md",
    "the-lexus-and-the-olive-tree.md",
    "the-lost-colony.md",
    "the-origin-of-species.md",
    "tomorrow-when-the-war-began.md",
    "wall-and-piece.md",
]


def frontmatter(path):
    text = path.read_text()
    raw = text.split("---", 2)[1]
    data = {}
    for line in raw.splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            data[key] = value.strip('"')
    return data


class ReviewMetadataTest(unittest.TestCase):
    def test_2008_goodreads_imports_do_not_sort_as_new_2026_reviews(self):
        for filename in MISDATED_2008_IMPORTS:
            with self.subTest(filename=filename):
                self.assertEqual(frontmatter(REVIEWS / filename)["date"], "2008-01-01")

    def test_title_line_period_does_not_precede_separator(self):
        title = frontmatter(REVIEWS / "the-shockwave-rider.md")["title"]

        self.assertEqual(title, "Proto-cyberpunk that thinks harder than it feels: The Shockwave Rider")
        self.assertNotIn(".:", title)

    def test_title_line_question_mark_replaces_separator(self):
        title = frontmatter(REVIEWS / "there-is-no-antimemetics-division.md")["title"]

        self.assertEqual(title, "Perception warped, weaponized, what? There Is No Antimemetics Division")
        self.assertNotIn("?:", title)

    def test_abbreviated_book_titles_keep_period_before_subtitle_colon(self):
        self.assertEqual(
            frontmatter(REVIEWS / "dubai-co-global-strategies-for-doing-business-in-the-gulf-states.md")["title"],
            "Dubai & Co.: Global Strategies for Doing Business in the Gulf States",
        )
        self.assertEqual(
            frontmatter(REVIEWS / "creativity-inc-overcoming-the-unseen-forces-that-stand-in-the-way-of-true-inspir.md")["title"],
            "Creativity, Inc.: Overcoming the Unseen Forces That Stand in the Way of True Inspiration",
        )

    def test_review_titles_do_not_have_losing_punctuation_before_separator(self):
        allowed_period_colon = {"Dubai & Co.:", "Creativity, Inc.:"}
        for path in REVIEWS.glob("*.md"):
            if path.name == "_index.md":
                continue
            title = frontmatter(path).get("title", "")
            with self.subTest(filename=path.name):
                self.assertNotIn("?:", title)
                if ".:" in title:
                    self.assertTrue(any(allowed in title for allowed in allowed_period_colon), title)


if __name__ == "__main__":
    unittest.main()
