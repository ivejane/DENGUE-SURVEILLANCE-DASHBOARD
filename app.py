import os

import re

import glob

import warnings

import json

import urllib.request

import numpy as np

import pandas as pd

import streamlit as st

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

import plotly.express as px

from sklearn.cluster import KMeans

from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import StandardScaler

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, mean_squared_error

from statsmodels.tsa.arima.model import ARIMA

from statsmodels.tsa.stattools import adfuller



warnings.filterwarnings("ignore")



CONFIG = {

    "file_candidates": ["FINAL-ADS-DENGUE-DATABASE-2021-2025.xlsx", "FINAL-ADS-DENGUE-DATABASE-2021-2025.xls", "FINAL-ADS-DENGUE-DATABASE-2021-2025.csv"],

    "search_paths": [".", "/content/data", "/content", "/mount/src"],

    "train_years": [2022, 2023, 2024],

    "test_years": [2025, 2026],

    "arima_horizon": 24,

    "age_bins": [0, 5, 10, 18, 60, 200],

    "age_labels": ["0-4", "5-9", "10-17", "18-59", "60+"],

    "min_minority_class": 30,

    "k_clusters": 4,

    "rf_estimators": 200,

    "random_state": 42,

    "valid_municipalities": [

        "Bunawan", "Bayugan", "City Of Bayugan", "Esperanza", "La Paz", "Loreto", 

        "Prosperidad", "Rosario", "San Francisco", "San Luis", 

        "Santa Josefa", "Sibagat", "Talacogon", "Trento", "Veruela"

    ]

}



NULL_TOKENS = {"", "nan", "none", "n/a", "na", "null", "-", "--", ".", "?", "undefined", "#n/a", "#value!", "not applicable", "notavailable"}



def clean_text(value):

    if value is None: return np.nan

    try:

        if pd.isna(value): return np.nan

    except (TypeError, ValueError): pass
