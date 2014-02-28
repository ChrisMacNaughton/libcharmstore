import collections
import re


# Define a sequence of allowed constraints to be used in the process of
# preparing the bundle object. See the _prepare_constraints function below.
ALLOWED_CONSTRAINTS = (
    'arch',
    'container',
    'cpu-cores',
    'cpu-power',
    'mem',
    'root-disk',
    # XXX: BradCrittenden 2014-02-12:
    # tags are supported by MaaS only so they are not currently implemented.
    # It is unclear whether the GUI should support them or not so they are
    # being left out for now.
    # Also, tags are a comma-separated, which would clash with the currently
    # broken constraint parsing in the GUI.
    # 'tags',
)


# Constraints should be a string of the form:
# 'k1=v1 k2=v2 ... kn=vn'
# Due to historical reasons, many bundles use a comma-separated list rather
# than the space-separated list juju-core expects.  This regular expression
# handles both separators.
# XXX: BradCrittenden 2014-02-26: The regex is insuffficient to parse the
# 'tags' constraint that is supported for MaaS deployments as the value is a
# comma-separated list.
CONSTRAINTS_REGEX = re.compile('([\w-]+=\w+)[,\s]*?')


def parse_constraints(original_constraints):
    """Parse the constraints and validate them.

    constraints is a space-separated string of key=value pairs or a dict.
    Returns a dict of validated constraints.
    Raises ValueError if one or more constraints is invalid.
    """

    constraints = original_constraints
    if not isinstance(constraints, collections.Mapping):
        constraints = constraints.strip()
        if not constraints:
            return {}
        pairs = CONSTRAINTS_REGEX.findall(constraints)
        constraints = dict(i.split('=') for i in pairs)
    if len(constraints) == 0 or not all(constraints.values()):
        raise ValueError('invalid constraints: {}'.format(
            original_constraints))
    unsupported = set(constraints).difference(ALLOWED_CONSTRAINTS)
    if unsupported:
        msg = 'unsupported constraints: {}'.format(
            ', '.join(sorted(unsupported)))
        raise ValueError(msg)
    return constraints


def check_constraints(original_constraints):
    """Check to see that constraints are space-separated and valid."""
    try:
        parsed = parse_constraints(original_constraints)
    except ValueError:
        return False
    tokens = original_constraints.strip().split()
    return len(parsed) == len(tokens)
