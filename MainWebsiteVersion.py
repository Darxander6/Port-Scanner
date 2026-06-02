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

col1,col2 = st.columns(2)
with col1:
    start_port = st.number_input("starting port", min_value =1,max_value = 65535,value =20)
with col2:
    end_port = st.number_input("ending port", min_value =1,max_value = 65535,value =100)
max_threads = st.slider("Scan Speed (Simultaneous Threads)", min_value=10, max_value=200, value=100)
if st.button("Launch scan", type = "primary"):
    try:
        with st.spinner("resolving target domain..."):
            target_ip = socket.gethostbyname(target_input)
        st.info(f"scanning target: **{target_input}** ({target_ip})")
    except socket.gaierror:
        st.error("Target domain or IP could not be resolved. Check your spelling.")
        st.stop()
    if end_port <start_port:
        st.error("Ending port must be greater than or equal to starting port.")
        st.stop()
    progress_bar= st.progress(0.0)
    status_text = st.empty()
    ports_to_scan = list(range(int(start_port), int(end_port) + 1))

    total_ports = len(ports_to_scan)
    open_ports = []
    log_stream = "Initailizing scan...\n"
    log_area.code(log_stream, langauge = "bash")


    with ThreadPoolExecutor(max_workers = max_threads) as executer:
        futures = {executor.submit(check_port, target_ip, p) : p for p in ports_to_scan}
        for i, future in enumerate(as_completed(futures)):
            port = futures[future]
            result = future.result()
            if result:
                open_ports.append(result)
                log_stream += f"[+] Port {result} is OPEN/n"
            
            progress_percent = (i + 1)/ total_ports
            progress_bar.progress(progress_percent)
            status_text.text(f"Scanning port {port}.. ({i+1}/{total_ports})")
            log_area.code(log_stream, language = "bash")
        status_text.text("Scan Completed!")
        if open_ports:
            st.success(f"Completed! Discovered {len(open_ports)} open ports(s).")
            cols = st.columns*min(len(open_ports), 4)
            for index, op in enumerate(sorted(open_ports)):
                col[index % 4].metric(label = "Open Port", value = f"Port {op}")
        else:
            st.info("Scan completed. No open ports discovered in that specsefic range.")
