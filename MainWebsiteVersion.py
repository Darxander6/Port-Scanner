import socket
import threading
import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed
st.set_page_config(page_title="Port Scanner with python", page_icon = "🛡️")
st.title("Port Scanner with python")
st.write("A secure, web-hosted demonstration tool to check for open ports on target hosts.")
def check_port(target_ip, port):

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            result = s.connect_ex((target_ip,port))
            if result ==0:
                return port
    except Exception:
        pass
    return None

target_input = st.text_input("enter Target Host (ip or Domain name)",value = "localhost")
