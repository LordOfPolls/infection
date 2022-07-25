import logging
import os

from src.bot import Bot

logging.basicConfig()
cls_log = logging.getLogger("naff")
log = logging.getLogger("main")
log.setLevel(logging.DEBUG)
cls_log.setLevel(logging.INFO)


def load_extensions():
    log.info("Loading Extensions...")

    for file in os.listdir("ext"):
        if file.endswith(".py") and not file.startswith("_"):
            log.info(f"Loading extension {file}")
            bot.load_extension(f"ext.{file[:-3]}")


if __name__ == "__main__":
    bot = Bot()
    load_extensions()
    log.info("Starting Client...")
    bot.start("OTk5NjA1ODY3NDc5NTY4Mzk0.G1Zk0N.aCCupK_iIzil-WD3ZDA7X0kxBUYG1sUGUp2zio")
