#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 08-Aug-2013
# Last mod : 08-Aug-2013
# -----------------------------------------------------------------------------
from django.utils.translation import ugettext as _
from django.db                import models
from django.db.models              import ImageField
from django.db.models.fields.files import ImageFieldFile
from PIL                           import Image
from django.core.files.base        import ContentFile
import cStringIO, imghdr, tempfile, logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
#
#    CountryField
#
# -----------------------------------------------------------------------------
# - Took from http://djangosnippets.org/snippets/1281/
# - filtered for countries that are actually referenced into CPI dataset

COUNTRIES = (
    ('AFG', _('Afghanistan')),
    ('ALB', _('Albania')),
    ('DZA', _('Algeria')),
    ('AGO', _('Angola')),
    ('ATG', _('Antigua and Barbuda')),
    ('ARG', _('Argentina')),
    ('ARM', _('Armenia')),
    ('ABW', _('Aruba')),
    ('AUS', _('Australia')),
    ('AUT', _('Austria')),
    ('AZE', _('Azerbaijan')),
    ('BHS', _('Bahamas')),
    ('BHR', _('Bahrain')),
    ('BGD', _('Bangladesh')),
    ('BRB', _('Barbados')),
    ('BLR', _('Belarus')),
    ('BEL', _('Belgium')),
    ('BLZ', _('Belize')),
    ('BEN', _('Benin')),
    ('BTN', _('Bhutan')),
    ('BOL', _('Bolivia')),
    ('BIH', _('Bosnia and Herzegovina')),
    ('BWA', _('Botswana')),
    ('BRA', _('Brazil')),
    ('BRN', _('Brunei Darussalam')),
    ('BGR', _('Bulgaria')),
    ('BFA', _('Burkina Faso')),
    ('BDI', _('Burundi')),
    ('KHM', _('Cambodia')),
    ('CMR', _('Cameroon')),
    ('CAN', _('Canada')),
    ('CPV', _('Cape Verde')),
    ('CAF', _('Central African Republic')),
    ('TCD', _('Chad')),
    ('CHL', _('Chile')),
    ('CHN', _('China')),
    ('HKG', _('China - Hong Kong')),
    ('MAC', _('China - Macao')),
    ('COL', _('Colombia')),
    ('COM', _('Comoros')),
    ('COG', _('Congo')),
    ('CRI', _('Costa Rica')),
    ('CIV', _("Cote d'Ivoire")),
    ('HRV', _('Croatia')),
    ('CYP', _('Cyprus')),
    ('CZE', _('Czech Republic')),
    ('DNK', _('Denmark')),
    ('DJI', _('Djibouti')),
    ('DMA', _('Dominica')),
    ('DOM', _('Dominican Republic')),
    ('ECU', _('Ecuador')),
    ('EGY', _('Egypt')),
    ('SLV', _('El Salvador')),
    ('GNQ', _('Equatorial Guinea')),
    ('EST', _('Estonia')),
    ('ETH', _('Ethiopia')),
    ('FJI', _('Fiji')),
    ('FIN', _('Finland')),
    ('FRA', _('France')),
    ('GAB', _('Gabon')),
    ('GMB', _('Gambia')),
    ('GEO', _('Georgia')),
    ('DEU', _('Germany')),
    ('GHA', _('Ghana')),
    ('GRC', _('Greece')),
    ('GRD', _('Grenada')),
    ('GTM', _('Guatemala')),
    ('GIN', _('Guinea')),
    ('GNB', _('Guinea-Bissau')),
    ('GUY', _('Guyana')),
    ('HTI', _('Haiti')),
    ('HND', _('Honduras')),
    ('HUN', _('Hungary')),
    ('ISL', _('Iceland')),
    ('IND', _('India')),
    ('IDN', _('Indonesia')),
    ('IRN', _('Iran')),
    ('IRQ', _('Iraq')),
    ('IRL', _('Ireland')),
    ('ISR', _('Israel')),
    ('ITA', _('Italy')),
    ('JAM', _('Jamaica')),
    ('JPN', _('Japan')),
    ('JOR', _('Jordan')),
    ('KAZ', _('Kazakhstan')),
    ('KEN', _('Kenya')),
    ('KWT', _('Kuwait')),
    ('KGZ', _('Kyrgyzstan')),
    ('LAO', _("Lao People's Democratic Republic")),
    ('LVA', _('Latvia')),
    ('LBN', _('Lebanon')),
    ('LSO', _('Lesotho')),
    ('LBR', _('Liberia')),
    ('LBY', _('Libyan Arab Jamahiriya')),
    ('LTU', _('Lithuania')),
    ('LUX', _('Luxembourg')),
    ('MKD', _('Macedonia')),
    ('MDG', _('Madagascar')),
    ('MWI', _('Malawi')),
    ('MYS', _('Malaysia')),
    ('MDV', _('Maldives')),
    ('MLI', _('Mali')),
    ('MLT', _('Malta')),
    ('MRT', _('Mauritania')),
    ('MUS', _('Mauritius')),
    ('MEX', _('Mexico')),
    ('MNG', _('Mongolia')),
    ('MNE', _('Montenegro')),
    ('MAR', _('Morocco')),
    ('MOZ', _('Mozambique')),
    ('MMR', _('Myanmar')),
    ('NAM', _('Namibia')),
    ('NPL', _('Nepal')),
    ('NLD', _('Netherlands')),
    ('NZL', _('New Zealand')),
    ('NIC', _('Nicaragua')),
    ('NER', _('Niger')),
    ('NGA', _('Nigeria')),
    ('NOR', _('Norway')),
    ('PSE', _('Occupied Palestinian Territory')),
    ('OMN', _('Oman')),
    ('PAK', _('Pakistan')),
    ('PAN', _('Panama')),
    ('PNG', _('Papua New Guinea')),
    ('PRY', _('Paraguay')),
    ('PER', _('Peru')),
    ('PHL', _('Philippines')),
    ('POL', _('Poland')),
    ('PRT', _('Portugal')),
    ('QAT', _('Qatar')),
    ('KOR', _('Republic of Korea')),
    ('MDA', _('Republic of Moldova')),
    ('ROU', _('Romania')),
    ('RUS', _('Russian Federation')),
    ('RWA', _('Rwanda')),
    ('KNA', _('Saint Kitts and Nevis')),
    ('LCA', _('Saint Lucia')),
    ('VCT', _('Saint Vincent and the Grenadines')),
    ('WSM', _('Samoa')),
    ('SMR', _('San Marino')),
    ('STP', _('Sao Tome and Principe')),
    ('SAU', _('Saudi Arabia')),
    ('SEN', _('Senegal')),
    ('SRB', _('Serbia')),
    ('SYC', _('Seychelles')),
    ('SLE', _('Sierra Leone')),
    ('SGP', _('Singapore')),
    ('SVK', _('Slovakia')),
    ('SVN', _('Slovenia')),
    ('SLB', _('Solomon Islands')),
    ('ZAF', _('South Africa')),
    ('ESP', _('Spain')),
    ('LKA', _('Sri Lanka')),
    ('SDN', _('Sudan')),
    ('SUR', _('Suriname')),
    ('SWZ', _('Swaziland')),
    ('SWE', _('Sweden')),
    ('CHE', _('Switzerland')),
    ('SYR', _('Syrian Arab Republic')),
    ('TJK', _('Tajikistan')),
    ('THA', _('Thailand')),
    ('TLS', _('Timor-Leste')),
    ('TGO', _('Togo')),
    ('TON', _('Tonga')),
    ('TTO', _('Trinidad and Tobago')),
    ('TUN', _('Tunisia')),
    ('TUR', _('Turkey')),
    ('UGA', _('Uganda')),
    ('UKR', _('Ukraine')),
    ('ARE', _('United Arab Emirates')),
    ('GBR', _('United Kingdom')),
    ('TZA', _('United Republic of Tanzania')),
    ('USA', _('United States of America')),
    ('URY', _('Uruguay')),
    ('VUT', _('Vanuatu')),
    ('VEN', _('Venezuela (Bolivarian Republic of)')),
    ('VNM', _('Viet Nam')),
    ('YEM', _('Yemen')),
    ('ZMB', _('Zambia')),
    ('ZWE', _('Zimbabwe')),
)

