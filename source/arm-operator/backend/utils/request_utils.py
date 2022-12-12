from global_variables import Config


def get_common_headers():
    return {"x-access-token": Config.IC_TOKEN}
