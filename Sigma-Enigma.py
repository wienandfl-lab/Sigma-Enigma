import base64
from pathlib import Path

from PIL import Image
import streamlit as st

NUM_PIXELS = 100


def build_keystream(img):
    """Liest die ersten NUM_PIXELS Pixel eines Bildes und gibt die Farbwerte
    (0-255) als flache Liste von Verschiebungswerten zurueck: [r, g, b, ...]."""
    img = img.convert("RGB")
    width, height = img.size
    count = min(NUM_PIXELS, width * height)
    pixels = [img.getpixel((i % width, i // width)) for i in range(count)]
    keystream = [value for pixel in pixels for value in pixel]
    return keystream


def caesar(text, keystream, decrypt=False):
    """Caesar-Verschluesselung mit fortlaufendem Schluessel: jeder Buchstabe
    wird um den naechsten Schluesselwert (mod 26) verschoben. Nicht-Buchstaben
    bleiben unveraendert. Der Schluessel wird bei langem Text zyklisch wiederholt."""
    out = []
    j = 0  # zaehlt nur Buchstaben, damit Ent-/Verschluesselung deckungsgleich ist
    n = len(keystream)
    for ch in text:
        if "a" <= ch <= "z":
            base = ord("a")
        elif "A" <= ch <= "Z":
            base = ord("A")
        else:
            out.append(ch)
            continue
        shift = keystream[j % n] % 26
        if decrypt:
            shift = -shift
        out.append(chr((ord(ch) - base + shift) % 26 + base))
        j += 1
    return "".join(out)


# ---------------------------------------------------------------- UI ----------

st.set_page_config(page_title="Sigma-Enigma", page_icon="icon.png", layout="centered")

st.title("Sigma-Enigma")
st.caption("Bildbasierte Caesar-Verschluesselung — der Schluessel entsteht aus "
           "den Farbwerten der ersten 100 Pixel deines Bildes.")

if "result" not in st.session_state:
    st.session_state.result = ""
    st.session_state.result_label = ""

col_in, col_key = st.columns(2)

with col_in:
    text = st.text_area("Text", height=160, placeholder="Hier deinen Text eingeben …")

with col_key:
    uploaded = st.file_uploader(
        "Schluessel-Bild (hochladen oder hierher ziehen)",
        type=["jpg", "jpeg", "png", "bmp", "gif"],
    )
    if uploaded is not None:
        st.image(uploaded, caption="Schluessel-Bild", use_container_width=True)

st.divider()

btn_enc, btn_dec = st.columns(2)
do_encrypt = btn_enc.button("Verschluesseln", use_container_width=True, type="primary")
do_decrypt = btn_dec.button("Entschluesseln", use_container_width=True)

if do_encrypt or do_decrypt:
    if not text:
        st.warning("Bitte zuerst einen Text eingeben.")
    elif uploaded is None:
        st.warning("Bitte zuerst ein Schluessel-Bild hochladen.")
    else:
        keystream = build_keystream(Image.open(uploaded))
        decrypt = do_decrypt
        st.session_state.result = caesar(text, keystream, decrypt=decrypt)
        st.session_state.result_label = "Entschluesselt" if decrypt else "Verschluesselt"

if st.session_state.result:
    st.subheader(st.session_state.result_label)
    # st.code zeigt oben rechts automatisch ein Kopier-Symbol zum Kopieren.
    st.code(st.session_state.result, language=None)


