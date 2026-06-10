# Sigma-Enigma

Bildbasierte Caesar-Verschluesselung als Streamlit-App. Der Schluessel entsteht
aus den Farbwerten der ersten 100 Pixel eines hochgeladenen Bildes.

> ⚠️ Hinweis: Dies ist eine Caesar-Chiffre und bietet **keinen echten
> kryptografischen Schutz**. Gedacht als Spaß- und Lernprojekt.

## Lokal starten

```bash
pip install -r requirements.txt
streamlit run Sigma-Enigma.py
```

## Online stellen mit Streamlit Community Cloud (kostenlos)

### 1. Code auf GitHub legen
1. Kostenloses Konto auf https://github.com anlegen (falls noch nicht vorhanden).
2. Neues Repository erstellen, z. B. `sigma-enigma` (Public).
3. Diese Dateien hochladen:
   - `Sigma-Enigma.py`
   - `requirements.txt`
   - `README.md` (optional)

### 2. Bei Streamlit Cloud deployen
1. Auf https://share.streamlit.io gehen und mit GitHub einloggen.
2. Auf **"Create app" / "New app"** klicken.
3. Auswaehlen:
   - **Repository:** dein-name/sigma-enigma
   - **Branch:** main
   - **Main file path:** `Sigma-Enigma.py`
4. Auf **"Deploy"** klicken.

Nach ~1 Minute ist die App unter einer oeffentlichen URL erreichbar, z. B.
`https://dein-name-sigma-enigma.streamlit.app` — diese Adresse kann jeder
aufrufen.

### Updates
Jeder neue Commit/Push auf GitHub wird automatisch live deployed.
