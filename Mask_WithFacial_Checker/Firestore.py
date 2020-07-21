# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 00:04:06 2020

@author: SUBHAM KUNDU
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('google-services.json')
firebase_admin.initialize_app(cred)

db = firestore.client()