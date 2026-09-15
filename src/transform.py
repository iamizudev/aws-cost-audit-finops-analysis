import json
import logging
from pathlib import Path

import pandas as pd


logger = logging.getLogger(__name__)


REQUIRED_COLUMNS = [
    "start_date",
    "end_date",
    "service",
    "cost",
    "currency",
    "estimated",
]


def find_latest_raw_file():
    """
    Find the most recently created raw Cost Explorer JSON file.

    Returns:
        Path: Path to the latest raw JSON file.

    Raises:
        FileNotFoundError: If no JSON files are found.
        OSError: If the raw data directory cannot be accessed.
    """
    try:
        project_root = Path(__file__).resolve().parent.parent
        raw_directory = project_root / "data" / "raw"

        raw_files = list(raw_directory.glob("*.json"))

        if not raw_files:
            raise FileNotFoundError(
                f"No raw JSON files found in {raw_directory}."
            )

        latest_file = max(
            raw_files,
            key=lambda file: file.stat().st_mtime
        )

        logger.info("Latest raw file selected: %s", latest_file)

        return latest_file

    except OSError as error:
        logger.error(
            "Unable to access raw data directory: %s",
            error
        )
        raise


def load_raw_data(file_path):
    """
    Load the raw Cost Explorer JSON file.

    Args:
        file_path (Path): Path to the raw JSON file.

    Returns:
        dict: Raw Cost Explorer response.

    Raises:
        json.JSONDecodeError: If the file contains invalid JSON.
        OSError: If the file cannot be read.
    """
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        logger.info("Raw JSON loaded successfully.")

        return data

    except json.JSONDecodeError as error:
        logger.error(
            "Invalid JSON in raw file %s: %s",
            file_path,
            error
        )
        raise

    except OSError as error:
        logger.error(
            "Unable to read raw file %s: %s",
            file_path,
            error
        )
        raise


def extract_results(raw_data):
    """
    Extract monthly service-level records from Cost Explorer data.

    Args:
        raw_data (dict): Raw Cost Explorer response.

    Returns:
        list: Flattened service-level cost records.

    Raises:
        ValueError: If the expected AWS response structure is missing.
    """
    if "ResultsByTime" not in raw_data:
        raise ValueError(
            "Invalid Cost Explorer response: "
            "'ResultsByTime' is missing."
        )

    results = raw_data["ResultsByTime"]

    if not isinstance(results, list):
        raise ValueError(
            "'ResultsByTime' must be a list."
        )

    if not results:
        raise ValueError(
            "Cost Explorer returned no results."
        )

    records = []

    for result in results:
        time_period = result.get("TimePeriod", {})
        estimated = result.get("Estimated")

        start_date = time_period.get("Start")
        end_date = time_period.get("End")

        groups = result.get("Groups", [])

        for group in groups:
            keys = group.get("Keys", [])
            metrics = group.get("Metrics", {})
            cost_data = metrics.get("UnblendedCost", {})

            service = keys[0] if keys else None

            records.append(
                {
                    "start_date": start_date,
                    "end_date": end_date,
                    "service": service,
                    "cost": cost_data.get("Amount"),
                    "currency": cost_data.get("Unit"),
                    "estimated": estimated,
                }
            )

    if not records:
        raise ValueError(
            "No service-level cost records were found."
        )

    logger.info(
        "Extracted %d service-level records.",
        len(records)
    )

    return records


def transform_results(records):
    """
    Convert service-level records into a pandas DataFrame.

    Args:
        records (list): Service-level cost records.

    Returns:
        pandas.DataFrame: Structured cost dataset.
    """
    dataframe = pd.DataFrame(records)

    dataframe["start_date"] = pd.to_datetime(
        dataframe["start_date"],
        errors="coerce"
    )

    dataframe["end_date"] = pd.to_datetime(
        dataframe["end_date"],
        errors="coerce"
    )

    dataframe["cost"] = pd.to_numeric(
        dataframe["cost"],
        errors="coerce"
    )

    logger.info(
        "Transformed %d records into a DataFrame.",
        len(dataframe)
    )

    return dataframe


