import streamlit as st
from PIL import Image

import dscript


# Check if the ip address is valid
def is_valid_ipv4(ip):
    try:
        return all(0 <= int(num) < 256 for num in ip.split('.')) and len(ip.split('.')) == 4
    except ValueError:
        return False


img = Image.open('./favicon.ico')

st.set_page_config(page_title="dscript driver", page_icon=img)
st.title("dscript driver")
infobox = st.empty()


def ip_changed():
    ip = st.session_state.ip_address
    if is_valid_ipv4(ip):
        dscript.ip_address = ip
    else:
        st.error('Invalid IP address')


st.text_input('Module ip address', value=dscript.ip_address, key='ip_address', on_change=ip_changed)


def set_gate(position: int, switch: int, state: bool):
    infobox.info(f'{"C" if state else "Disc"}onnecting gate...')
    try:
        dscript.set_gate(position, switch, state)
        infobox.success(f'Gate {i + 1} {"" if state else "dis"}connected')
    except Exception as e:
        infobox.error(type(e).__name__ + ': ' + str(e))


col1, col2, _, col3, col4 = st.columns([2, 2, 1, 2, 2])


with col1:
    st.subheader('Switch 1')
    for i in range(6):
        if st.button(f'🟢 Connect {i + 1}', key=f'connect1-{i + 1}', use_container_width=True):
            set_gate(i + 1, 1, True)

with col2:
    st.subheader('ㅤ')
    for i in range(6):
        if st.button(f'🔴 Disconnect {i + 1}', key=f'disconnect1-{i + 1}', use_container_width=True):
            set_gate(i + 1, 1, False)

with col3:
    st.subheader('Switch 2')
    for i in range(6):
        if st.button(f'🟢 Connect {i + 1}', key=f'connect2-{i + 1}', use_container_width=True):
            set_gate(i + 1, 2, True)

with col4:
    st.subheader('ㅤ')
    for i in range(6):
        if st.button(f'🔴 Disconnect {i + 1}', key=f'disconnect2-{i + 1}', use_container_width=True):
            dscript.set_gate(i + 1, 2, False)
            set_gate(i + 1, 2, False)

st.text('\n')
if st.button('🔁 Reset All Relays', key='reset'):
    dscript.reset_relays()
st.divider()


def numeric_changed():
    st.session_state.slider = st.session_state.numeric
    dscript.pulse_duration = st.session_state.numeric


def slider_changed():
    st.session_state.numeric = st.session_state.slider
    dscript.pulse_duration = st.session_state.slider


if 'slider' not in st.session_state:
    st.session_state.slider = dscript.pulse_duration

if 'numeric' not in st.session_state:
    st.session_state.numeric = dscript.pulse_duration

st.number_input('Pulse edge duration (s)', min_value=0.0,
                step=0.01,
                format="%.3f",
                key='numeric', on_change=numeric_changed, help='⎍')

st.slider('slider', min_value=0.0,
          max_value=1.0,
          format="%.3f",
          step=0.001,
          key='slider', on_change=slider_changed, label_visibility='hidden')

st.text('\n')


def change_timeout():
    dscript.connection_timeout = round(st.session_state.connection_timeout, 1)


def port_changed():
    dscript.port = st.session_state.port


def slowdown_changed():
    dscript.slowdown = st.session_state.slowdown


with st.expander("Advanced"):
    st.text('\n')
    st.number_input('Slowdown (s)', min_value=0.0, value=dscript.slowdown, step=0.01, format='%.3f',
                    key='slowdown', on_change=slowdown_changed,
                    help='Amount of time that the driver will wait for the relay before sending the next command.')

    st.number_input('Connection timeout (s)', min_value=0.0, value=dscript.connection_timeout, step=0.1, format='%.1f',
                    key='connection_timeout', on_change=change_timeout)

    st.number_input('Port', min_value=0, max_value=65535, value=dscript.port, step=1, key='port',
                    on_change=port_changed)

st.text('\n')
st.text('Copyright © 2023. LPQM')

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
