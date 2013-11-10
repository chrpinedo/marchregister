#!/usr/bin/env python
# -*- coding: utf-8 -*-


# default configuration
# this configuration options may be overwritten by a external configuration
# file provided by the MARCHREGISTER_SETTINGS variable.
DATABASE = '/tmp/marchregister.db'
DATABASE_SQL = 'marchregister.sql'
DATABASE_TABLE = 'entries'
DATABASE_FIELDS = { 'entries' : ['number', 'name', 'first_lastname',
                                 'second_lastname', 'id_number', 'settlement',
                                 'province', 'sex', 'federated', 'club',
                                 'email', 'born_date', 'registry_date',
                                 'registry_time']}
CSV_FILE = 'registries.csv'
DEBUG = True
SECRET_KEY = '123secret456key'
USERNAME = 'admin'
PASSWORD = 'admin'
HTML_TITLE = 'XXVII. Gorobel Ibilaldia'
HTML_RECHECK = False
REGISTER = True
# end of the configuration


# vim: ts=8 sts=4 sw=4 et
