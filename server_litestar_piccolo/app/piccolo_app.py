"""Import all of the Tables in your app here, and register them withthe APP_CONFIG."""

from pathlib import Path

from piccolo.conf.apps import AppConfig, table_finder

from constants import BASE_PATH

APP_CONFIG = AppConfig(
    app_name="staffsec",
    migrations_folder_path=Path(BASE_PATH, "migrations"),
    table_classes=table_finder(
        modules=["app.tables.tables"],
        exclude_imported=True,
    ),
    migration_dependencies=[],
    commands=[],
)
