import logging

from botocore.exceptions import ClientError

from src.exceptions import FormatDataError
from src.exceptions import GetDataError
from src.exceptions import ObfuscationError
from src.utils.format_data import format_data
from src.utils.get_data import get_data
from src.utils.get_file_type import get_file_type
from src.utils.obfuscate_fields import obfuscate_fields


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def obfuscator(event):
    """
    Obfuscates personally identifiable information (PII) fields in a data file.

    Args:
        event (dict): A dictionary containing the following keys:
            file_to_obfuscate (str): The S3 URI of the file to be obfuscated.
            pii_fields (list): A list of strings of PII fields for obfuscation.

    Returns:
        str: The obfuscated data in the same format as the input file.

    Raises:
        AttributeError: If there is an error extracting the file type.
        GetDataError: If there is an error loading the data from the file.
        ClientError: If there is an AWS error loading the data.
        TypeError: If there the file type is not supported.
        ObfuscationError: If there is an error obfuscating the PII fields.
        FormatDataError: If there is an error formatting the obfuscated data.
        Exception (critical): If an unexpected error occurs.
    """
    try:
        file_path = event["file_to_obfuscate"]
        fields_to_obfuscate = event["pii_fields"]
        file_type = get_file_type(file_path)

        data = get_data(file_path, file_type)
        obfuscated_data = obfuscate_fields(data, fields_to_obfuscate)
        formatted_data = format_data(obfuscated_data, file_type)

        return formatted_data

    except AttributeError as e:
        logger.error(f"Error extracting file type: {e}", exc_info=True)
        raise e
    except (GetDataError, ClientError, TypeError) as e:
        logger.error(
            f"Error loading data from {file_path}: {e}", exc_info=True
        )
        raise e
    except ObfuscationError as e:
        logger.error(f"Error obfuscating fields: {e}", exc_info=True)
        raise e
    except FormatDataError as e:
        logger.error(f"Error formatting obfuscated data: {e}", exc_info=True)
        raise e
    except Exception as e:
        logger.critical("An unexpected error occurred", exc_info=True)
        raise e
