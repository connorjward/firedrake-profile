import logparser




LOG_FILE = "assemble.log"


with open(LOG_FILE) as f:
    log = f.read()


stages = logparser.parse_stages(log)