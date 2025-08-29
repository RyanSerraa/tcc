import streamlit as st
from openai import OpenAI


class Agents:
    
    @staticmethod
    @st.cache_resource
    def load_agent(agentEndpoint, apiKey):
        base_url = agentEndpoint + "/api/v1"
        api_key = apiKey
        client = OpenAI(base_url=base_url, api_key=api_key)
        return client