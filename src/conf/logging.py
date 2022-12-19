def get_logging(log_level: str = 'INFO') -> dict:
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': log_level,
            'handlers': ['stdout'],
        },
        'formatters': {
            'simple': {
                'format': '%(asctime)s %(module)s.%(funcName)s[%(lineno)d] %(message)s'
            },
        },
        'handlers': {
            'null': {
                'class': 'logging.NullHandler',
            },
            'stdout': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            'aiohttp.access': {
                'handlers': ['stdout'],
                'level': log_level,
                'propagate': False,
            }
        }
    }
