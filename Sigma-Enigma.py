import base64
from pathlib import Path
import io

from PIL import Image
import streamlit as st

NUM_PIXELS = 100


def build_keystream(img):
    """Liest die ersten NUM_PIXELS Pixel und erzeugt Keystream."""
    img = img.convert("RGB")
    width, height = img.size
    count = min(NUM_PIXELS, width * height)
    pixels = [img.getpixel((i % width, i // width)) for i in range(count)]
    keystream = [value for pixel in pixels for value in pixel]
    return keystream


def caesar(text, keystream, decrypt=False):
    """Caesar-Verschlüsselung mit Bild-basiertem Schlüssel."""
    out = []
    j = 0
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


# ---------------- UI ----------------

st.set_page_config(page_title="Sigma-Enigma", page_icon="icon.png", layout="centered")

st.title("Sigma-Enigma")
st.caption(
    "Bildbasierte Caesar-Verschlüsselung — der Schlüssel entsteht aus den Pixelwerten."
)

if "result" not in st.session_state:
    st.session_state.result = ""
    st.session_state.result_label = ""


col_in, col_key = st.columns(2)

with col_in:
    text = st.text_area(
        "Text",
        height=160,
        placeholder="Hier deinen geheimen Text eingeben …",
    )

with col_key:
    uploaded = st.file_uploader(
        "Schlüsselbild hochladen",
        type=["jpg", "jpeg", "png", "bmp", "gif"],
    )

    camera_image = st.camera_input("Oder Foto aufnehmen")

    image_source = camera_image if camera_image is not None else uploaded


# ---------------- Bildanzeige + Download ----------------

if image_source is not None:
    st.image(image_source, caption="Schlüsselbild", use_container_width=True)

    img = Image.open(image_source)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    st.download_button(
        label="Schlüsselbild herunterladen",
        data=buffer,
        file_name="enigma_key_image.png",
        mime="image/png",
    )


st.divider()

# ---------------- Buttons ----------------

btn_enc, btn_dec = st.columns(2)
do_encrypt = btn_enc.button("Verschlüsseln", use_container_width=True, type="primary")
do_decrypt = btn_dec.button("Entschlüsseln", use_container_width=True)

if do_encrypt or do_decrypt:
    if not text:
        st.warning("Bitte zuerst einen Text eingeben.")
    elif image_source is None:
        st.warning("Bitte zuerst ein Schlüsselbild hochladen oder aufnehmen.")
    else:
        img = Image.open(image_source)
        keystream = build_keystream(img)

        decrypt = do_decrypt
        st.session_state.result = caesar(text, keystream, decrypt=decrypt)
        st.session_state.result_label = "Entschlüsselt" if decrypt else "Verschlüsselt"


# ---------------- Output ----------------

if st.session_state.result:
    st.subheader(st.session_state.result_label)
    st.code(st.session_state.result, language=None)