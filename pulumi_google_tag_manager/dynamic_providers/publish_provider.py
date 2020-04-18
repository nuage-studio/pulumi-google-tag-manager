from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service, get_key_file_location


SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.delete.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
    "https://www.googleapis.com/auth/tagmanager.publish"
]


class PublishProvider(ResourceProvider):

    def create(self, props):
        service = get_service("tagmanager", "v2", SCOPES, props['key_location'])

        create_version = (
            service.accounts()
            .containers()
            .workspaces()
            .create_version(path=props["workspace_path"])
            .execute()
        )

        publish_result = (
            service.accounts()
            .containers()
            .versions()
            .publish(path=create_version["containerVersion"]["path"])
            .execute()
        )

        return CreateResult(id_=props["workspace_path"], outs={
            **props,
            **create_version,
            "container_version_id": create_version["containerVersion"]["containerVersionId"],
            "container_version_path": create_version["containerVersion"]["path"]
        })
