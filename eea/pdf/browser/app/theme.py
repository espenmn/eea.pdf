""" Browser views
"""
import json

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from eea.pdf.cache.cache import updateContext
from eea.downloads.interfaces import IStorage
import transaction

class Theme(BrowserView):
    """ Custom view controller
    """
    @property
    def types(self):
        """ Types
        """
        field = self.context.getField('types')
        types = field.getAccessor(self.context)
        return types()

    def flushPDFsCache(self):
        """ Flush all PDFs cache for this theme
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        for brain in catalog.searchResults(portal_type=self.types):
            obj = brain.getObject()
            storage = IStorage(obj).of('pdf')
            storage_pdf_obj = obj.unrestrictedTraverse(
                storage.absolute_url(True), None)
            #change modification time only if
            #the object has a PDF generated in downloads
            if storage_pdf_obj is not None:
                updateContext(obj)
        return json.dumps('ok')


class ThemeUtils(BrowserView):
    """ Custom view controller
    """

    def __init__(self, context, request):
        super(ThemeUtils, self).__init__(context, request)
        self.context = context
        self.request = request

    def __call__(self, portal_type, theme, comment=None, depth=1):
        """
        :param portal_type: Portal Types to look for when changing theme
        :type portal_type: str
        :param theme: Theme id we want to apply for the given portal_type
        :type theme: str
        :param comment: Comment added in history comment
        :type comment: str
        :param depth: How far do we want to look for the content from context
        :type depth: int
        :return: List of object that had their local theme set
        :rtype: str
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())
        search_query = {
            'Language': 'all',
            'portal_type': portal_type,
            'path': {'query': folder_path, 'depth': int(depth)}

        }
        objs_path = []
        count = 0
        results = catalog(search_query)
        first_result = results[0].getObject()
        pr = getToolByName(self.context, 'portal_repository')
        isVersionable = pr.isVersionable(first_result)
        should_version = False
        if pr.supportsPolicy(first_result, 'at_edit_autoversion') \
                and isVersionable:
            should_version = True
        for brain in results:
            obj = brain.getObject()
            obj_theme = obj.getField('pdfTheme')
            obj_theme.set(obj, theme)
            objs_path.append(obj.absolute_url())
            if should_version:
                cmnt = "Migration script version which set Pdf theme to %s." \
                          % theme
                cmnt = cmnt + ' ' + comment if comment else cmnt
                pr.save(obj, comment=cmnt)
            count += 1
            if count % 50 == 0:
                transaction.savepoint(optimistic=True)

        return 'Done setting %s theme for \n %s' % (theme, "\n".join(objs_path))
