from datetime import datetime as dt
from services.service_factory import get_enabled_services
import json


def lambda_handler(event, context):

    data = [{'service': service.get_service_name(),
             'data': service.get_data()}
            for service in get_enabled_services()]

    return {
        'statusCode': 200,
        'body': {
            'fetched_at': json.dumps(f'{dt.now()}'),
            'data': data
        }
    }
