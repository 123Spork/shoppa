from shoppa.core.managers import CoreSQLDBModelManager


def get_settings_manager(model):

    class ConfigSettingsManager(CoreSQLDBModelManager):
        Model = model
    return ConfigSettingsManager