import logging
import logging.config
from pathlib import Path

import yaml


BASE_DIR = Path(__file__).resolve().parent.parent
LOGGING_FILE = BASE_DIR / "logging.yaml"


try:
    with open(
        LOGGING_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError(
            "Configuração YAML inválida."
        )

    config["handlers"]["file"]["filename"] = str(
        BASE_DIR / "app.log"
    )

    logging.config.dictConfig(config)

except (
    OSError,
    yaml.YAMLError,
    KeyError,
    TypeError,
    ValueError,
) as erro:

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s - %(name)s - "
            "%(levelname)s - %(message)s"
        )
    )

    logger = logging.getLogger(
        "persistencia_api"
    )

    logger.error(
        "Erro ao carregar configuração de logging: %s",
        erro,
    )

else:
    logger = logging.getLogger(
        "persistencia_api"
    )


logger.info(
    "Sistema de logging inicializado."
)