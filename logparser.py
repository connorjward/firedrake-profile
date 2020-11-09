import re


class Pattern:
    scientific_notation = r"\d+.\d+e[+-]\d+"
    percent = r"\d+.\d+%"


def parse_stages(input_str):
    """
    Return a list of matches corresponding to the 'Summary of Stages'
    section of the PETSc log output.
    """
    patterns = [r"\s+\d+:\s+(?P<name>.*):"]
    for prefix in ["time", "flop", "mess", "mess_len", "rdct"]:
        pattern = (r"\s+(?P<{prefix}>{sci_num})"
                       r"\s+(?P<{prefix}_percent>{percent})"
                       .format(prefix=prefix,
                               sci_num=Pattern.scientific_notation, 
                               percent=Pattern.percent))
        patterns.append(pattern)

    return [match for match in re.finditer("".join(patterns), input_str)]

