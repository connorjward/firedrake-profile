"""
???
"""

import re


class Pattern:
    scientific_notation = r"\d+.\d+e[+-]\d+"
    percent = r"\d+.\d+%"


class PETScLogParser:

    def __init__(self, flog):
        with open(flog) as f:
            self._text = f.read()


    def parse_stage_time(self, stage_name):
        for stage in self._parse_stages():
            if stage["name"] == stage_name:
                return float(stage["time"])
        raise KeyError


    def _parse_stages(self):
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

        matches = re.finditer("".join(patterns), self._text)

        return [match.groupdict() for match in matches]
