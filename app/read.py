from app.utils.decorators import something_might_go_wrong, no_args
from app.utils.responses import success


@something_might_go_wrong
@no_args
def single():
    return success("Hello World!")


@something_might_go_wrong
@no_args
def all_():
    return success("Hello World!")
