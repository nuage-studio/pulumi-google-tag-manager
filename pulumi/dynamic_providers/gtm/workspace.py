from pulumi.dynamic import Resource
from pulumi import Input, Output
from .workspace_provider import WorkspaceProvider
from ..service import get_key_file_location


class WorkspaceArgs(object):
    container_path: Input[str]
    workspace_name: Input[str]

    def __init__(
        self, container_path, workspace_name,
    ):
        self.container_path = container_path
        self.workspace_name = workspace_name


class Workspace(Resource):
    workspace_id: Output[str]
    path: Output[str]

    def __init__(self, name, args: WorkspaceArgs, opts=None):
        full_args = {
            "workspace_id": None,
            "path": None,
            "key_location": get_key_file_location(),
            **vars(args),
        }
        super().__init__(WorkspaceProvider(), name, full_args, opts)
