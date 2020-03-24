from pulumi.dynamic import Resource
from pulumi import Input, Output
from .container_provider import ContainerProvider
from ..service import get_key_file_location


class ContainerArgs(object):
    account_id: Input[str]
    container_name: Input[str]

    def __init__(
        self, account_id, container_name,
    ):
        self.account_id = account_id
        self.container_name = container_name


class Container(Resource):
    container_id: Output[str]
    path: Output[str]
    gtm_tag: Output[str]
    gtm_tag_noscript: Output[str]


    def __init__(self, name, args: ContainerArgs, opts=None):
        full_args = {
            "container_id": None,
            "path": None,
            "key_location": get_key_file_location(),
            "gtm_tag_noscript": None,
            "gtm_tag": None,
            **vars(args),
        }
        super().__init__(ContainerProvider(), name, full_args, opts)
