from datetime import datetime as dt
from services.service_factory import get_enabled_services
import json
import config as c


def lambda_handler(event, context):

    is_forced = event[c.lambda_is_forced_event_key] \
        if c.lambda_is_forced_event_key in event \
        else False

    data = [{'family':    service.get_service_family_name(),
             'service':   service.get_service_name(),
             'full_name': service.get_service_full_name(),
             'data':      service.get_data(is_forced)}
            for service in get_enabled_services()]

    return {
        'statusCode': 200,
        'body': {
            'fetched_at': json.dumps(f'{dt.now()}'),
            'data': data
        }
    }
