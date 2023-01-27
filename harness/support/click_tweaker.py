""" click tweaker.  Prevent click from doing a sys.exit(2) """


class CLIExitException(Exception):
    def __init__(self, code: int) -> None:
        self.code = code
        super().__init__(self)
def no_click_exit(_self, code=0):
    raise CLIExitException(code)


# This import has to occur here
import click

click.core.Context.exit = no_click_exit
