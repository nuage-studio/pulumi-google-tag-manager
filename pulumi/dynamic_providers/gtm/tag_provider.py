from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service, get_key_file_location


SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.delete.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
]

service = get_service("tagmanager", "v2", SCOPES)


class TagProvider(ResourceProvider):
    def create(self, props):
        tag_body = {
            "name": props["tag_name"],
            "type": "ua",
            "parameter": [
                {
                    "key": "trackingId",
                    "type": "template",
                    "value": str(props["tracking_id"]),
                }
            ],
        }

        tag = (
            service.accounts()
            .containers()
            .workspaces()
            .tags()
            .create(parent=props["workspace_path"], body=tag_body)
            .execute()
        )

        return CreateResult(id_=props["workspace_id"], outs={**props, **tag})

    def update(self, id, _olds, props):
        tag_body = {
            "name": props["tag_name"],
            "type": "ua",
            "parameter": [
                {
                    "key": "trackingId",
                    "type": "template",
                    "value": str(props["tracking_id"]),
                }
            ],
        }
        tag = (
            service.accounts()
            .containers()
            .workspaces()
            .tags()
            .update(path=_olds["path"], body=tag_body)
            .execute()
        )

        return UpdateResult(outs={**props, **tag})

    def delete(self, id, props):
        service.accounts().containers().workspaces().tags().delete(
            path=props["path"]
        ).execute()

