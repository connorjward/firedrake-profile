import re


class Pattern:

    scientific_notation = r"\d+.\d+e[+-]\d+"
    percent = r"\d+.\d+%"


def parse_stages(f):
    patterns = [r"\s+\d+:\s+(?P<name>.*):"]
    for prefix in ["time", "flop", "messages", "message_lengths", "reductions"]:
        pattern = (r"\s+(?P<{prefix}>{sci_num})\s+(?P<{prefix}_percent>{percent})"
                   .format(prefix=prefix,
                           sci_num=Pattern.scientific_notation, 
                           percent=Pattern.percent))
        patterns.append(pattern)

    stages = re.finditer("".join(patterns), f)

    return stages


LOG_FILE = "assemble.log"


with open(LOG_FILE) as f:
    log = f.read()

#pattern = re.compile("\s+\d+:\s+(?P<name>.*):\s+(?P<time>\d+.\d+e[+-]\d+)")

#stages = pattern.finditer(log)
stages = parse_stages(log)
for stage in stages:
    print(stage.group("name"))