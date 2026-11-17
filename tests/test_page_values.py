"""tools/make_page.py: this page's own values (a copy of Kovai Minnal with the district's words)"""
import re, subprocess, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "research_free"), str(ROOT / "poster")]
import allnews, post, validate      # noqa: E402


class PageValues(unittest.TestCase):
    def test_names(self):
        self.assertEqual(post.PAGE, "chennai")
        self.assertEqual(post.TAG, "#ChennaiMinnal")
        self.assertEqual(validate.LAST, "மேலும் செய்திகளுக்கு சென்னை மின்னல் பக்கத்தை பின்தொடருங்கள்.")
        self.assertEqual(post.FOLLOW_LINE, validate.LAST)

    def test_own_district_only(self):
        self.assertTrue(allnews.has_place("சென்னையில் பேருந்து விபத்து"))
        self.assertTrue(allnews.other_district("கோவையில் பேருந்து விபத்து"))
        self.assertTrue(allnews.other_district("செங்கல்பட்டு அருகே விபத்து") or "chennai" == "chengalpattu")

    def test_no_kovai_name_left_in_code(self):
        out = subprocess.run(["grep", "-rIlE", "Kovai Minnal|கோவை மின்னல்|kovai_minnal|KovaiMinnal|kovaiminnal", str(ROOT), "--include=*.py",
                              "--include=*.yml", "--include=*.json", "--exclude-dir=fb_posted", "--exclude-dir=.git", "--exclude-dir=tests"],
                             capture_output=True, text=True).stdout.split()
        self.assertEqual(out, [])


if __name__ == "__main__":
    unittest.main()
