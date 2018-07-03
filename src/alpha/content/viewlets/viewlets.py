# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import common as base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import alsoProvides
from alpha.content.browser.view import ExchangeRate
from plone.protect.interfaces import IDisableCSRFProtection
from plone import api
from sets import Set
import datetime
from alpha.content.browser.currency_configlet import IExchange


class ProductViewlet(base.ViewletBase, ExchangeRate):
    def getMostView(self):
        context = api.portal.get()
        if self.context.getParentNode().has_key('products'):
            context = self.context.getParentNode()['products']
        mostView = api.content.find(context=context, portal_type='Product', p_indexCategory='mostView', depth=1)
        return mostView

    def getSpecial(self):
        context = api.portal.get()
        if self.context.getParentNode().has_key('products'):
            context = self.context.getParentNode()['products']
        special = api.content.find(context=context, portal_type='Product', p_indexCategory='special', depth=1)
        return special

    def getLatest(self):
        context = api.portal.get()
        if self.context.getParentNode().has_key('products'):
            context = self.context.getParentNode()['products']
        latest = api.content.find(context=context, portal_type='Product', p_indexCategory='latest', depth=1)
        return latest


class TimeLimitViewlet(base.ViewletBase, ExchangeRate):
    def getTimeLimit(self):
        context = api.portal.get()
        timeLimitList = []
        if self.context.getParentNode().has_key('promotions'):
            context = self.context.getParentNode()['promotions']
            timeLimitBrain = api.content.find(context=context, portal_type='Product', depth=1)
            for item in timeLimitBrain:
                item_timeLimit = item.getObject().timeLimit or datetime.datetime(1,1,1,0,0)
                if not(item_timeLimit and not item_timeLimit >= datetime.datetime.today()):
                    timeLimitList.append(item)
        return timeLimitList


class BestSellersViewlet(base.ViewletBase, ExchangeRate):
    def getBestSellers(self):
        context = api.portal.get()
        if self.context.getParentNode().has_key('products'):
            context = self.context.getParentNode()['products']
        bestSellers = api.content.find(context=context, portal_type='Product', p_bestSeller=True, depth=1)
        return bestSellers


class MainBanner(ProductViewlet, TimeLimitViewlet, BestSellersViewlet, ExchangeRate):
    def pdb(self):
        import pdb;pdb.set_trace()

    def getBannerPage(self):
        context = api.portal.get()
        bannerPage = []
        if self.context.getParentNode().has_key('banner'):
            context = self.context.getParentNode()['banner']
        bannerPage = api.content.find(context=context, portal_type='Document', depth=1)
        return bannerPage

    def getAllIndexProduct(self):
        allProduct = Set()
        for item in self.getMostView():
            allProduct.add(item.getObject())

        for item in self.getSpecial():
            allProduct.add(item.getObject())

        for item in self.getLatest():
            allProduct.add(item.getObject())

        for item in self.getTimeLimit():
            allProduct.add(item.getObject())

        for item in self.getBestSellers():
            allProduct.add(item.getObject())

        return allProduct
    
    def getObjectImg(self, obj):
        objectImg = api.content.find(context=obj, portal_type='productimg', depth=1, b_size=4)
        return objectImg


class NewsViewlet(base.ViewletBase):
    def getNewsItem(self):
        context = api.portal.get()
        if self.context.getParentNode().has_key('news'):
            context = self.context.getParentNode()['news']
        newsItem = api.content.find(context=context, portal_type='News Item', b_size=12, depth=1)
        return newsItem

    def getNewsMonth(self, obj):
        return datetime.datetime.strptime(obj.CreationDate(), '%Y-%m-%dT%H:%M:%S+00:00').strftime('%B')

    def getNewsYear(self, obj):
        return datetime.datetime.strptime(obj.CreationDate(), '%Y-%m-%dT%H:%M:%S+00:00').strftime('%Y')

    def getNewsDay(self, obj):
        return datetime.datetime.strptime(obj.CreationDate(), '%Y-%m-%dT%H:%M:%S+00:00').strftime('%d')


class FriendLinkViewlet(base.ViewletBase):
    def getFriendLink(self):
        portal = api.portal.get()
        friendLink = []
        if portal.hasObject('friend-link'):
            friendLink = api.content.find(portal['friend-link'], portal_type='Link')
        return friendLink


class ShopCart(base.ViewletBase):
   def getRmbRate(self):
        return api.portal.get_registry_record('exchange', interface=IExchange)


class AccountViewlet(base.ViewletBase):
    def isAnonymous(self):
        if not api.user.is_anonymous():
            return False
        return True

    def getCurrentUser(self):
        current = api.user.get_current()
        return current


class NewsletterViewlet(base.ViewletBase):
    def update(self):
        formdata = self.request.form
        if formdata.has_key('email_add'):
            email = formdata.pop('email_add')
            self.updateEmailList(email)
            current_url = self.context.absolute_url() 
            self.request.response.redirect(current_url)

    def updateEmailList(self, email):
        newsletter = self.getNewsletter()
        emailList = Set()
        if newsletter != None:
            emailList = newsletter.getObject().description.split('\r\n')
            emailList = Set([e for e in emailList if e != ''])
            emailList.add(email)
            request = self.request
            alsoProvides(request, IDisableCSRFProtection)
            emailStr = ''
            for email in emailList:
                emailStr += email + '\r\n' 
            newsletter.getObject().description = emailStr 

    def getNewsletter(self):
        portal = api.portal.get()
        if portal.hasObject('resource'):
            emailPage = api.content.find(portal['resource'], portal_type='Document', id='newsletter' )
            return emailPage[0] if len(emailPage) != 0 else None
        else:
            return 

