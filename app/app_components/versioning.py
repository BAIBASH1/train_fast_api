from fastapi_versioning import VersionedFastAPI


def init_versioned_fastapi(app):
    app = VersionedFastAPI(
        app,
        version_format="{major}",
        prefix_format="/v{major}",
        description="Greet users with a nice message",
    )
    return app
