from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service

SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.delete.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
]

service = get_service("tagmanager", "v2", SCOPES)


class ContainerProvider(ResourceProvider):
    def create(self, props):
        account_path = f"accounts/{props['account_id']}"
        container = (
            service.accounts()
            .containers()
            .create(
                parent=account_path,
                body={"name": props["container_name"], "usage_context": ["web"]},
            )
            .execute()
        )
        return CreateResult(
            id_=props["account_id"],
            outs={"container_id": container["containerId"], **props, **container},
        )

    def update(self, id, _olds, props):
        container = (
            service.accounts()
            .containers()
            .update(
                path=_olds["path"],
                body={"name": props["container_name"], "usage_context": ["web"]},
            )
            .execute()
        )
        return UpdateResult(outs={**props, **container})

    def delete(self, props):
        service.accounts().containers().delete(path=props["path"]).execute()
