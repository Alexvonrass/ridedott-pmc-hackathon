import base64
import io

import dash
import numpy as np
import soundfile as sf
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash_recording_components import AudioRecorder

from ridedott_pmc_hackathon.constants import language_dropdown_options

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Language Selector and Chat Interface with Audio Recording"),
        html.Label("Doctor's Language"),
        dcc.Dropdown(
            id="doctors-language-dropdown",
            options=language_dropdown_options,
            value=language_dropdown_options[0]["value"],
            clearable=False,
        ),
        html.Label("Patient's Language"),
        dcc.Dropdown(
            id="patients-language-dropdown",
            options=language_dropdown_options
            + [{"label": "Unknown", "value": "unknown"}],
            value="unknown",
            clearable=False,
        ),
        html.Div(            [
                
                html.Div([
                            html.P("This is another Div containing a paragraph."),
                            html.P("Another paragraph for demonstration."),
                            html.P("Another paragraph for demonstration.")
                        ]),
                ## below interval block updates every second with new text info
                dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
        )
            ],
            id="chat-window",

            style={
                "border": "1px solid #ccc",
                "width": "80%",
                "height": "400px",
                "margin": "auto",
                "padding": "10px",
                "overflow-y": "auto",
            },

        ),
        html.Button("Record Audio", id="record-button", n_clicks=0),
        html.Button("Stop Recording", id="stop-button", n_clicks=0),
        html.Button("Play Audio", id="play-button", n_clicks=0),
        html.Div(id="audio-output"),
        AudioRecorder(id="audio-recorder"),
        html.Div(
            id="dummy-output", style={"display": "none"}
        ),  # Dummy output to handle state updates invisibly
    ]
)

audio_samples = []  # Initialize a global variable to store audio samples


@app.callback(
    Output("audio-recorder", "recording"),
    Input("record-button", "n_clicks"),
    Input("stop-button", "n_clicks"),
    State("audio-recorder", "recording"),
    prevent_initial_call=True,
)
def control_recording(record_clicks, stop_clicks, recording):
    triggered = dash.callback_context.triggered[0]["prop_id"]
    if "record-button" in triggered:
        return True
    elif "stop-button" in triggered:
        return False
    return recording


@app.callback(
    Output("dummy-output", "children"),
    Input("audio-recorder", "audio"),
    prevent_initial_call=True,
)
def update_audio(audio):
    global audio_samples
    if audio is not None:
        # Convert dictionary values to a list of samples
        current_samples = list(audio.values())
        audio_samples.extend(current_samples)
    return ""


@app.callback(
    Output("audio-output", "children"),
    Input("play-button", "n_clicks"),
    prevent_initial_call=True,
)
def play_audio(play_clicks):
    if audio_samples:
        audio_array = np.array(audio_samples)
        with io.BytesIO() as wav_buffer:
            sf.write(wav_buffer, audio_array, 16000, format="WAV")
            wav_bytes = wav_buffer.getvalue()
            wav_base64 = base64.b64encode(wav_bytes).decode()
            audio_src = f"data:audio/wav;base64,{wav_base64}"
            return html.Audio(src=audio_src, controls=True)
    return "No audio recorded."


if __name__ == "__main__":
    app.run_server(debug=True, )
