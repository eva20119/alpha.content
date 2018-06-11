# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from alpha.content import _


class IProduct(model.Schema):
    title = schema.TextLine(
        title=_(u'Title'),
        required=True
    )

    productNo = schema.TextLine(
        title=_(u'Product Nomber'),
        required=False
    )
    
    rating = schema.TextLine(
        title=_(u'Rating'),
        required=False,
        readonly=True,
    )
    
    price = schema.TextLine(
        title=_(u'Price'),
        required=False
    )

    salePrice = schema.TextLine(
        title=_(u'Sale Price'),
        required=False
    )

    cover = namedfile.NamedBlobImage(
        title=_(u'Cover Image'),
        required=False,
    )

    description = schema.Text(
        title=(u'Description'),
        required=False
    )
 
    fieldset('More Info', fields=['brand', 'productCode', 'availability', 'downloadFile', 'feature'])
    brand = schema.TextLine(
        title=_(u'Brand'),
        required=False
    )

    productCode = schema.TextLine(
        title=_(u'Produce Code'),
        required=False
    )

    availability = schema.TextLine(
        title=(u'Availability'),
        required=False
    )
    
    downloadFile = namedfile.NamedBlobFile(
        title=_(u'Download File'),
        required=False,
    )
    
    feature = RichText(
        title=_(u'Feature'),
        required=False
    )

    fieldset('Specification', fields=['specification'])
    specification = schema.List(
        title=_(u'specification'),
        description=_(u'ex. clockspeed:100mhz'),
        value_type=schema.TextLine(),
        required=False,
    )

@implementer(IProduct)
class Product(Container):
    """
    """