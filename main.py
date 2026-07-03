from cleaning.clean import run as clean
from validation.validate import run as validate
from warehouse.load import run as load

from utils.logger import logger


def main():

    logger.info("=" * 50)
    logger.info("🚀 AeroStream Pipeline Started")
    logger.info("=" * 50)

    clean()

    validate()

    load()

    logger.info("=" * 50)
    logger.info("🎉 AeroStream Pipeline Completed Successfully")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()