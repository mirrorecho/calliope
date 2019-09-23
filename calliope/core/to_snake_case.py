import re

# SEE COMMENT AT: https://gist.github.com/jaytaylor/3660565
def to_snake_case(s):
    return re.sub("([A-Z])", "_\\1", s).lower().lstrip("_")