# semantic_versioning
Another semantic versioning package, but better! It follows semantic versioning described in **PEP440**.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **semantic_versioning**.

```bash
pip install semantic_versioning
```

## Usage
Use **validate** function to check if versions in strings are correctly formatted.

```python
from semantic_versioning import SemanticVersion

# use to validate (returns True)
assert SemanticVersion.validate("3.4.5-dev1")
```

Use **parse** function to load a SemanticVersion object from a string.

```python
from semantic_versioning import SemanticVersion

SemanticVersion.parse("1.2.4")
# SemanticVersion(major=1, minor=2, patch=3)

SemanticVersion.parse("1.2a3.dev6")
# SemanticVersion(major=1, minor=2, pre_release_type="a", pre_release=3, dev_release=6)

SemanticVersion.parse("1-5-6", separator="-")
# SemanticVersion(major=1, minor=5, patch=3)

SemanticVersion.parse("1.0.1.2.5")
# SemanticVersion(major=1, minor=0, patch=1, versions=[2,5])
```

The SemanticVersion class is comparable and will correctly take pre/dev/post releases into account.

```python
from semantic_versioning import SemanticVersion

SemanticVersion.parse("1.2.3") < SemanticVersion.parse("1.2.4") # True
SemanticVersion.parse("1.2.3") < SemanticVersion.parse("1.2") # True
SemanticVersion.parse("1.2.dev0") < SemanticVersion.parse("1.2.dev1") # True
SemanticVersion.parse("1.2.dev0") < SemanticVersion.parse("1.2") # True
SemanticVersion.parse("1.2a1") < SemanticVersion.parse("1.2b0") # True
SemanticVersion.parse("1.2a1") < SemanticVersion.parse("1.2.post2") # True
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
