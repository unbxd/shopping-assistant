import os
from yaml import load, Loader

dir_path = os.path.dirname(os.path.realpath(__file__))

config_file_path = os.path.join(dir_path, 'config.yaml')
APPLICATION_CONFIG = load(open(config_file_path), Loader=Loader)

# OAuth credentials

# proxy config
PROXY_CONFIG = APPLICATION_CONFIG.get('proxy', {})
PROXY_USER = os.environ.get('PROXY_USER', PROXY_CONFIG.get('user'))
PROXY_PASSWORD = os.environ.get('PROXY_PASSWORD', PROXY_CONFIG.get('password'))
PROXY_IP = os.environ.get('PROXY_IP', PROXY_CONFIG.get('ip'))
PROXY_PORT = os.environ.get('PROXY_PORT', PROXY_CONFIG.get('port'))

# logging config
LOG_LEVEL = os.environ.get('LOG_LEVEL', APPLICATION_CONFIG.get('log_level', 'INFO'))

LOGGING = {
    'version': 1,
    'root': {
        'level': LOG_LEVEL
    }
}

REGION_MAPPING = {
    "use-1d": "us-east-1",
    "ap-southeast-1": "ap-southeast-1",
    "ap-southeast-2": "ap-southeast-2",
    "eu-west-2": "eu-west-2",
    "us-east-4": "us-east4rc",
    "australia-southeast-1": "australia-southeast-1",
}

# mimir endpoint config
MIMIR_US_EAST_1_ENDPOINT = os.environ.get('MIMIR_US_EAST_1_ENDPOINT',
                                          APPLICATION_CONFIG["mimir_endpoints"]["us_east_1"])
MIMIR_AP_SOUTHEAST_1_ENDPOINT = os.environ.get('MIMIR_AP_SOUTHEAST_1_ENDPOINT',
                                               APPLICATION_CONFIG["mimir_endpoints"]["ap_southeast_1"])
MIMIR_AP_SOUTHEAST_2_ENDPOINT = os.environ.get('MIMIR_AP_SOUTHEAST_2_ENDPOINT',
                                               APPLICATION_CONFIG["mimir_endpoints"]["ap_southeast_2"])
MIMIR_EU_WEST_2_ENDPOINT = os.environ.get('MIMIR_EU_WEST_2_ENDPOINT',
                                          APPLICATION_CONFIG["mimir_endpoints"]["eu_west_2"])
MIMIR_US_EAST_4_ENDPOINT = os.environ.get('MIMIR_US_EAST_4_ENDPOINT',
                                          APPLICATION_CONFIG["mimir_endpoints"]["us_east_4"])
MIMIR_AUSTRALIA_SOUTHEAST_1_ENDPOINT = os.environ.get('MIMIR_AUSTRALIA_SOUTHEAST_1_ENDPOINT',
                                                      APPLICATION_CONFIG["mimir_endpoints"]["australia_southeast_1"])
REGION_MIMIR_MAPPING = {
    "use-1d": MIMIR_US_EAST_1_ENDPOINT,
    "ap-southeast-1": MIMIR_AP_SOUTHEAST_1_ENDPOINT,
    "ap-southeast-2": MIMIR_AP_SOUTHEAST_2_ENDPOINT,
    "eu-west-2": MIMIR_EU_WEST_2_ENDPOINT,
    "us-east-4": MIMIR_US_EAST_4_ENDPOINT,
    "australia-southeast-1": MIMIR_AUSTRALIA_SOUTHEAST_1_ENDPOINT,
}

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', "").strip('\n')

DEMO_SITES = {
    "grocery": {
        "site_key": "ss-unbxd-prod-waitrose37331668673646",
        "region": "eu-west-2"
    }
}

