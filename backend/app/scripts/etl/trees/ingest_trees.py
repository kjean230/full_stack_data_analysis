""" 
creating an ingestion python script to read tree data from a csv file and load it into a database
ingesting NYC Tree Census (1995, 2005, 2015) into the SQL table

we will be using JSON config for year-specific column mappings and file paths
and implements idempotency via unique constraint (year, census_tree_id).
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any

import pandas as pd
from geoalchemy2.elements import WKTElement
from sqlalchemy import text
from sqlalchemy.dialects.mysql import insert

from app.db.session import SessionLocal
from app.models.tree import Tree