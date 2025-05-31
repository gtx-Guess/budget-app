from pyairtable import Api as pyairtableapiclient
from constants import AIRTABLE_ACCESS_TOKEN, AIRTABLE_ACCOUNTS, AIRTABLE_TRANSACTIONS, AIRTABLE_DB_ID
from datetime import datetime
import pytz
from typing import Dict, List, Union, Any

AIRTABLE_API = pyairtableapiclient(AIRTABLE_ACCESS_TOKEN)
TRANSACTION_FIELDS = ["*Name", "**Date", "**USD", "*Vendor", "*Notes"]
ACCOUNT_FIELDS = ["**Institution", "**USD", "**Last Successful Update"]

REQUEST_TYPES = {
    "transactions": {
        "fields": TRANSACTION_FIELDS,
        "table": AIRTABLE_TRANSACTIONS
    },
    "accounts": {
        "fields": ACCOUNT_FIELDS,
        "table": AIRTABLE_ACCOUNTS
    }
}

def make_request_to_airtable(request_type: str) -> Dict[str, Any]:
    """
    Make a request to Airtable API and clean the response data.
    """
    try:
        request_config = REQUEST_TYPES[request_type]
        table = AIRTABLE_API.table(AIRTABLE_DB_ID, request_config["table"])
        response = table.all(fields=request_config["fields"])
        clean_data = clean_response_data(response)
        return clean_data
    except KeyError:
        raise ValueError(f"Invalid request type: {request_type}. Valid types are: {list(REQUEST_TYPES.keys())}")
    except Exception as e:
        raise Exception(f"Error making Airtable request: {str(e)}")

def clean_response_data(data: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
    """
    Clean and format the response data, including datetime conversion to PST.
    """
    if isinstance(data, dict):
        cleaned_dict = {}
        for k, v in data.items():
            clean_key = k.replace('*', '')
            if isinstance(v, str) and (k.lower().endswith('date') or k.lower().endswith('time')):
                try:
                    if 'T' in v and v.endswith('Z'):
                        date_obj = datetime.fromisoformat(v.replace('Z', '+00:00'))
                        pst = pytz.timezone('America/Los_Angeles')
                        pst_time = date_obj.astimezone(pst)
                        cleaned_dict[clean_key] = pst_time.strftime('%B %d at %H:%M')
                    else:
                        cleaned_dict[clean_key] = v
                except ValueError:
                    cleaned_dict[clean_key] = v
            else:
                cleaned_dict[clean_key] = clean_response_data(v) if isinstance(v, (dict, list)) else v
        return cleaned_dict
    elif isinstance(data, list):
        return [clean_response_data(item) for item in data]
    else:
        return data