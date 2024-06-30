import ctypes
import os
import threading
import time

import pymem
import streamlit as st

from functions.rcs import rcs
from functions.trig import trig
from functions.esp import esp

st.set_page_config(page_title="QUANTICO.py",
                   page_icon="🚀",
                   layout="centered",
                   initial_sidebar_state="collapsed")
state = st.session_state

exit_app = st.sidebar.button("Shut Down")

if exit_app:
    time.sleep(3)
    os._exit(0)

try:
    pm = pymem.Pymem("cs2.exe")
    state.msg = st.toast("cs2.exe found! loading...", icon="🎉")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    time.sleep(1)
    state.msg.toast("Quantico.py loaded", icon="💯")
except pymem.exception.ProcessNotFound:
    st.error("cs2.exe not found!", icon="🚨")


keys = [
    "shift", "x", "x2", "alt", "ctrl", "insert", "home", "page up", "delete", "end",
    "page down", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11",
    "f12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "up", "left", "down",
    "right", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g",
    "h", "j", "k", "l","z", "x", "c", "v", "b", "n", "m", "-", "=", "backspace", "tab",
    "[", "]", "caps lock", ";", "'", "enter", ",", ".", "/", "num lock", "/", "*",
    "-", "+", "enter", "scroll lock", "pause", "`", ".", 
]

# App design + layout
with open("assets\style.css") as f:
    css = f.read()

# Custom title using CSS file
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.markdown('<h1 class="title-font">Quant<span style="color:black;">ico</span>🚀</h1>', unsafe_allow_html=True)

ballons = st.balloons()

tab1, tab2, tab3 = st.tabs(["Aim", "ESP", "Misc"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        enable_trigger = st.toggle("Enable trigger bot")
        if not enable_trigger:
            state.disable_keys = True
        else:
            state.disable_keys = False
        
        enable_rcs = st.toggle("Enable RCS")
        if not enable_rcs:
            state.disable_slider = True
        else:
            state.disable_slider = False
        
        state.enable_trigger = enable_trigger
        state.enable_rcs = enable_rcs
    
    with col2:
        trigkey = st.selectbox("Trigger bot key (*x* and *x2* are mouse side-butttons)",
                               keys, placeholder="Choose a key", disabled=state.disable_keys)
        amt = st.slider("RCS Amount", 0.0, 2.0, 2.0, 0.1, disabled=state.disable_slider)

with tab2:
    enable_esp = st.toggle("Enable ESP")
    state.enable_esp = enable_esp


# Create shared variables to signal the threads to stop
trigger_stop_flag = threading.Event()
rcs_stop_flag = threading.Event()
esp_stop_flag = threading.Event()


def run_trigger():
    while not trigger_stop_flag.is_set():
        if enable_trigger:
            trig(pm, client, trigkey)
            
            
def on_trigkey_change(new_key):
    # Check if tbot is running and stop it
    if state.tbot_thread is not None and state.tbot_thread.is_alive():
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(state.tbot_thread.ident),
            ctypes.py_object(SystemExit)
        )
        state.tbot_thread.join()
        
    # Refresh tbot with updated key
    state.tbot_thread = threading.Thread(target=run_trigger)
    state.tbot_thread.start()
    
            
def run_rcs():
    while not rcs_stop_flag.is_set():
        if enable_rcs:
            rcs(pm, client, amt)


def on_rcs_change(new_amt):
    # Check if rcs is running and stop it
    if state.rcs_thread is not None and state.rcs_thread.is_alive():
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(state.rcs_thread.ident),
            ctypes.py_object(SystemExit)
        )
        state.rcs_thread.join()
        
    # Refresh rcs with new amt
    state.rcs_thread = threading.Thread(target=run_rcs)
    state.rcs_thread.start()
            

def run_esp():
    while not esp_stop_flag.is_set():
        if enable_esp:
            esp(pm, client)


# Create a session state objects
if "tbot_thread" not in state:
    state.tbot_thread = None

state.trigkey = None
if trigkey != state.trigkey:
    state.trigkey = trigkey
    on_trigkey_change(trigkey)    
    
if "rcs_thread" not in state:
    state.rcs_thread = None

state.amt = None
if amt != state.amt:
    state.amt = amt
    on_rcs_change(amt)
    
if "esp_thread" not in state:
    state.esp_thread = None


# Check if the threads are running and start them if needed 
if state.tbot_thread is None or not state.tbot_thread.is_alive():
    state.tbot_thread = threading.Thread(target=run_trigger)
    state.tbot_thread.start()

if state.rcs_thread is None or not state.rcs_thread.is_alive():
    state.rcs_thread = threading.Thread(target=run_rcs)
    state.rcs_thread.start()

if state.esp_thread is None or not state.esp_thread.is_alive():
    state.esp_thread = threading.Thread(target=run_esp)
    state.esp_thread.start()


# Check if the checkboxes are unchecked and set the stop flags
if not enable_trigger:
    trigger_stop_flag.set()
    if state.tbot_thread.is_alive():
        # Workaround to ensure the thread stops properly
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(state.tbot_thread.ident),
            ctypes.py_object(SystemExit)
        )
        state.tbot_thread.join()

if not enable_rcs:
    rcs_stop_flag.set()
    if state.rcs_thread.is_alive():
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(state.rcs_thread.ident),
            ctypes.py_object(SystemExit)
        )
        state.rcs_thread.join()

if not enable_esp:
    esp_stop_flag.set()
    if state.esp_thread.is_alive():
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(state.esp_thread.ident),
            ctypes.py_object(SystemExit)
        )
        state.esp_thread.join()
