# AffiliateFlow AI

**Product link → verified product brief → affiliate content package → voice-over → short video draft**

This is the first local MVP scaffold for the AffiliateFlow AI project. It is designed for Windows and beginner users.

## What this version does

- Accepts an affiliate product URL (the URL is kept as the affiliate destination; it is not scraped).
- Lets you enter product facts from the manufacturer's/retailer's public product page.
- Uses the Gemini API to draft a product brief, short-video scripts, captions, hashtags, and a visual shot list.
- Can create a voice-over audio file using Edge TTS.
- Can assemble a simple vertical MP4 draft from images you provide and the generated voice-over.

## What it does NOT do yet

- It does not automatically access Amazon Associates data or scrape Amazon pages.
- It does not generate original product photographs by itself in this first version. It creates a visual brief and accepts images you have permission to use.
- It does not auto-publish to YouTube, TikTok, or Instagram.
- It does not guarantee sales, commissions, platform reach, or Amazon Associates approval.

## Important affiliate and age note

Use only product images, logos, music, and footage you own or are licensed to use. Do not claim that you personally tested a product unless you really did. Check product claims against the official source. Clearly disclose affiliate relationships (for example: “I may earn a commission from qualifying purchases”). Follow each platform's branded-content rules and the affiliate program's terms. Amazon Associates participation and payment setup have eligibility and age requirements; if you are under 18, ask a parent/guardian to review the rules and handle any account that legally requires an adult.

## 1. Install on Windows

1. Install Python 3.11 or newer from https://www.python.org/downloads/ (tick **Add Python to PATH**).
2. Install FFmpeg from https://ffmpeg.org/download.html and make sure `ffmpeg` works in Command Prompt.
3. Extract this ZIP.
4. Open the extracted `AffiliateFlow-AI` folder.
5. Double-click `setup_windows.bat`.
6. Copy `.env.example` to `.env` and add your Gemini API key.
7. Double-click `run_windows.bat`.

The app should open in your browser at `http://localhost:8501`.

## 2. Get a Gemini API key

Create a key in Google AI Studio: https://aistudio.google.com/app/apikey

Keep the key private. Never paste it into GitHub, screenshots, or public chats. The app reads it from `.env`.

## 3. Basic workflow

1. Paste your affiliate product URL.
2. Enter the product name and factual features from an official source.
3. Choose the target platform and video language.
4. Generate the content package.
5. Review every factual statement and edit anything inaccurate.
6. Generate voice-over audio.
7. Upload permitted product images and assemble a draft video.
8. Review the final video and disclosure before publishing it yourself.

## 4. Upload this project to GitHub

Open your repository `https://github.com/abuhanif-emon/AffiliateFlow-AI`, choose **Add file → Upload files**, drag the extracted project files/folders into the page, then choose **Commit changes**. Do not upload `.env`, API keys, generated private data, or large media files.

## Project layout

```text
AffiliateFlow-AI/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── setup_windows.bat
├── run_windows.bat
├── config/
│   └── platforms.json
├── prompts/
│   ├── product_research.md
│   ├── content_package.md
│   ├── visual_brief.md
│   └── quality_check.md
├── docs/
│   ├── workflow.md
│   └── compliance.md
└── output/
    └── .gitkeep
```

## Troubleshooting

- **Python not found:** reinstall Python and tick “Add Python to PATH”.
- **FFmpeg not found:** install FFmpeg, reopen Command Prompt, and run `ffmpeg -version`.
- **Gemini error:** check the API key in `.env`, internet connection, and current API/model availability.
- **Amazon page won't load:** expected; this MVP does not scrape Amazon. Enter facts manually from official product information.
- **Video has no audio:** generate the voice-over first, then assemble the video.
