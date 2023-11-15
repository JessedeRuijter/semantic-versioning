import unittest
from semversion import SemanticVersion


class TestParseSemanticVersion(unittest.TestCase):
    def test_parse_simple_correct(self):
        assert SemanticVersion.parse("1") == SemanticVersion(1)
        assert SemanticVersion.parse("1.0") == SemanticVersion(1, 0)
        assert SemanticVersion.parse("1.12.0") == SemanticVersion(1, 12, 0)
        assert SemanticVersion.parse("3.4.1.4") == SemanticVersion(3,4,1,[4])
        assert SemanticVersion.parse("3.4.1.4.6") == SemanticVersion(3,4,1,[4,6])

    def test_parse_release_correct(self):
        assert SemanticVersion.parse("1-dev1") == SemanticVersion(1, dev_release=1)
        assert SemanticVersion.parse("1.post12") == SemanticVersion(1, post_release=12)
        assert SemanticVersion.parse("1.3a3") == SemanticVersion(1, 3, pre_release_type="a", pre_release=3)
        assert SemanticVersion.parse("1.3.5a3_dev1") == SemanticVersion(1, 3, 5, pre_release_type="a", pre_release=3, dev_release=1)



class TestValidateSemanticVersion(unittest.TestCase):
    def test_validate_correct(self):
        assert SemanticVersion.validate("0")
        assert SemanticVersion.validate("0.5")
        assert SemanticVersion.validate("0.5b4")
        assert SemanticVersion.validate("3.4.1.4.6")
        assert SemanticVersion.validate("3.4.1.4.6rc4-dev0.post134444")

    def test_validate_incorrect(self):
        assert SemanticVersion.parse("1-dev1") == SemanticVersion(1, dev_release=1)
        assert SemanticVersion.parse("1.post12") == SemanticVersion(1, post_release=12)
        assert SemanticVersion.parse("1.3a3") == SemanticVersion(1, 3, pre_release_type="a", pre_release=3)
        assert SemanticVersion.parse("1.3.5a3_dev1") == SemanticVersion(1, 3, 5, pre_release_type="a", pre_release=3, dev_release=1)
