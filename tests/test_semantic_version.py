import unittest

from semantic_versioning import SemanticVersion


class TestEqualsSemanticVersion(unittest.TestCase):
    def test_equals_correct(self):
        assert SemanticVersion(1, 2, 3) == SemanticVersion(1, 2, 3)
        assert SemanticVersion(1, 2, 3, [1, 2]) == SemanticVersion(1, 2, 3, [1, 2])
        assert SemanticVersion(1, 2, 3, [1, 2], "a", 4, 5, 6) == SemanticVersion(
            1,
            2,
            3,
            [1, 2],
            "a",
            4,
            5,
            6,
        )

    def test_equals_incorrect(self):
        assert SemanticVersion(1, 5, 3) != SemanticVersion(1, 2, 3)
        assert SemanticVersion(1, 2, 3, [1, 2]) != SemanticVersion(1, 2, 3, [3, 2])
        assert SemanticVersion(1, 2, 3, [1, 2], "a", 4, 5, 6) != SemanticVersion(
            1,
            2,
            3,
            [1, 2],
            "b",
            4,
            5,
            6,
        )
        assert SemanticVersion(1, 2, 3, [1, 2], "a", 4, 5, 6) != SemanticVersion(
            1,
            2,
            3,
            [1, 2],
            "a",
            7,
            5,
            6,
        )


class TestParseSemanticVersion(unittest.TestCase):
    def test_parse_simple_correct(self):
        assert SemanticVersion.parse("1") == SemanticVersion(1)
        assert SemanticVersion.parse("1.0") == SemanticVersion(1, 0)
        assert SemanticVersion.parse("1.12.0") == SemanticVersion(1, 12, 0)
        assert SemanticVersion.parse("3.4.1.4") == SemanticVersion(3, 4, 1, [4])
        assert SemanticVersion.parse("3.4.1.4.6") == SemanticVersion(3, 4, 1, [4, 6])

    def test_parse_release_correct(self):
        assert SemanticVersion.parse("1-dev1") == SemanticVersion(1, dev_release=1)
        assert SemanticVersion.parse("1.post12") == SemanticVersion(1, post_release=12)
        assert SemanticVersion.parse("1.3a3") == SemanticVersion(
            1,
            3,
            pre_release_type="a",
            pre_release=3,
        )
        assert SemanticVersion.parse("1.3.5a3_dev1") == SemanticVersion(
            1,
            3,
            5,
            pre_release_type="a",
            pre_release=3,
            dev_release=1,
        )


class TestValidateSemanticVersion(unittest.TestCase):
    def test_validate_correct(self):
        assert SemanticVersion.validate("0")
        assert SemanticVersion.validate("0.5")
        assert SemanticVersion.validate("0.5b4")
        assert SemanticVersion.validate("3.4.1.4.6")
        assert SemanticVersion.validate("3.4.1.4.6rc4.post134444-dev0")
        assert SemanticVersion.validate("3.4.1.4.6a4.dev0")
        assert SemanticVersion.validate("3.4.post0")

    def test_validate_incorrect(self):
        # 0 prefix not allowed.
        assert not SemanticVersion.validate("1.01.0")
        # Pre-release after dev-release incorrect.
        assert not SemanticVersion.validate("1.0.9.dev1a4")
        # Post-release after dev-release incorrect.
        assert not SemanticVersion.validate("1.0.9.dev1.post4")
        # Unknown pre-release token.
        assert not SemanticVersion.validate("1.0.9c4")
        # No separator before prerelease.
        assert not SemanticVersion.validate("1.0.9.a4")


class TestCompareSemanticVersion(unittest.TestCase):
    def test_compare_simple_correct(self):
        assert SemanticVersion(1) < SemanticVersion(2)
        assert SemanticVersion(1, 1) < SemanticVersion(2)
        assert SemanticVersion(1, 1, 3) < SemanticVersion(2)
        assert SemanticVersion(1, 1) < SemanticVersion(1, 2)
        assert SemanticVersion(1, 1, 1) < SemanticVersion(1, 2)
        assert SemanticVersion(1, 1, 1) < SemanticVersion(1, 1, 2)
        assert SemanticVersion(1, 1, 1, [1]) < SemanticVersion(1, 1, 2)
        assert SemanticVersion(1, 1, 1, [1, 1]) < SemanticVersion(1, 1, 1, [2])
        assert SemanticVersion(1, 1, 1, [1, 1]) < SemanticVersion(1, 1, 1, [1, 2])

    def test_compare_release_correct(self):
        assert SemanticVersion(1, pre_release_type="a", pre_release=1) < SemanticVersion(1)
        assert SemanticVersion(1, pre_release_type="a", pre_release=1) < SemanticVersion(
            1,
            pre_release_type="b",
            pre_release=1,
        )
        assert SemanticVersion(1, pre_release_type="a", pre_release=1) < SemanticVersion(
            1,
            pre_release_type="a",
            pre_release=2,
        )
        assert SemanticVersion(1, post_release=1) < SemanticVersion(
            1,
            pre_release_type="a",
            pre_release=1,
        )
        assert SemanticVersion(1, dev_release=1) < SemanticVersion(1, post_release=1)
        assert SemanticVersion(1, 0, 0, dev_release=1) < SemanticVersion(1, 0, 0, dev_release=2)
        assert SemanticVersion(1, 0, 0, [1, 1], dev_release=1) < SemanticVersion(
            1,
            0,
            0,
            [1, 1],
            dev_release=2,
        )


class TestStringifySemanticVersion(unittest.TestCase):
    def test_stringify_simple_correct(self):
        assert str(SemanticVersion(1)) == "1"
        assert str(SemanticVersion(1, 12)) == "1.12"
        assert str(SemanticVersion(1, 12, 0)) == "1.12.0"
        assert str(SemanticVersion(1, 12, 0, [4])) == "1.12.0.4"
        assert str(SemanticVersion(1, 12, 0, [4, 5])) == "1.12.0.4.5"

    def test_stringify_other_separator_correct(self):
        assert SemanticVersion(1).to_string(separator="-") == "1"
        assert SemanticVersion(1, 12).to_string(separator="-") == "1-12"
        assert SemanticVersion(1, 12, 0).to_string(separator="-") == "1-12-0"
        assert SemanticVersion(1, 12, 0, [4]).to_string(separator="-") == "1-12-0-4"
        assert SemanticVersion(1, 12, 0, [4, 5]).to_string(separator="-") == "1-12-0-4-5"

    def test_stringify_release_correct(self):
        assert str(SemanticVersion(1, pre_release_type="a", pre_release=3)) == "1a3"
        assert str(SemanticVersion(1, 12, pre_release_type="b", pre_release=0)) == "1.12b0"
        assert str(SemanticVersion(1, 12, 0, post_release=4)) == "1.12.0.post4"
        assert str(SemanticVersion(1, 12, 0, [4, 5], dev_release=1)) == "1.12.0.4.5.dev1"
