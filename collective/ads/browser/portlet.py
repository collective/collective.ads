from zope.interface import implements
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form

from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from Products.CMFPlone import PloneMessageFactory as _

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Acquisition import aq_inner, aq_base, aq_parent
from Products.CMFPlone.interfaces import INonStructuralFolder 

try:
  from Products.CMFDynamicViewFTI.interfaces import IBrowserDefault
except:
  from Products.CMFPlone.interfaces import IBrowserDefault

import random
from DateTime import DateTime
import math 


#from zope.schema.vocabulary import SimpleVocabulary
from Products.Archetypes.public import DisplayList

class IAdsPortlet(IPortletDataProvider):
    """A portlet which can render a Ads
    """
   
    name = schema.TextLine(
           title=_(u"label_title", default=u"Title"),
           description=_(u"help_title",
                         default=u"The title"),
           default=u"",
           required=False)    
    
    count = schema.Int(title=_(u'Number of items to display'),
           description=_(u'How many items to list.'),
           required=True,
           default=5)
    
    state = schema.Tuple(title=_(u"Workflow state"),
           description=_(u"Items in which workflow state to show."),
           default=('published', ),
           required=True,
           value_type=schema.Choice(
                                    vocabulary="plone.app.vocabularies.WorkflowStates")
           )

    keywords_filter = schema.Tuple(
           title=_(u'portlet_label_keywords_filter',
                   default=u'Keywords Filter'),
           description=_(u'portlet_help_keywords_filter',
                         default=u'Select which teasers with specific keywords '
                                 u'should be shown. Select none to order to show '
                                 u'any teasers.'),
           default=None,
           required=False,
           value_type=schema.Choice(
               vocabulary="plone.app.vocabularies.Keywords"),
           )

        
from Products.CMFPlone.utils import log
    
class Assignment(base.Assignment):
    implements(IAdsPortlet)
    
    keywords_filter = None
    
    def __init__(self,name=u"", count=5, state=('published', ), keywords_filter=None):
        self.count = count
        self.state = state
        self.name= name
        self.keywords_filter = keywords_filter

    title = _(u'Ads', default=u'Ads')


class Renderer(base.Renderer):

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
       
    def title(self):
        return self.data.name or ''      
        
    def update(self):
        pass

    #memoize @
    def getFilteredBanners(self):
   
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        state = self.data.state
        count = self.data.count
        
        query = {}
        query['portal_type']='Banner'
        query['effectiveRange']=DateTime()
        query['review_state']=state
        
        if self.data.keywords_filter:
            query['Subject'] = self.data.keywords_filter
            
        banners = catalog(**query)
        bannerPool = []

        for banner in banners:
            percentage = banner.getPercent
          
            #XXX make better check here /100 is not good.
            # check if not 0
            if percentage!=0:
                percentage = int(math.ceil(percentage/100));
                # dont show banner if all clicks were used or the banner is outdated
                if banner.getClicksUsed < banner.getClicks:
                    for i in range(percentage):
                        bannerPool.append(banner)
        
        # get count and randomize
        if (len(bannerPool)>count):
            bannerPool = random.sample(bannerPool,count);
        
        return bannerPool;


    render = ViewPageTemplateFile('templates/adsportlet.pt')

#class AddForm(base.NullAddForm):
class AddForm(base.AddForm):
    form_fields = form.Fields(IAdsPortlet)
    label = _(u"Add Ads Portlet")
    description = _(u"Displays banners in this plone site ")
    
    def create(self, data):
        return Assignment(name=data.get('name',''),count=data.get('count', 5), keywords_filter=data.get('keywords_filter',''), state=data.get('state', ('published',)))
    
class EditForm(base.EditForm):
    
    form_fields = form.Fields(IAdsPortlet)
    label = _(u"Edit Ads Portlet")
    description = _(u"Displays banners in this Plone site")
    
    