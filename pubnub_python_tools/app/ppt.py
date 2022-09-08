# main_app wrapper
from .main_app import main
import asyncio
from ..logger.logging_config import get_logger
LOG = get_logger()  # Get logger if needed. Default: INFO

async def start_loop(self, *function_callback, run_forever=True):
    """
    function_callback: function(s) to be run until_complete.
    run_forever: keep the loop running forever.
    """
    loop = asyncio.get_event_loop()
    for function in function_callback:
        LOG.info("Loop will continue to run forever.")
        loop.run_until_complete(function)
    if run_forever:
        LOG.info("Loop will continue to run forever.")
        return loop.run_forever()

if "__name__" == "__main__":
    main()
