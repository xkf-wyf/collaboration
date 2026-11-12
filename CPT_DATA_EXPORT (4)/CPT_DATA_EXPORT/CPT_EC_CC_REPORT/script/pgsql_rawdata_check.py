# Databricks notebook source
import pandas as pd 
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

cl_ads = spark.conf.get('spark.var.catalog.ads')
current_date = datetime.now()
dth = current_date.strftime("%Y%m%d") 
# dth = '20260129'

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file_path = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/finbit/dm_tf_ddm_cc_output/{dth}"

if os.path.exists(file_path):
    dbutils.fs.rm(file_path, recurse=True)