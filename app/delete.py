from app.utils.decorators import something_might_go_wrong, no_args
from app.utils.responses import success


@something_might_go_wrong
@no_args
def main():
    return success("Hello World!")
