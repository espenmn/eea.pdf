""" EEA Relations Content Type
"""
#from zope.interface import implementer
#from Products.Archetypes import atapi
#from plone.app.blob.field import ImageField
#from archetypes.referencebrowserwidget import ReferenceBrowserWidget

#from Products.ATContentTypes.content.folder import ATFolder

from eea.pdf.content.interfaces import IPDFTheme
from eea.pdf.config import EEAMessageFactory as _

 
from zope import schema
from zope.interface import Interface
from zope.interface import implements
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides
from zope.i18nmessageid import MessageFactory

#_ = MessageFactory('eea.pdf')



class IIPDFBehavior(form.Schema):
    """ A field for icons"""
    
    cover = schema.TextLine(
        default='pdf.cover',
        description=_(
                u"A page template to be used for PDF Cover. "
                u"Leave empty to disable it."
            )
        )

    disclaimer = schema.TextLine(
    	default='pdf.disclaimer',
            description=_(
                u"A page template to be used for PDF Disclaimer, "
                u"the first page after PDF cover. "
                u"Leave empty to disable it."
            )
        )
    
    body = schema.TextLine(        
        default='pdf.body',
        description=_(
                u"A page template to be used for PDF Body. "
                u"Leave empty to disable it."
            )
    )
    backcover = schema.TextLine(
        default='pdf.cover.back',
        description=_(
                u"A page template to be used for PDF Back Cover. "
                u"Leave empty to disable it."
            )
        )
        
    header = schema.TextLine(        
        default='pdf.header',
        description=_(
                u"A page template to be used for PDF Header. "
                u"Leave empty to disable it."
            )
        )
    footer = schema.TextLine(        
        default='pdf.footer',
        description=_(
                u"A page template to be used for PDF Footer. "
                u"Leave empty to disable it."
            )
        )

    staticFooterAndHeader = schema.Bool(        
        default=False,
        description=_(u"Enable static footer and header html pages. "
                         u"Footer and header templates are evaluated once"
                         u" and then served for every pdf page."
            )
       )
       
    schema.TextLine('toc',
        default='pdf.toc',
        description=_(
                u"An XSL page template to be used for PDF Table of contents. "
                u"Leave empty to disable it."
            )
        )


    toclinks = schema.Bool( 
       default=False,
       description=_(u"Enable table of contents links")
    )

    javascript = schema.Bool(
       default=True,
       description=_(u"Enable or disable javascript")
    )
    
    javascriptdelay = schema.Int(
       default=60,
       description=_(u"Wait some seconds for javascript to finish")
       
    )
    
    timeout = schema.Int(
        default=3600,
        description=_(
                u"Abort PDF export after specified number of seconds. "
                u"Use zero to disable it."
            )
        )
        
    async = schema.Bool(        
        default=True,
        description=_(
                u"Generate PDF asynchronously and send an email to the user "
                u"when it's done."
            )
        )

    offset = schema.Int(       
        default=0,
        description=_(
                u"Page numbering offset within PDF Body."
            )
        )
    
    maxdepth = schema.Int(        
        default=1,
        description=_(
                u"Maximum depth to recursively include children items "
                u"while generating PDF for collection "
                u"or folderish content-types."
            )
        )
    
    maxbreadth = schema.Int(
        default=100,
        description=_(
                u"Maximum breadth to include children items "
                u"while generating PDF for collection "
                u"or folderish content-types where object is collection or "
                u"folderish."
            )
        )
    maxitems = schema.Int(        
        default=1000,
        description=_(
                u"Total maximum children items to be included "
                u"while generating PDF for collection "
                u"or folderish content-types."
            )
        )
    
    image = schema.Image(
        description=_(u"Upload a preview image for this theme")
        )



alsoProvides(IPDFBehavior, IFormFieldProvider)


