from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service, get_key_file_location


SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.delete.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
]


class GAPageviewTagProvider(ResourceProvider):
    def create(self, props):
        service = get_service("tagmanager", "v2", SCOPES, props['key_location'])
        tag_body = self._get_tag_body(props)

        tag = (
            service.accounts()
            .containers()
            .workspaces()
            .tags()
            .create(parent=props["workspace_path"], body=tag_body)
            .execute()
        )

        return CreateResult(id_=props["workspace_path"], outs={**props, **tag})

    def update(self, id, _olds, props):
        service = get_service("tagmanager", "v2", SCOPES, props['key_location'])
        tag_body = self._get_tag_body(props)
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
        service = get_service("tagmanager", "v1", SCOPES, props['key_location'])
        service.accounts().containers().tags().delete(
            accountId=props["accountId"],
            containerId=props["containerId"],
            tagId=props["tagId"],
        )
    
    def _get_tag_body(self, props):

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
            "firingTriggerId": props["firing_trigger_id"]
        }

        return tag_body