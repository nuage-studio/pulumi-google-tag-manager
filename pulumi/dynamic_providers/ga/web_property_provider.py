from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult
from ..service import get_service

SCOPES = ["https://www.googleapis.com/auth/analytics.edit"]

service = get_service("analytics", "v3", SCOPES)


class WebPropertyProvider(ResourceProvider):
    def create(self, props):
        accounts = service.management().accounts().list(fields="items").execute()

        web_property = (
            service.management()
            .webproperties()
            .insert(
                accountId=account,
                fields="id",
                body={"websiteUrl": props["site_url"], "name": props["site_name"]},
            )
            .execute()
        )

        return CreateResult(
            id_=props["account_id"], outs={"tracking_id": web_property["id"], **props},
        )

    def update(self, id, _olds, props):
        web_property = (
            service.management()
            .webproperties()
            .update(
                accountId=props["account_id"],
                webPropertyId=_olds["tracking_id"],
                body={"websiteUrl": props["site_url"], "name": props["site_url"]},
            )
            .execute()
        )

        return UpdateResult(outs={"tracking_id": web_property["id"], **props})

    def delete(self, props):
        service.management().webproperties().update(
            accountId=props["account_id"], webPropertyId=props["tracking_id"]
        )
