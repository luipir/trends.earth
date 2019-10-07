# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LDMP - A QGIS plugin
 This plugin supports monitoring and reporting of land degradation to the UNCCD 
 and in support of the SDG Land Degradation Neutrality (LDN) target.
                              -------------------
        begin                : 2017-05-23
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Conservation International
        email                : GEF-LDMP@conservation.org
 ***************************************************************************/
"""

import os
import json

from qgis.PyQt.QtCore import QTimer, Qt
from qgis.PyQt.QtWidgets import QMessageBox, QApplication
from qgis.PyQt.QtTest import QTest

from LDMP.layers import add_layer, get_file_metadata


with open(os.path.join(os.path.dirname(__file__), 'trends.earth_test_user_credentials.json'), 'r') as fin:
    regular_keys = json.load(fin)
with open(os.path.join(os.path.dirname(__file__), 'trends.earth_admin_user_credentials.json'), 'r') as fin:
    admin_keys = json.load(fin)


# Ensure any message boxes that open are closed within 1 second
def close_msg_boxes():
    for w in QApplication.topLevelWidgets():
        if isinstance(w, QMessageBox):
            print('Closing message box')
            QTest.keyClick(w, Qt.Key_Enter)
timer = QTimer()
timer.timeout.connect(close_msg_boxes)
timer.start(1000)


# Used to load default bands from test datasets onto the map
def add_default_bands_to_map(f):
    json_file = os.path.splitext(f)[0] + '.json'
    m = get_file_metadata(json_file)
    for band_number in range(1, len(m['bands']) + 1):
        # The minus 1 is because band numbers start at 1, not zero
        band_info = m['bands'][band_number - 1]
        if band_info['add_to_map']:
            add_layer(f, band_number, band_info)
