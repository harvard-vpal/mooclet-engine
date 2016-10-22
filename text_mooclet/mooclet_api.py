import requests
from django.conf import settings


def url_base(prefix):
    r = "{}/{}".format(settings.MOOCLET_URL_BASE, prefix)


class Mooclet:

    prefix = 'mooclets'
    url_base = "{}/{}".format(settings.MOOCLET_URL_BASE, prefix)

    @staticmethod
    def create(**kwargs):
        '''
        create mooclet
        arguments: name, policy
        '''
        r = requests.post(Mooclet.url_base, data=kwargs)
        return r.json()

    @staticmethod
    def get(mooclet_id):
        '''
        get mooclet data
        '''
        r = requests.get("{}/{}".format(Mooclet.url_base, mooclet_id))
        return r.json()

    def modify():
        pass

    def get_version(**kwargs):
        '''
        use policy to get version for this mooclet
        arguments: 
        '''
        r = requests.get("{}/{}".format(Mooclet.url_base, mooclet_id))
        return r.json()


class Version:

    prefix = 'version'
    url_base = "{}/{}".format(settings.MOOCLET_URL_BASE, prefix)

    def get(version_id):
        '''
        get version data
        '''
        r = requests.get("{}/{}".format(Version.url_base, version_id))
        return r.json()

    @staticmethod
    def create(**kwargs):
        '''
        create version
        arguments: mooclet, name
        '''
        r = requests.post(Version.url_base, data=kwargs)
        return r.json()

    def modify():
        pass
