import logging
from datetime import datetime
from pathlib import Path




logger = logging.getLogger(__name__)


def load_data(dataframe):
    """
    Save the validated cost DataFrame as a CSV file.

    The processed CSV is stored separately from the raw JSON
    so that the original AWS Cost Explorer response remains unchanged.

    Args:
        dataframe (pandas.DataFrame): Validated cost dataset.

    Returns:
        Path: Path to the generated CSV file.

    Raises:
        ValueError: If the DataFrame is empty.
        OSError: If the CSV file cannot be created or written.
    """
    if dataframe.empty:
        raise ValueError(
            "Cannot load data because the DataFrame is empty."
        )

    try:
        project_root = Path(__file__).resolve().parent.parent
        processed_directory = project_root / "data" / "processed"

        processed_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        file_path = (
            processed_directory
            / f"clean_cost_data_{timestamp}.csv"
        )

        dataframe.to_csv(
            file_path,
            index=False
        )

        logger.info(
            "Processed CSV successfully saved to %s",
            file_path
        )

        logger.info(
            "Rows loaded: %d",
            len(dataframe)
        )

        return file_path

    except OSError as error:
        logger.error(
            "Failed to save processed cost data: %s",
            error
        )
        raise


