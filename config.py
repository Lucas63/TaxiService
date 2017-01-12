

minute_length = 1


log_config = {
"version": 1,
"disable_existing_loggers": 0,
"root": {
"level": "DEBUG",
"handlers": [
"console",
"debugfile"
]
},
"loggers": {

},
"formatters": {
"precise": {
"format": "%(asctime)s %(name)-15s %(levelname)-8s %(message)s"
},
"brief": {
"format": "%(levelname)-8s: %(name)-15s: %(message)s"
}
},
"handlers": {
"debugfile": {
"class": "logging.FileHandler",
"formatter": "precise",
"mode": "a",
"level": "DEBUG",
"filename": "log/debug.log"
},
"console": {
"formatter": "precise",
"class": "logging.StreamHandler",
"stream": "ext://sys.stdout",
"level": "DEBUG"
}
}
}
"""
dictConfig(settings.log_config)
dictConfig(settings.log_error)

logger = logging.getLogger("log_config")

logger.info("Server started")
"""