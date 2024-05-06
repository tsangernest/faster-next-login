from fastapi.security import OpenIdConnect


class OIDCSettings:
    base_url: str = "http://localhost:8000/realms"

    client_id: str = "fastapi"
    client_secret: str = "i19tV496HQLGQObmRCY47dId9aZEL0YN"

    oidc_realm: str = "master"


    wk_url: str = f"{base_url}/{oidc_realm}/.well-known/openid-configuration"
    az_code_url: str = f"{base_url}/{oidc_realm}/protocol/openid-connect"


oidc_scheme: OpenIdConnect = OpenIdConnect(
    openIdConnectUrl=OIDCSettings.wk_url,
    auto_error=False,
)



