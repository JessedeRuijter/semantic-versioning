from .flags import Operator

POS_NUM = r"(0|[1-9]\d*)"
VERSION_PATTERN = rf"(?P<major>{POS_NUM})(\.(?P<minor>{POS_NUM}))?(\.(?P<patch>{POS_NUM}))?(?P<versions>(\.{POS_NUM})*)?"
RELEASE_PATTERN = rf"((?P<pre_release_type>a|b|rc)(?P<pre_release>{POS_NUM}))?((\.|-|_)post(?P<post_release>{POS_NUM}))?((\.|-|_)dev(?P<dev_release>{POS_NUM}))?"
FULL_VERSION_PATTERN = rf"{VERSION_PATTERN}{RELEASE_PATTERN}"

OPERATOR_PATTERN = "|".join([operator.value for operator in Operator])
EXPRESSION_PATTERN = rf"(?P<operator>{(OPERATOR_PATTERN)})(?P<version>{FULL_VERSION_PATTERN})"
