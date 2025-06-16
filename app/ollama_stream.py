import requests
import json
import time
import streamlit as st

def stream_from_ollama(prompt: str):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "phi3:mini",
        "prompt": prompt,
        "stream": True
    }
    with requests.post(url, json=payload, stream=True) as response:
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        yield data["response"]
                except json.JSONDecodeError:
                    continue

def stream_response_to_streamlit(prompt: str):
    placeholder = st.empty()
    output = ""
    for chunk in stream_from_ollama(prompt):
        output += chunk
        placeholder.markdown(output + "▌")
        time.sleep(0.02)  # control typing speed
    placeholder.markdown(output)
