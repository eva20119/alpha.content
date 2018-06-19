# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.contenttypes.browser.folder import FolderView
from Acquisition import aq_inner
from email.mime.text import MIMEText
import json
import datetime
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
from zope.globalrequest import getRequest
from alpha.content.browser.configlet import IDict


class NewsItemView(BrowserView):
    
    def getNewsMonth(self, obj):
        return datetime.datetime.strptime(obj.CreationDate(), '%Y-%m-%dT%H:%M:%S+00:00').strftime('%B')

    def getNewsYear(self, obj):
        return datetime.datetime.strptime(obj.CreationDate(), '%Y-%m-%dT%H:%M:%S+00:00').strftime('%Y')

    def getNewsDay(self, obj):
        return datetime.datetime.strptime(obj.CreationDate(), '%Y-%m-%dT%H:%M:%S+00:00').strftime('%d')


class ProductView(BrowserView):
    def pdb(self):
        request = self.request
        alsoProvides(request, IDisableCSRFProtection)
        import pdb;pdb.set_trace()

    def getImg(self):
	request = self.request
	context = self.context
	imgBrain = api.content.find(context=context, portal_type='ProductImg', sort_limit=4)
	return imgBrain


class CoverView(BrowserView):
    template = ViewPageTemplateFile('templates/cover_view.pt')
    def __call__(self):
	return self.template()


class UpdateConfiglet():
    def __call__(self):
	portal = api.portal.get()
	try:
            productBrains = api.content.find(context=portal["products"], portal_type="Product")
	except:
	    productBrains = []
        try:
            request = self.request
        except:
            request = getRequest()

        alsoProvides(request, IDisableCSRFProtection)
        # sortList[buggy] = [0,{'1/4': 0, '1/8': 5} ]
        # sortList[${cayegory}] = [${category_count}, { ${subject}: ${subject_count} }]
        sortList = {}
	brandList = {}
	productData = {}
        try:
            for item in productBrains:
		obj = item.getObject()
                category = obj.category
                subject = obj.subcategory
		brand = obj.brand
		title = obj.title
		productNo = obj.productNo
		objAbsUrl = obj.absolute_url()
		salePrice = obj.salePrice
		price = obj.price

                if sortList.has_key(category):
                    sortList[category][0] += 1
                    if sortList[category][1].has_key(subject):
                        sortList[category][1][subject] += 1
                    else:
                        sortList[category][1][subject] = 1
                else:
                    sortList[category] = [1, {subject: 1}]

		if brandList.has_key(brand):
		    brandList[brand] += 1
		else:
		    brandList[brand] = 1
		img = objAbsUrl + '/@@images/cover'
		productData[title] = [category, subject, brand, price, salePrice, objAbsUrl, productNo, img]


            sortList = json.dumps(sortList).decode('utf-8')
            api.portal.set_registry_record('sortList', sortList, interface=IDict)

	    brandList = json.dumps(brandList).decode('utf-8')
	    api.portal.set_registry_record('brandList', brandList, interface=IDict)

	    productData = sorted(productData.items(), key=lambda x:x[0])
            productData = json.dumps(productData).decode('utf-8')
            api.portal.set_registry_record('productData', productData, interface=IDict)

        except  Exception as e:
            print e


class ProductListing(BrowserView):
    template = ViewPageTemplateFile("templates/product_listing.pt")
    def __call__(self):
	sortList = api.portal.get_registry_record("sortList", interface=IDict)
	brandList = api.portal.get_registry_record('brandList', interface=IDict)
	productData = api.portal.get_registry_record('productData', interface=IDict)

	self.sortList = json.loads(sortList)
	self.brandList = json.loads(brandList)
	self.productData = productData
        return self.template()


class NewsFolderView(FolderView, NewsItemView):
    def results (self, **kwargs):
        kwargs.update(self.request.get('contentFilter', {}))
        if 'object_provides' not in kwargs:  # object_provides is more specific
            kwargs.setdefault('portal_type', 'News Item')
        kwargs.setdefault('batch', True)
        kwargs.setdefault('b_size', self.b_size)
        kwargs.setdefault('b_start', self.b_start)

        listing = aq_inner(self.context).restrictedTraverse(
            '@@folderListing', None)
        if listing is None:
            return []
        results = listing(**kwargs)
        return results


class SocialButtonMacro(BrowserView):
    """"""

