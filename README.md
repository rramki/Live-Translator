# 🌐 Live Audio Translator

A real-time speech-to-translation Streamlit app powered by **Claude AI** and the browser's **Web Speech API**.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)

---

## ✨ Features

- 🎤 **Live microphone capture** — no server-side audio processing needed
- 🔁 **Continuous listening** — auto-restarts after each sentence
- 💬 **Dual scrolling panels** — transcript on the left, translation on the right
- ⚡ **Real-time** — translates each sentence as it's finalized
- 🌐 **18 languages** — Spanish, French, Japanese, Arabic, Hindi, and more
- 📱 **Mobile-friendly** — responsive layout for handheld devices

---

## 🚀 Deploy to Streamlit Cloud

### 1. Fork / Clone this repo

```bash
git clone https://github.com/YOUR_USERNAME/live-translator.git
cd live-translator
```

### 2. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/live-translator.git
git push -u origin main
```

### 3. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select your GitHub repo and set **Main file path** to `app.py`
4. Click **"Deploy"**

### 4. Add your Anthropic API Key as a Secret

In Streamlit Cloud dashboard → your app → **Settings** → **Secrets**, add:

```toml
# No secrets needed server-side — API key is entered by the user in the sidebar
```

> The API key is entered by users directly in the sidebar UI. No server-side secrets required.

---

## 🛠 Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in **Chrome** or **Edge**.

---

## 🌍 Supported Languages

| Source | Target |
|--------|--------|
| English, Spanish, French, German | Spanish, French, German, Japanese |
| Japanese, Korean, Chinese | Korean, Chinese (Simplified), Arabic |
| Arabic, Portuguese, Italian | Portuguese, Italian, Russian |
| Russian, Hindi, Auto-detect | Hindi, Turkish, Dutch, Polish... |

---

## 🔑 Getting an Anthropic API Key

1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Sign up / log in
3. Go to **API Keys** → **Create Key**
4. Paste it in the app sidebar

---

## ⚠️ Browser Compatibility

| Browser | Support |
|---------|---------|
| Chrome (Desktop & Android) | ✅ Full |
| Edge (Desktop) | ✅ Full |
| Safari (iOS) | ⚠️ Limited |
| Firefox | ❌ Not supported |

---

## 📁 Project Structure

```
live-translator/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml        # Theme & server configuration
└── README.md              # This file
```

---

## 📄 License

MIT License — free to use, modify, and distribute.
