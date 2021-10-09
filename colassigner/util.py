import re

wswitch_rex = re.compile("(?=([a-z|0-9|A-Z][A-Z|0-9]))")


def camel_to_snake(cc_str):
    out = cc_str
    for group in wswitch_rex.findall(cc_str):
        out = out.replace(group, "_".join(group))
    return out.lower()
