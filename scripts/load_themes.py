#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 07-Aug-2013
# Last mod : 07-Aug-2013
# -----------------------------------------------------------------------------
from webapp.core.models import Theme

THEMES   = ("admin-culture", "admin-order-safety", "aid-developing-countries", "aid", "airplane", "ambulance", "books", "car", "civil-defence", "civilian-action", "coal", "communication", "community", "construction", "courts", "culture", "defence-admin", "defence-research", "defence", "dollar", "economic-aid", "economy-tourism", "education", "electricity", "energy", "environment-admin", "environment", "euro", "family", "farms", "financial-admin", "fishing", "foreign-military-aid", "forest", "fuel", "garbage", "government", "health", "helping-others", "hospital-specialized", "hospital", "housing", "human-resources", "labour", "legislative", "manufactoring-construction", "media", "medical-supplies", "military", "misc-services", "money", "nuclear", "old-age", "order-safety", "other-medical", "our-streets", "petrol", "police2", "pollution", "post-secondary", "pound2", "pre-school", "primary", "prisons", "public-debt", "publicaffairs", "railways", "rd-order-safety", "research", "satellite-dish", "schools", "secondary-lower", "secondary-upper", "social-systems", "sports", "street-lights", "traffic-watersup", "transport", "tree", "unemployment", "unknown", "waste", "water", "wheelchair", "wind")
DISABLED = ("EC", "admin", "africa", "anchor", "asia", "dental", "energy2", "family2", "fire-brigade", "government-uk", "harbor", "island", "microscope", "planning", "police", "pound", "toilet", "worldmap")


for theme_name in THEMES:
    theme = Theme()
    theme.title  = theme_name
    theme.image  = "themes/%s.svg" % theme_name
    theme.save()

for theme_name in DISABLED:
    theme = Theme()
    theme.title  = theme_name
    theme.image  = "themes/%s.svg" % theme_name
    theme.active = False
    theme.save()
