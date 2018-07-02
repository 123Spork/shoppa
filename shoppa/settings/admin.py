import json

from flask import Response
from shoppa.core.exceptions import ObjectNotFound
from shoppa.core.http import crossdomain, parse_args, request_data
from shoppa.core.views import BaseAdminView
from shoppa.settings.models import get_settings_class


class AdminConfigSettingsUpdateView(BaseAdminView):
    """
        URI: /admin/settings-config/update
        POST: Update Config Settings
    """
    uri = '/admin/settings-config/update'

    @crossdomain(origin='*')
    #@requires_admin_login
    def post(self):
        try:
            args = parse_args(
                (
                    ('site_name', str, True),
                    ('contact_number', str, True),
                    ('email_address', str, True),
                    ('facebook_page_link', str, True),
                    ('twitter_page_link', str, True),
                    ('instagram_page_link', str, True),
                ),request_data())
        except Exception as e:
            return Response(status=400, response=json.dumps({
                'error_message': "Server received invalid arguments. Expecting site_name, contact_number, email_address\
                    facebook_page_link, twitter_page_link and instagram_page_link",
                'error_location': '/admin/settings-config/update POST'
            }))

        ConfigSettingsClass = get_settings_class()
        try:
            c_settings = ConfigSettingsClass.objects.get(
                settings_id="base"
            )
        except ObjectNotFound:
            c_settings = ConfigSettingsClass(
                settings_id="base",
                site_name=args['site_name'],
                contact_number=args['contact_number'],
                email_address=args['email_address'],
                facebook_page_link=args['facebook_page_link'],
                twitter_page_link=args['twitter_page_link'],
                instagram_page_link=args['instagram_page_link']
            )
            c_settings.save()
        else:
            c_settings.site_name=args['site_name'],
            c_settings.contact_number=args['contact_number'],
            c_settings.email_address=args['email_address'],
            c_settings.facebook_page_link=args['facebook_page_link'],
            c_settings.twitter_page_link=args['twitter_page_link'],
            c_settings.instagram_page_link=args['instagram_page_link']
            c_settings.save()

        return Response(status=200, response=json.dumps(
            {
                # 'session_id': self.user.session_id,
                'settings': c_settings.to_dict()
            }))


class AdminConfigSettingsFetchView(BaseAdminView):
    """
        URI: /admin/settings-config/fetch
        POST: Fetch all config settings.
    """
    uri = '/admin/settings-config/fetch'

    @crossdomain(origin='*')
    #@requires_admin_login
    def get(self):
        ConfigSettingsClass = get_settings_class()
        try:
            c_settings = ConfigSettingsClass.objects.get(
                settings_id="base"
            )
        except ObjectNotFound:
            c_settings = ConfigSettingsClass(
                settings_id="base",
                site_name="",
                contact_number="",
                email_address="",
                facebook_page_link="",
                twitter_page_link="",
                instagram_page_link=""
            )

        return Response(status=200, response=json.dumps(
            {
                # 'session_id': self.user.session_id,
                'settings': c_settings.to_dict()
            }))