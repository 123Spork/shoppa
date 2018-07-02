import logging
from sqlalchemy import String, Column

from shoppa.core.models import BaseSQLModel
from shoppa.settings.managers import get_settings_manager

log = logging.getLogger(__name__)


def get_settings_class():
    table_name = "{0}".format("site_settings")

    if table_name in BaseSQLModel.registry:
        return BaseSQLModel.registry[table_name]
    else:
        class ConfigSettings(BaseSQLModel):
            __tablename__ = table_name
            __table_args__ = {'useexisting': True}

            settings_id = Column(String(100), primary_key=True)
            site_name = Column(String(200))
            contact_number = Column(String(200))
            email_address = Column(String(200))
            facebook_page_link = Column(String(200))
            twitter_page_link = Column(String(200))
            instagram_page_link = Column(String(200))

        ConfigSettings.objects = get_settings_manager(ConfigSettings)()
        return ConfigSettings