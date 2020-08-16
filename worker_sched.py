import sciolyid.web
from config import config
import sciolyid.web.tasks as tasks

sciolyid.web.setup(config)
tasks.run_beat(["--loglevel=info"])
