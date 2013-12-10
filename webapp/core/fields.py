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

from django.db import models

# -----------------------------------------------------------------------------
#
#    CountryField
#
# -----------------------------------------------------------------------------
# - Took from http://djangosnippets.org/snippets/1281/
# - filtered for countries that are actually referenced into CPI dataset

COUNTRIES = (
    ('AFG', 'Afghanistan (AFG)'),
    ('ALB', 'Albania (ALB)'),
    ('DZA', 'Algeria (DZA)'),
    ('AGO', 'Angola (AGO)'),
    ('ATG', 'Antigua and Barbuda (ATG)'),
    ('ARG', 'Argentina (ARG)'),
    ('ARM', 'Armenia (ARM)'),
    ('ABW', 'Aruba (ABW)'),
    ('AUS', 'Australia (AUS)'),
    ('AUT', 'Austria (AUT)'),
    ('AZE', 'Azerbaijan (AZE)'),
    ('BHS', 'Bahamas (BHS)'),
    ('BHR', 'Bahrain (BHR)'),
    ('BGD', 'Bangladesh (BGD)'),
    ('BRB', 'Barbados (BRB)'),
    ('BLR', 'Belarus (BLR)'),
    ('BEL', 'Belgium (BEL)'),
    ('BLZ', 'Belize (BLZ)'),
    ('BEN', 'Benin (BEN)'),
    ('BTN', 'Bhutan (BTN)'),
    ('BOL', 'Bolivia (BOL)'),
    ('BIH', 'Bosnia and Herzegovina (BIH)'),
    ('BWA', 'Botswana (BWA)'),
    ('BRA', 'Brazil (BRA)'),
    ('BRN', 'Brunei Darussalam (BRN)'),
    ('BGR', 'Bulgaria (BGR)'),
    ('BFA', 'Burkina Faso (BFA)'),
    ('BDI', 'Burundi (BDI)'),
    ('KHM', 'Cambodia (KHM)'),
    ('CMR', 'Cameroon (CMR)'),
    ('CAN', 'Canada (CAN)'),
    ('CPV', 'Cape Verde (CPV)'),
    ('CAF', 'Central African Republic (CAF)'),
    ('TCD', 'Chad (TCD)'),
    ('CHL', 'Chile (CHL)'),
    ('CHN', 'China (CHN)'),
    ('HKG', 'China - Hong Kong (HKG)'),
    ('MAC', 'China - Macao (MAC)'),
    ('COL', 'Colombia (COL)'),
    ('COM', 'Comoros (COM)'),
    ('COG', 'Congo (COG)'),
    ('CRI', 'Costa Rica (CRI)'),
    ('CIV', "Cote d'Ivoire (CIV)"),
    ('HRV', 'Croatia (HRV)'),
    ('CYP', 'Cyprus (CYP)'),
    ('CZE', 'Czech Republic (CZE)'),
    ('DNK', 'Denmark (DNK)'),
    ('DJI', 'Djibouti (DJI)'),
    ('DMA', 'Dominica (DMA)'),
    ('DOM', 'Dominican Republic (DOM)'),
    ('ECU', 'Ecuador (ECU)'),
    ('EGY', 'Egypt (EGY)'),
    ('SLV', 'El Salvador (SLV)'),
    ('GNQ', 'Equatorial Guinea (GNQ)'),
    ('EST', 'Estonia (EST)'),
    ('ETH', 'Ethiopia (ETH)'),
    ('FJI', 'Fiji (FJI)'),
    ('FIN', 'Finland (FIN)'),
    ('FRA', 'France (FRA)'),
    ('GAB', 'Gabon (GAB)'),
    ('GMB', 'Gambia (GMB)'),
    ('GEO', 'Georgia (GEO)'),
    ('DEU', 'Germany (DEU)'),
    ('GHA', 'Ghana (GHA)'),
    ('GRC', 'Greece (GRC)'),
    ('GRD', 'Grenada (GRD)'),
    ('GTM', 'Guatemala (GTM)'),
    ('GIN', 'Guinea (GIN)'),
    ('GNB', 'Guinea-Bissau (GNB)'),
    ('GUY', 'Guyana (GUY)'),
    ('HTI', 'Haiti (HTI)'),
    ('HND', 'Honduras (HND)'),
    ('HUN', 'Hungary (HUN)'),
    ('ISL', 'Iceland (ISL)'),
    ('IND', 'India (IND)'),
    ('IDN', 'Indonesia (IDN)'),
    ('IRN', 'Iran (IRN)'),
    ('IRQ', 'Iraq (IRQ)'),
    ('IRL', 'Ireland (IRL)'),
    ('ISR', 'Israel (ISR)'),
    ('ITA', 'Italy (ITA)'),
    ('JAM', 'Jamaica (JAM)'),
    ('JPN', 'Japan (JPN)'),
    ('JOR', 'Jordan (JOR)'),
    ('KAZ', 'Kazakhstan (KAZ)'),
    ('KEN', 'Kenya (KEN)'),
    ('KWT', 'Kuwait (KWT)'),
    ('KGZ', 'Kyrgyzstan (KGZ)'),
    ('LAO', "Lao People's Democratic Republic (LAO)"),
    ('LVA', 'Latvia (LVA)'),
    ('LBN', 'Lebanon (LBN)'),
    ('LSO', 'Lesotho (LSO)'),
    ('LBR', 'Liberia (LBR)'),
    ('LBY', 'Libyan Arab Jamahiriya (LBY)'),
    ('LTU', 'Lithuania (LTU)'),
    ('LUX', 'Luxembourg (LUX)'),
    ('MKD', 'Macedonia (MKD)'),
    ('MDG', 'Madagascar (MDG)'),
    ('MWI', 'Malawi (MWI)'),
    ('MYS', 'Malaysia (MYS)'),
    ('MDV', 'Maldives (MDV)'),
    ('MLI', 'Mali (MLI)'),
    ('MLT', 'Malta (MLT)'),
    ('MRT', 'Mauritania (MRT)'),
    ('MUS', 'Mauritius (MUS)'),
    ('MEX', 'Mexico (MEX)'),
    ('MNG', 'Mongolia (MNG)'),
    ('MNE', 'Montenegro (MNE)'),
    ('MAR', 'Morocco (MAR)'),
    ('MOZ', 'Mozambique (MOZ)'),
    ('MMR', 'Myanmar (MMR)'),
    ('NAM', 'Namibia (NAM)'),
    ('NPL', 'Nepal (NPL)'),
    ('NLD', 'Netherlands (NLD)'),
    ('NZL', 'New Zealand (NZL)'),
    ('NIC', 'Nicaragua (NIC)'),
    ('NER', 'Niger (NER)'),
    ('NGA', 'Nigeria (NGA)'),
    ('NOR', 'Norway (NOR)'),
    ('PSE', 'Occupied Palestinian Territory (PSE)'),
    ('OMN', 'Oman (OMN)'),
    ('PAK', 'Pakistan (PAK)'),
    ('PAN', 'Panama (PAN)'),
    ('PNG', 'Papua New Guinea (PNG)'),
    ('PRY', 'Paraguay (PRY)'),
    ('PER', 'Peru (PER)'),
    ('PHL', 'Philippines (PHL)'),
    ('POL', 'Poland (POL)'),
    ('PRT', 'Portugal (PRT)'),
    ('QAT', 'Qatar (QAT)'),
    ('KOR', 'Republic of Korea (KOR)'),
    ('MDA', 'Republic of Moldova (MDA)'),
    ('ROU', 'Romania (ROU)'),
    ('RUS', 'Russian Federation (RUS)'),
    ('RWA', 'Rwanda (RWA)'),
    ('KNA', 'Saint Kitts and Nevis (KNA)'),
    ('LCA', 'Saint Lucia (LCA)'),
    ('VCT', 'Saint Vincent and the Grenadines (VCT)'),
    ('WSM', 'Samoa (WSM)'),
    ('SMR', 'San Marino (SMR)'),
    ('STP', 'Sao Tome and Principe (STP)'),
    ('SAU', 'Saudi Arabia (SAU)'),
    ('SEN', 'Senegal (SEN)'),
    ('SRB', 'Serbia (SRB)'),
    ('SYC', 'Seychelles (SYC)'),
    ('SLE', 'Sierra Leone (SLE)'),
    ('SGP', 'Singapore (SGP)'),
    ('SVK', 'Slovakia (SVK)'),
    ('SVN', 'Slovenia (SVN)'),
    ('SLB', 'Solomon Islands (SLB)'),
    ('ZAF', 'South Africa (ZAF)'),
    ('ESP', 'Spain (ESP)'),
    ('LKA', 'Sri Lanka (LKA)'),
    ('SDN', 'Sudan (SDN)'),
    ('SUR', 'Suriname (SUR)'),
    ('SWZ', 'Swaziland (SWZ)'),
    ('SWE', 'Sweden (SWE)'),
    ('CHE', 'Switzerland (CHE)'),
    ('SYR', 'Syrian Arab Republic (SYR)'),
    ('TJK', 'Tajikistan (TJK)'),
    ('THA', 'Thailand (THA)'),
    ('TLS', 'Timor-Leste (TLS)'),
    ('TGO', 'Togo (TGO)'),
    ('TON', 'Tonga (TON)'),
    ('TTO', 'Trinidad and Tobago (TTO)'),
    ('TUN', 'Tunisia (TUN)'),
    ('TUR', 'Turkey (TUR)'),
    ('UGA', 'Uganda (UGA)'),
    ('UKR', 'Ukraine (UKR)'),
    ('ARE', 'United Arab Emirates (ARE)'),
    ('GBR', 'United Kingdom (GBR)'),
    ('TZA', 'United Republic of Tanzania (TZA)'),
    ('USA', 'United States of America (USA)'),
    ('URY', 'Uruguay (URY)'),
    ('VUT', 'Vanuatu (VUT)'),
    ('VEN', 'Venezuela (Bolivarian Republic of) (VEN)'),
    ('VNM', 'Viet Nam (VNM)'),
    ('YEM', 'Yemen (YEM)'),
    ('ZMB', 'Zambia (ZMB)'),
    ('ZWE', 'Zimbabwe (ZWE)'),
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