def validate_data(dataframe):
    """
    Validate the service-level cost dataset.

    Validation checks include required columns, missing values,
    duplicates, dates, costs, currency, and estimated status.

    Args:
        dataframe (pandas.DataFrame): Transformed cost data.

    Returns:
        pandas.DataFrame: Validated cost dataset.

    Raises:
        ValueError: If critical data-quality issues are found.
    """
    validation_errors = []

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Missing values
    missing_values = dataframe[REQUIRED_COLUMNS].isnull().sum()

    missing_fields = {
        column: int(count)
        for column, count in missing_values.items()
        if count > 0
    }

    if missing_fields:
        validation_errors.append(
            f"Missing values found: {missing_fields}"
        )

    # Duplicate records
    duplicate_count = int(dataframe.duplicated().sum())

    if duplicate_count > 0:
        logger.warning(
            "Found %d duplicate records. Removing duplicates.",
            duplicate_count
        )

        dataframe = dataframe.drop_duplicates().copy()

    # Invalid dates
    invalid_dates = dataframe[
        dataframe["start_date"].isna()
        | dataframe["end_date"].isna()
    ]

    if not invalid_dates.empty:
        validation_errors.append(
            f"{len(invalid_dates)} records contain invalid dates."
        )

    # Invalid time periods
    invalid_periods = dataframe[
        dataframe["start_date"] >= dataframe["end_date"]
    ]

    if not invalid_periods.empty:
        validation_errors.append(
            f"{len(invalid_periods)} records have invalid time periods."
        )

    # Invalid cost values
    invalid_costs = dataframe[
        dataframe["cost"].isna()
    ]

    if not invalid_costs.empty:
        validation_errors.append(
            f"{len(invalid_costs)} records contain invalid cost values."
        )

    # Negative costs
    negative_costs = dataframe[
        dataframe["cost"] < 0
    ]

    if not negative_costs.empty:
        validation_errors.append(
            f"{len(negative_costs)} records contain negative costs."
        )

    # Service names
    invalid_services = dataframe[
        dataframe["service"].isna()
        | (dataframe["service"].astype(str).str.strip() == "")
    ]

    if not invalid_services.empty:
        validation_errors.append(
            f"{len(invalid_services)} records have missing service names."
        )

    # Currency
    invalid_currency = dataframe[
        dataframe["currency"] != "USD"
    ]

    if not invalid_currency.empty:
        validation_errors.append(
            f"{len(invalid_currency)} records contain unexpected currency."
        )

    # Estimated flag
    invalid_estimated = dataframe[
        ~dataframe["estimated"].isin([True, False])
    ]

    if not invalid_estimated.empty:
        validation_errors.append(
            f"{len(invalid_estimated)} records have invalid "
            "estimated values."
        )

    # Sort chronologically
    dataframe = dataframe.sort_values(
        by=["start_date", "service"]
    ).reset_index(drop=True)

    if validation_errors:
        logger.error(
            "Data validation failed with %d issue(s).",
            len(validation_errors)
        )

        for error in validation_errors:
            logger.error("Validation issue: %s", error)

        raise ValueError(
            "Critical data-quality issues were found. "
            "Review the validation errors before continuing."
        )

    logger.info("Data validation passed successfully.")
    logger.info(
        "Records after validation: %d",
        len(dataframe)
    )
    logger.info(
        "Duplicate records removed: %d",
        duplicate_count
    )

    return dataframe


def transform_data():
    """
    Run the complete transformation and validation process.

    Returns:
        pandas.DataFrame: Clean and validated service-level dataset.
    """
    raw_file = find_latest_raw_file()
    raw_data = load_raw_data(raw_file)

    records = extract_results(raw_data)
    dataframe = transform_results(records)
    dataframe = validate_data(dataframe)

    return dataframe


