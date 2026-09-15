import logging

from extract import extract_data, save_raw_data
from transform import transform_data
from load import load_data


logger = logging.getLogger(__name__)


def main():
    """Run the complete AWS cost ETL pipeline."""

    logger.info("Starting AWS Cost Audit ETL pipeline.")

    try:
        # 1. Extract
        logger.info("Starting extraction.")
        raw_data = extract_data()

        # 2. Save raw data
        logger.info("Saving raw Cost Explorer response.")
        save_raw_data(raw_data)

        # 3. Transform and validate
        logger.info("Starting transformation and validation.")
        dataframe = transform_data()

        # 4. Load processed data
        logger.info("Loading validated data.")
        output_file = load_data(dataframe)

        logger.info(
            "AWS Cost Audit ETL pipeline completed successfully."
        )
        logger.info("Processed file: %s", output_file)

    except Exception as error:
        logger.error(
            "AWS Cost Audit ETL pipeline failed: %s",
            error
        )
        raise


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    main()