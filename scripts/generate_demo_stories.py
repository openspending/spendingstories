#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : date
# Last mod : date
# -----------------------------------------------------------------------------
import random
import loremipsum
from webapp.core.models import Theme, Story
from webapp.currency.models import Currency

YEARS     = range(2003, 2013)
CURRENCY  = Currency.objects.all()
THEMES    = list(Theme.objects.filter(active=True))
COUNTRIES = (('AFG', 'Afghanistan'),('ALB', 'Albania'),('DZA', 'Algeria'),('AGO', 'Angola'),('ATG', 'Antigua and Barbuda'),('ARG', 'Argentina'),('ARM', 'Armenia'),('ABW', 'Aruba'),('AUS', 'Australia'),('AUT', 'Austria'),('AZE', 'Azerbaijan'),('BHS', 'Bahamas'),('BHR', 'Bahrain'),('BGD', 'Bangladesh'),('BRB', 'Barbados'),('BLR', 'Belarus'),('BEL', 'Belgium'),('BLZ', 'Belize'),('BEN', 'Benin'),('BTN', 'Bhutan'),('BOL', 'Bolivia'),('BIH', 'Bosnia and Herzegovina'),('BWA', 'Botswana'),('BRA', 'Brazil'),('BRN', 'Brunei Darussalam'),('BGR', 'Bulgaria'),('BFA', 'Burkina Faso'),('BDI', 'Burundi'),('KHM', 'Cambodia'),('CMR', 'Cameroon'),('CAN', 'Canada'),('CPV', 'Cape Verde'),('CAF', 'Central African Republic'),('TCD', 'Chad'),('CHL', 'Chile'),('CHN', 'China'),('HKG', 'China - Hong Kong'),('MAC', 'China - Macao'),('COL', 'Colombia'),('COM', 'Comoros'),('COG', 'Congo'),('CRI', 'Costa Rica'),('CIV', "Cote d'Ivoire"),('HRV', 'Croatia'),('CYP', 'Cyprus'),('CZE', 'Czech Republic'),('DNK', 'Denmark'),('DJI', 'Djibouti'),('DMA', 'Dominica'),('DOM', 'Dominican Republic'),('ECU', 'Ecuador'),('EGY', 'Egypt'),('SLV', 'El Salvador'),('GNQ', 'Equatorial Guinea'),('EST', 'Estonia'),('ETH', 'Ethiopia'),('FJI', 'Fiji'),('FIN', 'Finland'),('FRA', 'France'),('GAB', 'Gabon'),('GMB', 'Gambia'),('GEO', 'Georgia'),('DEU', 'Germany'),('GHA', 'Ghana'),('GRC', 'Greece'),('GRD', 'Grenada'),('GTM', 'Guatemala'),('GIN', 'Guinea'),('GNB', 'Guinea-Bissau'),('GUY', 'Guyana'),('HTI', 'Haiti'),('HND', 'Honduras'),('HUN', 'Hungary'),('ISL', 'Iceland'),('IND', 'India'),('IDN', 'Indonesia'),('IRN', 'Iran'),('IRQ', 'Iraq'),('IRL', 'Ireland'),('ISR', 'Israel'),('ITA', 'Italy'),('JAM', 'Jamaica'),('JPN', 'Japan'),('JOR', 'Jordan'),('KAZ', 'Kazakhstan'),('KEN', 'Kenya'),('KWT', 'Kuwait'),('KGZ', 'Kyrgyzstan'),('LAO', "Lao People's Democratic Republic"),('LVA', 'Latvia'),('LBN', 'Lebanon'),('LSO', 'Lesotho'),('LBR', 'Liberia'),('LBY', 'Libyan Arab Jamahiriya'),('LTU', 'Lithuania'),('LUX', 'Luxembourg'),('MKD', 'Macedonia'),('MDG', 'Madagascar'),('MWI', 'Malawi'),('MYS', 'Malaysia'),('MDV', 'Maldives'),('MLI', 'Mali'),('MLT', 'Malta'),('MRT', 'Mauritania'),('MUS', 'Mauritius'),('MEX', 'Mexico'),('MNG', 'Mongolia'),('MNE', 'Montenegro'),('MAR', 'Morocco'),('MOZ', 'Mozambique'),('MMR', 'Myanmar'),('NAM', 'Namibia'),('NPL', 'Nepal'),('NLD', 'Netherlands'),('NZL', 'New Zealand'),('NIC', 'Nicaragua'),('NER', 'Niger'),('NGA', 'Nigeria'),('NOR', 'Norway'),('PSE', 'Occupied Palestinian Territory'),('OMN', 'Oman'),('PAK', 'Pakistan'),('PAN', 'Panama'),('PNG', 'Papua New Guinea'),('PRY', 'Paraguay'),('PER', 'Peru'),('PHL', 'Philippines'),('POL', 'Poland'),('PRT', 'Portugal'),('QAT', 'Qatar'),('KOR', 'Republic of Korea'),('MDA', 'Republic of Moldova'),('ROU', 'Romania'),('RUS', 'Russian Federation'),('RWA', 'Rwanda'),('KNA', 'Saint Kitts and Nevis'),('LCA', 'Saint Lucia'),('VCT', 'Saint Vincent and the Grenadines'),('WSM', 'Samoa'),('SMR', 'San Marino'),('STP', 'Sao Tome and Principe'),('SAU', 'Saudi Arabia'),('SEN', 'Senegal'),('SRB', 'Serbia'),('SYC', 'Seychelles'),('SLE', 'Sierra Leone'),('SGP', 'Singapore'),('SVK', 'Slovakia'),('SVN', 'Slovenia'),('SLB', 'Solomon Islands'),('ZAF', 'South Africa'),('ESP', 'Spain'),('LKA', 'Sri Lanka'),('SDN', 'Sudan'),('SUR', 'Suriname'),('SWZ', 'Swaziland'),('SWE', 'Sweden'),('CHE', 'Switzerland'),('SYR', 'Syrian Arab Republic'),('TJK', 'Tajikistan'),('THA', 'Thailand'),('TLS', 'Timor-Leste'),('TGO', 'Togo'),('TON', 'Tonga'),('TTO', 'Trinidad and Tobago'),('TUN', 'Tunisia'),('TUR', 'Turkey'),('UGA', 'Uganda'),('UKR', 'Ukraine'),('ARE', 'United Arab Emirates'),('GBR', 'United Kingdom'),('TZA', 'United Republic of Tanzania'),('USA', 'United States of America'),('URY', 'Uruguay'),('VUT', 'Vanuatu'),('VEN', 'Venezuela (Bolivarian Republic of)'),('VNM', 'Viet Nam'),('YEM', 'Yemen'),('ZMB', 'Zambia'),('ZWE', 'Zimbabwe'))

for i in range(100):
    story = Story()

    story.title               = loremipsum.generate_sentence()[2].rstrip(".")
    story.description         = random.choice( [loremipsum.generate_sentence()[2].rstrip("."),""] )
    story.value               = random.randint(1,200) * int("1" + "0" * random.randint(1,15))
    story.year                = random.choice(YEARS)
    story.country             = random.choice(COUNTRIES)[0]
    story.currency            = random.choice(CURRENCY)
    story.status              = random.choice(('published', 'refused', 'pending'))
    story.type                = random.choice(("over_one_year", "discrete"))
    story.source              = "http://www.okf.org"
    story.sticky              = random.randint(0,1) == 0
    # themes
    story.save()
    for j in range(random.randint(0, 4)):
        story.themes.add(random.choice(THEMES))

# EOF
