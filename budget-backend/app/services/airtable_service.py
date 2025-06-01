import pytz

from app.core.logger import LOG
from app.core.constants import AIRTABLE_ACCESS_TOKEN, AIRTABLE_ACCOUNTS, AIRTABLE_TRANSACTIONS, AIRTABLE_DB_ID

from pyairtable import Api as pyairtableapiclient
from datetime import datetime
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
        format_dates_for_display = request_type == "transactions"
        clean_data = clean_response_data(response, format_dates_for_display)
        
        return clean_data
    except KeyError:
        raise ValueError(f"Invalid request type: {request_type}. Valid types are: {list(REQUEST_TYPES.keys())}")
    except Exception as e:
        raise Exception(f"Error making Airtable request: {str(e)}")

def clean_response_data(data: Union[Dict, List, Any], format_dates_for_display: bool = True) -> Union[Dict, List, Any]:
    """
    Clean and format the response data.
    If format_dates_for_display is True, convert to PST display format.
    If False, keep in ISO format for database storage.
    """
    if isinstance(data, dict):
        cleaned_dict = {}
        for k, v in data.items():
            clean_key = k.replace('*', '')
            if isinstance(v, str) and (k.lower().endswith('date') or k.lower().endswith('time')):
                try:
                    if 'T' in v and v.endswith('Z'):
                        date_obj = datetime.fromisoformat(v.replace('Z', '+00:00'))
                        
                        if format_dates_for_display:
                            # Convert to PST for display
                            pst = pytz.timezone('America/Los_Angeles')
                            pst_time = date_obj.astimezone(pst)
                            cleaned_dict[clean_key] = pst_time.strftime('%B %d at %H:%M')
                        else:
                            # Keep in ISO format for database
                            cleaned_dict[clean_key] = date_obj.isoformat()
                    else:
                        cleaned_dict[clean_key] = v
                except ValueError:
                    cleaned_dict[clean_key] = v
            else:
                cleaned_dict[clean_key] = clean_response_data(v, format_dates_for_display) if isinstance(v, (dict, list)) else v
        return cleaned_dict
    elif isinstance(data, list):
        return [clean_response_data(item, format_dates_for_display) for item in data]
    else:
        return data