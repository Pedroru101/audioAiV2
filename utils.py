"""Utility functions for the Audio Capture Widget.
All functions are stateless helpers so they can be reused from both the UI
thread and worker threads safely.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, Tuple, List

import requests
from scipy.io import wavfile
import numpy as np

# Path to configuration file (alongside this utils.py file)
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

__all__ = [
    "load_config",
    "save_config",
    "merge_audio_files",
    "send_to_webhook",
    "load_history",
    "save_history",
]

DEFAULT_CONFIG: Dict[str, Any] = {
    "input_device_index": None,
    "output_device_index": None,
    "n8n_webhook_url": "http://localhost:5678/webhook/audio",
    "max_duration_minutes": 0,
}

# Path to recording history file (alongside this utils.py file)
HISTORY_PATH: str = os.path.join(os.path.dirname(__file__), "history.json")

def load_history() -> List[Dict[str, Any]]:
    """Load recording history from *history.json*."""
    if not os.path.exists(HISTORY_PATH):
        return []
    with open(HISTORY_PATH, "r", encoding="utf-8") as fp:
        return json.load(fp)

def save_history(history: List[Dict[str, Any]]) -> None:
    """Save recording history to *history.json*."""
    try:
        with open(HISTORY_PATH, "w", encoding="utf-8") as fp:
            json.dump(history, fp, indent=2, ensure_ascii=False)
    except IOError as exc:
        logging.error("Unable to save history: %s", exc)
        raise


def _ensure_config_exists() -> None:
    """Create a default config.json if it does not yet exist."""
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        save_config(DEFAULT_CONFIG)


# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

def load_config() -> Dict[str, Any]:
    """Load configuration from *config.json*.

    Returns
    -------
    dict
        The parsed configuration. If the file does not exist, a default file is
        created and its contents returned.
    """
    _ensure_config_exists()
    with open(CONFIG_PATH, "r", encoding="utf-8") as fp:
        return json.load(fp)


def save_config(data: Dict[str, Any]) -> None:
    """Persist *data* to *config.json*.

    Parameters
    ----------
    data : dict
        Data to save. Should be JSON-serialisable.
    """
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2, ensure_ascii=False)
    except IOError as exc:
        logging.error("Unable to save configuration: %s", exc)
        raise


# ---------------------------------------------------------------------------
# Audio processing helpers
# ---------------------------------------------------------------------------

def merge_audio_files(mic_path: str, sys_path: str, output_path: str) -> None:
    """Mezcla dos archivos WAV sumando sus muestras y normalizando para evitar clipping."""
    logging.info("Merging '%s' + '%s' -> '%s'", mic_path, sys_path, output_path)
    sr_mic, mic_data = wavfile.read(mic_path)
    sr_sys, sys_data = wavfile.read(sys_path)

    # Convertir a float para evitar overflow
    mic_data = mic_data.astype(np.float32)
    sys_data = sys_data.astype(np.float32)

    # Igualar longitudes
    max_len = max(len(mic_data), len(sys_data))
    if len(mic_data) < max_len:
        mic_data = np.pad(mic_data, ((0, max_len - len(mic_data)), (0,0)) if mic_data.ndim==2 else (0, max_len - len(mic_data)), mode='constant')
    if len(sys_data) < max_len:
        sys_data = np.pad(sys_data, ((0, max_len - len(sys_data)), (0,0)) if sys_data.ndim==2 else (0, max_len - len(sys_data)), mode='constant')

    # Mezclar (suma)
    mixed = mic_data + sys_data
    # Normalizar para evitar clipping
    max_abs = np.max(np.abs(mixed))
    if max_abs > 0:
        mixed = mixed / max_abs * 32767
    mixed = mixed.astype(np.int16)
    wavfile.write(output_path, sr_mic, mixed)



# ---------------------------------------------------------------------------
# Networking helpers
# ---------------------------------------------------------------------------

def send_to_webhook(url: str, file_path: str, final_chunk: bool = False, timeout: int = 5) -> Tuple[bool, str]:
    """Send *file_path* to *url* as multipart/form-data.

    Returns *(success, message)* where *success* is ``True`` when the request
    completed with a 2xx status code.
    """
    logging.info("Uploading '%s' to webhook '%s'", file_path, url)
    try:
        # Determinar el Content-Type correcto basado en la extensión
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.mp3':
            content_type = "audio/mpeg"
        elif file_extension == '.wav':
            content_type = "audio/wav"
        else:
            content_type = "audio/mpeg"  # Default fallback
        
        with open(file_path, "rb") as fp:
            files = {"file": (os.path.basename(file_path), fp, content_type)}
            data = {"final_chunk": str(final_chunk).lower()}
            response = requests.post(url, files=files, data=data, timeout=timeout)
        response.raise_for_status()
        logging.info("Webhook upload succeeded: %s", response.status_code)
        return True, response.text
    except requests.RequestException as exc:
        logging.error("Webhook upload failed: %s", exc)
        return False, str(exc)
