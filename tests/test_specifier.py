import unittest
from semantic_versioning import SemanticVersion, Specifier

class TestEqualsSemanticVersion(unittest.TestCase):
    def test_equals_correct(self):
        assert Specifier.parse(">1.2.1").complies(SemanticVersion(1, 2, 3))
        assert not Specifier.parse(">1.2.1").complies(SemanticVersion(1, 2, 0))
    
        assert Specifier.parse("<1.2.1").complies(SemanticVersion(1, 2, 0))
        assert not Specifier.parse("<1.2.1").complies(SemanticVersion(1, 2, 3))

        assert Specifier.parse("==1.2.1").complies(SemanticVersion(1, 2, 1))
        assert not Specifier.parse("==1.2.1").complies(SemanticVersion(1, 2, 3))
