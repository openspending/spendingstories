#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 08-Aug-2013
# Last mod : 08-Aug-2013
# -----------------------------------------------------------------------------
# This file is part of Spending Stories.
# 
#     Spending Stories is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Spending Stories is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with Spending Stories.  If not, see <http://www.gnu.org/licenses/>.

from django.utils.translation import ugettext as _
from django.db                import models

# -----------------------------------------------------------------------------
#
#    CountryField
#
# -----------------------------------------------------------------------------
# - Took from http://djangosnippets.org/snippets/1281/
# - filtered for countries that are actually referenced into CPI dataset

COUNTRIES = (
    ('AFG', _('Afghanistan (AFG)')),
    ('ALB', _('Albania (ALB)')),
    ('DZA', _('Algeria (DZA)')),
    ('AGO', _('Angola (AGO)')),
    ('ATG', _('Antigua and Barbuda (ATG)')),
    ('ARG', _('Argentina (ARG)')),
    ('ARM', _('Armenia (ARM)')),
    ('ABW', _('Aruba (ABW)')),
    ('AUS', _('Australia (AUS)')),
    ('AUT', _('Austria (AUT)')),
    ('AZE', _('Azerbaijan (AZE)')),
    ('BHS', _('Bahamas (BHS)')),
    ('BHR', _('Bahrain (BHR)')),
    ('BGD', _('Bangladesh (BGD)')),
    ('BRB', _('Barbados (BRB)')),
    ('BLR', _('Belarus (BLR)')),
    ('BEL', _('Belgium (BEL)')),
    ('BLZ', _('Belize (BLZ)')),
    ('BEN', _('Benin (BEN)')),
    ('BTN', _('Bhutan (BTN)')),
    ('BOL', _('Bolivia (BOL)')),
    ('BIH', _('Bosnia and Herzegovina (BIH)')),
    ('BWA', _('Botswana (BWA)')),
    ('BRA', _('Brazil (BRA)')),
    ('BRN', _('Brunei Darussalam (BRN)')),
    ('BGR', _('Bulgaria (BGR)')),
    ('BFA', _('Burkina Faso (BFA)')),
    ('BDI', _('Burundi (BDI)')),
    ('KHM', _('Cambodia (KHM)')),
    ('CMR', _('Cameroon (CMR)')),
    ('CAN', _('Canada (CAN)')),
    ('CPV', _('Cape Verde (CPV)')),
    ('CAF', _('Central African Republic (CAF)')),
    ('TCD', _('Chad (TCD)')),
    ('CHL', _('Chile (CHL)')),
    ('CHN', _('China (CHN)')),
    ('HKG', _('China - Hong Kong (HKG)')),
    ('MAC', _('China - Macao (MAC)')),
    ('COL', _('Colombia (COL)')),
    ('COM', _('Comoros (COM)')),
    ('COG', _('Congo (COG)')),
    ('CRI', _('Costa Rica (CRI)')),
    ('CIV', _("Cote d'Ivoire (CIV)")),
    ('HRV', _('Croatia (HRV)')),
    ('CYP', _('Cyprus (CYP)')),
    ('CZE', _('Czech Republic (CZE)')),
    ('DNK', _('Denmark (DNK)')),
    ('DJI', _('Djibouti (DJI)')),
    ('DMA', _('Dominica (DMA)')),
    ('DOM', _('Dominican Republic (DOM)')),
    ('ECU', _('Ecuador (ECU)')),
    ('EGY', _('Egypt (EGY)')),
    ('SLV', _('El Salvador (SLV)')),
    ('GNQ', _('Equatorial Guinea (GNQ)')),
    ('EST', _('Estonia (EST)')),
    ('ETH', _('Ethiopia (ETH)')),
    ('FJI', _('Fiji (FJI)')),
    ('FIN', _('Finland (FIN)')),
    ('FRA', _('France (FRA)')),
    ('GAB', _('Gabon (GAB)')),
    ('GMB', _('Gambia (GMB)')),
    ('GEO', _('Georgia (GEO)')),
    ('DEU', _('Germany (DEU)')),
    ('GHA', _('Ghana (GHA)')),
    ('GRC', _('Greece (GRC)')),
    ('GRD', _('Grenada (GRD)')),
    ('GTM', _('Guatemala (GTM)')),
    ('GIN', _('Guinea (GIN)')),
    ('GNB', _('Guinea-Bissau (GNB)')),
    ('GUY', _('Guyana (GUY)')),
    ('HTI', _('Haiti (HTI)')),
    ('HND', _('Honduras (HND)')),
    ('HUN', _('Hungary (HUN)')),
    ('ISL', _('Iceland (ISL)')),
    ('IND', _('India (IND)')),
    ('IDN', _('Indonesia (IDN)')),
    ('IRN', _('Iran (IRN)')),
    ('IRQ', _('Iraq (IRQ)')),
    ('IRL', _('Ireland (IRL)')),
    ('ISR', _('Israel (ISR)')),
    ('ITA', _('Italy (ITA)')),
    ('JAM', _('Jamaica (JAM)')),
    ('JPN', _('Japan (JPN)')),
    ('JOR', _('Jordan (JOR)')),
    ('KAZ', _('Kazakhstan (KAZ)')),
    ('KEN', _('Kenya (KEN)')),
    ('KWT', _('Kuwait (KWT)')),
    ('KGZ', _('Kyrgyzstan (KGZ)')),
    ('LAO', _("Lao People's Democratic Republic (LAO)")),
    ('LVA', _('Latvia (LVA)')),
    ('LBN', _('Lebanon (LBN)')),
    ('LSO', _('Lesotho (LSO)')),
    ('LBR', _('Liberia (LBR)')),
    ('LBY', _('Libyan Arab Jamahiriya (LBY)')),
    ('LTU', _('Lithuania (LTU)')),
    ('LUX', _('Luxembourg (LUX)')),
    ('MKD', _('Macedonia (MKD)')),
    ('MDG', _('Madagascar (MDG)')),
    ('MWI', _('Malawi (MWI)')),
    ('MYS', _('Malaysia (MYS)')),
    ('MDV', _('Maldives (MDV)')),
    ('MLI', _('Mali (MLI)')),
    ('MLT', _('Malta (MLT)')),
    ('MRT', _('Mauritania (MRT)')),
    ('MUS', _('Mauritius (MUS)')),
    ('MEX', _('Mexico (MEX)')),
    ('MNG', _('Mongolia (MNG)')),
    ('MNE', _('Montenegro (MNE)')),
    ('MAR', _('Morocco (MAR)')),
    ('MOZ', _('Mozambique (MOZ)')),
    ('MMR', _('Myanmar (MMR)')),
    ('NAM', _('Namibia (NAM)')),
    ('NPL', _('Nepal (NPL)')),
    ('NLD', _('Netherlands (NLD)')),
    ('NZL', _('New Zealand (NZL)')),
    ('NIC', _('Nicaragua (NIC)')),
    ('NER', _('Niger (NER)')),
    ('NGA', _('Nigeria (NGA)')),
    ('NOR', _('Norway (NOR)')),
    ('PSE', _('Occupied Palestinian Territory (PSE)')),
    ('OMN', _('Oman (OMN)')),
    ('PAK', _('Pakistan (PAK)')),
    ('PAN', _('Panama (PAN)')),
    ('PNG', _('Papua New Guinea (PNG)')),
    ('PRY', _('Paraguay (PRY)')),
    ('PER', _('Peru (PER)')),
    ('PHL', _('Philippines (PHL)')),
    ('POL', _('Poland (POL)')),
    ('PRT', _('Portugal (PRT)')),
    ('QAT', _('Qatar (QAT)')),
    ('KOR', _('Republic of Korea (KOR)')),
    ('MDA', _('Republic of Moldova (MDA)')),
    ('ROU', _('Romania (ROU)')),
    ('RUS', _('Russian Federation (RUS)')),
    ('RWA', _('Rwanda (RWA)')),
    ('KNA', _('Saint Kitts and Nevis (KNA)')),
    ('LCA', _('Saint Lucia (LCA)')),
    ('VCT', _('Saint Vincent and the Grenadines (VCT)')),
    ('WSM', _('Samoa (WSM)')),
    ('SMR', _('San Marino (SMR)')),
    ('STP', _('Sao Tome and Principe (STP)')),
    ('SAU', _('Saudi Arabia (SAU)')),
    ('SEN', _('Senegal (SEN)')),
    ('SRB', _('Serbia (SRB)')),
    ('SYC', _('Seychelles (SYC)')),
    ('SLE', _('Sierra Leone (SLE)')),
    ('SGP', _('Singapore (SGP)')),
    ('SVK', _('Slovakia (SVK)')),
    ('SVN', _('Slovenia (SVN)')),
    ('SLB', _('Solomon Islands (SLB)')),
    ('ZAF', _('South Africa (ZAF)')),
    ('ESP', _('Spain (ESP)')),
    ('LKA', _('Sri Lanka (LKA)')),
    ('SDN', _('Sudan (SDN)')),
    ('SUR', _('Suriname (SUR)')),
    ('SWZ', _('Swaziland (SWZ)')),
    ('SWE', _('Sweden (SWE)')),
    ('CHE', _('Switzerland (CHE)')),
    ('SYR', _('Syrian Arab Republic (SYR)')),
    ('TJK', _('Tajikistan (TJK)')),
    ('THA', _('Thailand (THA)')),
    ('TLS', _('Timor-Leste (TLS)')),
    ('TGO', _('Togo (TGO)')),
    ('TON', _('Tonga (TON)')),
    ('TTO', _('Trinidad and Tobago (TTO)')),
    ('TUN', _('Tunisia (TUN)')),
    ('TUR', _('Turkey (TUR)')),
    ('UGA', _('Uganda (UGA)')),
    ('UKR', _('Ukraine (UKR)')),
    ('ARE', _('United Arab Emirates (ARE)')),
    ('GBR', _('United Kingdom (GBR)')),
    ('TZA', _('United Republic of Tanzania (TZA)')),
    ('USA', _('United States of America (USA)')),
    ('URY', _('Uruguay (URY)')),
    ('VUT', _('Vanuatu (VUT)')),
    ('VEN', _('Venezuela (Bolivarian Republic of) (VEN)')),
    ('VNM', _('Viet Nam (VNM)')),
    ('YEM', _('Yemen (YEM)')),
    ('ZMB', _('Zambia (ZMB)')),
    ('ZWE', _('Zimbabwe (ZWE)')),
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

# EOF
