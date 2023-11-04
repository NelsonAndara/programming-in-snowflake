import os, configparser
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session

# Get either online Snowflake session, or local session (on error)
@st.cache_resource(show_spinner="Connecting to Snowflake...")
def getSession():
    try:
        return get_active_session()
    except:
        # customize with your own local connection parameters
        parser = configparser.ConfigParser()
        parser.read(os.path.join(os.path.expanduser('~'), ".snowsql/config"))
        section = "connections.demo_conn"
        pars = {
            "account": parser.get(section, "accountname"),
            "user": parser.get(section, "username"),
            "password": os.environ['SNOWSQL_PWD']
        }
        return Session.builder.configs(pars).create()

@st.cache_data(show_spinner="Running a Snowflake query...")
def runQuery(query):
    try: return getSession().sql(query).collect()
    except Exception as e: st.error(e); return None
