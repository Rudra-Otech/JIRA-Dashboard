import streamlit as st
import altair as alt
import plotly.express as px
import pandas as pd
import datetime as dt
from ydata_profiling import ProfileReport

from jira import JIRA
from jira.client import *
from jira.resources import *

import mysql.connector as mysql
from functools import reduce

import warnings

warnings.simplefilter(action='ignore', category=UserWarning)