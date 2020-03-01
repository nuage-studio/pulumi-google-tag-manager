from pulumi.dynamic import Resource, ResourceProvider, CreateResult, UpdateResult
from pulumi import Input, Output
from .container_provider import ContainerProvider


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

    def __init__(self, name, args: ContainerArgs, opts=None):
        full_args = {"container_id": None, "path": None, **vars(args)}
        super().__init__(ContainerProvider(), name, full_args, opts)
