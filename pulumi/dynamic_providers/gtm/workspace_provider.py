from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service, get_key_file_location


SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.delete.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
]

service = get_service("tagmanager", "v2", SCOPES)


class WorkspaceProvider(ResourceProvider):
    def create(self, props):
        workspace = (
            service.accounts()
            .containers()
            .workspaces()
            .create(
                parent=props["container_path"], body={"name": props["workspace_name"]}
            )
            .execute()
        )

        return CreateResult(id_=props["container_path"], outs={**props, **workspace})

    def update(self, id, _olds, props):
        workspace = (
            service.accounts()
            .containers()
            .workspaces()
            .update(path=_olds["path"], body={"name": props["workspace_name"]})
            .execute()
        )
        return UpdateResult(outs={**props, **workspace})

    def delete(self, id, props):
        service.accounts().containers().workspaces().delete(
            path=props["path"]
        ).execute()

