#!/usr/bin/python3
# This file is not mandatory.
# It's just a file your cronjob can run to update your database.

import sql_database as sqldb

sqldb.uploadToTable()
sqldb.deleteOld()