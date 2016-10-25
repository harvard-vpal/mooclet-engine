import requests
from django.conf import settings

class MoocletEngineModel:
    prefix = ''

    @classmethod
    def create(self, **kwargs):
        r = requests.post("{}/{}".format(settings.MOOCLET_URL_BASE, self.prefix), data=kwargs)
        return r.json()

    @classmethod
    def get(self, pk):
        r = requests.get("{}/{}/{}".format(settings.MOOCLET_URL_BASE, self.prefix, pk))
        return r.json()

    @classmethod
    def modify(self):
        pass


class Mooclet(MoocletEngineModel):

    prefix = 'mooclets'

    # define additional api method for mooclet

    @classmethod
    def get_version(self, pk, **kwargs):
        '''
        use policy to get version for this mooclet
        arguments: 
        '''
        r = requests.get("{}/{}/{}/{}".format(settings.MOOCLET_URL_BASE, self.prefix, pk, 'get_version'))
        return r.json()


class Version(MoocletEngineModel):
    prefix = 'versions'

class Variable(MoocletEngineModel):
    prefix = 'variables'

class Value(MoocletEngineModel):
    prefix = 'values'


