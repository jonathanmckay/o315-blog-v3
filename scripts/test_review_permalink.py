#!/usr/bin/env python3
import csv
import subprocess
import unittest
from pathlib import Path


BLOG_ROOT = Path(__file__).resolve().parents[1]
REVIEW_PATH = "content/reviews/the-faith-of-beasts.md"
EXPECTED_URL = "https://jonathanmckay.com/reviews/the-faith-of-beasts/"
OLD_URL_PATH = BLOG_ROOT / "public/reviews/deflated-dread-the-faith-of-beasts/index.html"


class ReviewPermalinkTest(unittest.TestCase):
    def test_faith_of_beasts_uses_book_title_slug(self):
        result = subprocess.run(
            ["hugo", "list", "all"],
            cwd=BLOG_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        pages = csv.DictReader(result.stdout.splitlines())
        review = next(row for row in pages if row["path"] == REVIEW_PATH)

        self.assertEqual(review["permalink"], EXPECTED_URL)

    def test_old_title_line_url_redirects_to_stable_slug(self):
        subprocess.run(["hugo", "--quiet"], cwd=BLOG_ROOT, check=True)

        self.assertTrue(OLD_URL_PATH.is_file())
        self.assertIn(EXPECTED_URL, OLD_URL_PATH.read_text())


if __name__ == "__main__":
    unittest.main()
