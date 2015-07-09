from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from models import *

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

import json


class BaseView:
    def __init__(self,context,request):
        self.request = request
        self.context = context
        
        
    
class BasicViews(BaseView):
    def __init__(self,context,request):
        BaseView.__init__(self,context,request)
    
    @view_config(renderer='pyramidapp:templates/home.mak',
        route_name="home")
    def home(self):
        
        return {
            }