class CountryField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 3)
        kwargs.setdefault('choices', COUNTRIES)

        super(CountryField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^webapp\.core\.fields\.CountryField"])

# -----------------------------------------------------------------------------
#
#    DJANGO-THUMBS
#                                            by Antonio Melé (http://django.es)
# -----------------------------------------------------------------------------

def generate_thumb(img, thumb_size):
    """
    Generates a thumbnail image and returns a ContentFile object with the thumbnail
    
    Parameters:
    ===========
    img         File object
    
    thumb_size  desired thumbnail size, ie: (200,120)
    
    format      format of the original image ('jpeg','gif','png',...)
                (this format will be used for the generated thumbnail, too)
    """
    img.seek(0) # see http://code.djangoproject.com/ticket/8222 for details
    temp_file = tempfile.NamedTemporaryFile()
    temp_file.write(img.file.read())
    temp_file.flush()
    format = imghdr.what(temp_file.name)
    temp_file.close()
    img.seek(0)
    image = Image.open(img)
    # Convert to RGB if necessary
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGB')
    # get size
    thumb_w, thumb_h = thumb_size
    # If you want to generate a square thumbnail
    if thumb_w == thumb_h:
        # quad
        xsize, ysize = image.size
        # get minimum size
        minsize = min(xsize,ysize)
        # largest square possible in the image
        xnewsize = (xsize-minsize)/2
        ynewsize = (ysize-minsize)/2
        # crop it
        image2 = image.crop((xnewsize, ynewsize, xsize-xnewsize, ysize-ynewsize))
        # load is necessary after crop                
        image2.load()
        # thumbnail of the cropped image (with ANTIALIAS to make it look better)
        image2.thumbnail(thumb_size, Image.ANTIALIAS)
    else:
        # not quad
        image2 = image
        image2.thumbnail(thumb_size, Image.ANTIALIAS)
    io = cStringIO.StringIO()
    # PNG and GIF are the same, JPG is JPEG
    if format.upper()=='JPG':
        format = 'JPEG'
    image2.save(io, format)
    return ContentFile(io.getvalue())    

class ImageWithThumbsFieldFile(ImageFieldFile):
    """
    See ImageWithThumbsField for usage example
    """
    def __init__(self, *args, **kwargs):
        super(ImageWithThumbsFieldFile, self).__init__(*args, **kwargs)
        if self.field.sizes:
            def get_size(self, size):
                if not self:
                    return ''
                else:
                    split = self.url.rsplit('.',1)
                    thumb_url = '%s.%sx%s.%s' % (split[0],w,h,split[1])
                    return thumb_url
            for format, size in self.field.sizes.items():
                (w,h) = size
                setattr(self, "url_%s" % format, get_size(self, size))

    def create_thumbnails(self):
        if self.name and self.field.sizes:
            for size in self.field.sizes.values():
                (w,h)         = size
                split         = self.name.rsplit('.',1)
                thumb_name    = '%s.%sx%s.%s' % (split[0],w,h,split[1])
                # you can use another thumbnailing function if you like
                try:
                    thumb_content = generate_thumb(self.file, size)
                    if self.storage.exists(thumb_name):
                        self.storage.delete(thumb_name)
                    thumb_name_   = self.storage.save(thumb_name, thumb_content)        
                    if not thumb_name == thumb_name_:
                        logger.error('There is already a file named %s' % thumb_name)
                        raise ValueError('There is already a file named %s' % thumb_name)
                except IOError as e:
                    logger.error("IOError")

    def save(self, name, content, save=True):
        super(ImageWithThumbsFieldFile, self).save(name, content, save)
        self.create_thumbnails()

    def delete_thumbnails(self, name):
        if name and self.field.sizes:
            for size in self.field.sizes.values():
                (w,h) = size
                split = name.rsplit('.',1)
                thumb_name = '%s.%sx%s.%s' % (split[0],w,h,split[1])
                try:
                    self.storage.delete(thumb_name)
                except:
                    pass

    def delete(self, save=True):
        name = self.name
        super(ImageWithThumbsFieldFile, self).delete(save)
        self.delete_thumbnails(name)

class ImageWithThumbsField(ImageField):
    attr_class = ImageWithThumbsFieldFile
    """
    Usage example:
    ==============
    photo = ImageWithThumbsField(upload_to='images', sizes=((125,125),(300,200),)
    
    To retrieve image URL, exactly the same way as with ImageField:
        my_object.photo.url
    To retrieve thumbnails URL's just add the size to it:
        my_object.photo.url_125x125
        my_object.photo.url_300x200
    
    Note: The 'sizes' attribute is not required. If you don't provide it, 
    ImageWithThumbsField will act as a normal ImageField
        
    How it works:
    =============
    For each size in the 'sizes' atribute of the field it generates a 
    thumbnail with that size and stores it following this format:
    
    available_filename.[width]x[height].extension

    Where 'available_filename' is the available filename returned by the storage
    backend for saving the original file.
    
    Following the usage example above: For storing a file called "photo.jpg" it saves:
    photo.jpg          (original file)
    photo.125x125.jpg  (first thumbnail)
    photo.300x200.jpg  (second thumbnail)
    
    With the default storage backend if photo.jpg already exists it will use these filenames:
    photo_.jpg
    photo_.125x125.jpg
    photo_.300x200.jpg
    
    Note: django-thumbs assumes that if filename "any_filename.jpg" is available 
    filenames with this format "any_filename.[widht]x[height].jpg" will be available, too.
    """
    # TODO: Add method to regenerate thubmnails. See https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, sizes=None, **kwargs):
        self.verbose_name = verbose_name
        self.name         = name
        self.width_field  = width_field
        self.height_field = height_field
        self.sizes        = sizes
        super(ImageField, self).__init__(**kwargs)

# Add field to South
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^webapp\.core\.fields\.ImageWithThumbsField"])
except:
    pass

# EOF
