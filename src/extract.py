import json
import logging
from datetime import datetime
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from settings import AWS_PROFILE, AWS_REGION


logger = logging.getLogger(__name__)


def extract_data():
    """
    Extract monthly AWS cost data grouped by AWS service.

    The audit period covers June 1, 2026 through August 31, 2026.
    Cost Explorer uses an exclusive end date, so September 1, 2026
    is used to include all of August 31.

    Returns:
        dict: Raw Cost Explorer API response.

    Raises:
        ClientError: If AWS returns an API error.
        BotoCoreError: If a boto3-related error occurs.
    """
    try:
        session = boto3.Session(
            profile_name=AWS_PROFILE,
            region_name=AWS_REGION
        )

        cost_explorer = session.client("ce")

        logger.info("Connected to AWS Cost Explorer.")
        logger.info(
            "Extracting AWS cost data from "
            "2026-06-01 to 2026-08-31."
        )

        response = cost_explorer.get_cost_and_usage(
            TimePeriod={
                "Start": "2026-06-01",
                "End": "2026-09-01"
            },
            Granularity="MONTHLY",
            Metrics=[
                "UnblendedCost"
            ],
            GroupBy=[
                {
                    "Type": "DIMENSION",
                    "Key": "SERVICE"
                }
            ]
        )

        logger.info(
            "Cost data successfully extracted by AWS service."
        )

        return response

    except ClientError as error:
        logger.error(
            "AWS Cost Explorer API error: %s",
            error
        )
        raise

    except BotoCoreError as error:
        logger.error(
            "Boto3 error while extracting cost data: %s",
            error
        )
        raise


def save_raw_data(data):
    """
    Save the untouched Cost Explorer response as JSON.

    Args:
        data (dict): Raw Cost Explorer API response.

    Returns:
        Path: Path to the saved JSON file.

    Raises:
        OSError: If the file cannot be created or written.
    """
    try:
        project_root = Path(__file__).resolve().parent.parent
        raw_directory = project_root / "data" / "raw"

        raw_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        file_path = (
            raw_directory
            / f"cost_explorer_{timestamp}.json"
        )

        with file_path.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                indent=4
            )

        logger.info(
            "Raw Cost Explorer data saved to %s",
            file_path
        )

        return file_path

    except OSError as error:
        logger.error(
            "Failed to save raw cost data: %s",
            error
        )
        raise

