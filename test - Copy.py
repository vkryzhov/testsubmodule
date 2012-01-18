111
'''
    Getting the C2DM Token.
'''
import os
import sys
import datetime
from local_constants import *
from service.cwn.management import console_settings
from settings import *
from service.cwn.models import *
from django.core.management.base import BaseCommand, CommandError
import urllib, urllib2, codecs

class Command(BaseCommand):

    def handle(self, *args, **options):
        # Build payload
        values = {'accountType' : C2DM_TOKEN_ACCOUNT_TYPE,
                  'Email' : C2DM_TOKEN_EMAIL,
                  'Passwd' : C2DM_TOKEN_PASSWORD, 
                  'source' : C2DM_TOKEN_SOURCE, 
                  'service' : C2DM_TOKEN_SERVICE}

        try:
            # Build request
            data = urllib.urlencode(values)
            request = urllib2.Request(C2DM_TOKEN_URL, data)
            
            # Post request
            response = urllib2.urlopen(request)
            responseAsString = response.read()
            
            # Format response
            responseAsList = responseAsString.split('\n')
            
            # Get Auth part of response
#            print responseAsList[2].split('=')[1]
            token = responseAsList[2].split('=')[1]
            
            if token:
                C2DMInfo.objects.filter(active = True).update(active=False, updated=datetime.datetime.utcnow())
                new_c2dminfo = C2DMInfo(
                    token = token,
                    active = True)
                new_c2dminfo.save()
                
                logging.info('New C2DM token saved.')
            else:
                # TODO: add inform admin about this error
                logging.info('Get the new C2DM token failed.')

        except Exception,e:
            # TODO: add inform admin about this error
#            print 'Getting new C2DM token. %s'  %e
            logging.exception( 'Getting new C2DM token. %s'  %e)
