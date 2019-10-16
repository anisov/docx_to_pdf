import os
from aiologger import Logger
from aiologger.handlers.files import AsyncFileHandler
from aiologger.formatters.base import Formatter


# In version 0.4.0 AsyncFileHandler don't have formatter in __init__().
class AsyncFileHandlerFormatter(AsyncFileHandler):
    def __init__(
            self,
            formatter: Formatter = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.formatter = formatter


formatter = Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = Logger.with_default_handlers(
    name='converter',
    formatter=formatter
)

logger.add_handler(
    AsyncFileHandlerFormatter(
        filename=os.path.join(os.path.dirname(__file__), f'logs/{logger.name}.txt'),
        formatter=formatter
    )
)
