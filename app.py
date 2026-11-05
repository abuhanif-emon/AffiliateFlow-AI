import asyncio
import json
import os
import re
import tempfile
from pathlib import Path

import edge_tts
import streamlit as st
from dotenv import load_dotenv
from google import genai
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips

load_dotenv()
ROOT = Path(__file__).parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

st.set_page_config(page_title="AffiliateFlow AI", page_icon="🎬", layout="wide")
st.title("🎬 AffiliateFlow AI")
st.caption("Product link → content package → voice-over → short-video draft")

st.info("This is an early MVP. The product URL is saved as your affiliate destination; this app does not scrape Amazon or verify facts from the URL. Enter product facts from an official source and check all AI output before publishing.")

api_key = os.getenv("GEMINI_API_KEY", "").strip()
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

with st.sidebar:
    st.header("Setup")
    if api_key and api_key != "PASTE_YOUR_KEY_HERE":
        st.success("Gemini API key detected")
    else:
        st.warning("Add GEMINI_API_KEY to your .env file")
    st.write("Platforms: YouTube Shorts · TikTok · Instagram Reels")
    st.write("Output folder:", str(OUT))

st.subheader("1. Product information")
with st.form("product_form"):
    product_url = st.text_input("Affiliate product URL", placeholder="Paste your affiliate link")
    product_name = st.text_input("Product name")
    product_facts = st.text_area(
        "Verified product features (paste facts from an official product source)",
        placeholder="Example: Officially listed capacity, dimensions, compatibility, included items...",
        height=140,
    )
    audience = st.text_input("Target audience", value="People researching this product")
    language = st.selectbox("Content language", ["English", "Bangla"])
    platform = st.multiselect(
        "Platforms",
        ["YouTube Shorts", "TikTok", "Instagram Reels"],
        default=["YouTube Shorts", "TikTok", "Instagram Reels"],
    )
    tone = st.selectbox("Video tone", ["Helpful and professional", "Friendly and simple", "Feature-focused"])
    submitted = st.form_submit_button("Generate content package", type="primary")

if submitted:
    if not product_url.startswith(("https://", "http://")):
        st.error("Please enter a valid http(s) affiliate URL.")
    elif not product_name.strip() or not product_facts.strip():
        st.error("Enter the product name and factual product details.")
    elif not api_key or api_key == "PASTE_YOUR_KEY_HERE":
        st.error("Gemini API key missing. Add it to .env and restart the app.")
    elif not platform:
        st.error("Select at least one platform.")
    else:
        prompt = f"""
You are the content assistant for AffiliateFlow AI.
Create a responsible affiliate short-video content package.

Product name: {product_name}
Affiliate destination URL: {product_url}
User-supplied product facts (not independently verified): {product_facts}
Audience: {audience}
Language: {language}
Platforms: {", ".join(platform)}
Tone: {tone}

Rules:
- Use ONLY the supplied facts for product claims. Do not invent price, discount, rating, reviews, warranty, availability, performance, or personal testing.
- Clearly label any fact needing verification as [CHECK].
- Do not claim the creator personally used/tested the product.
- Include a clear affiliate disclosure in every platform caption/script.
- No fake urgency, guarantees, or fabricated testimonials.
- Make a platform-specific package for each selected platform.
- Include: 3 hooks, 20-40 second voice-over script, scene-by-scene storyboard with visual guidance, on-screen captions, post caption, title, hashtags, and final fact-check checklist.
- Keep the script natural and useful, not pushy.
"""
        try:
            with st.spinner("Generating content with Gemini..."):
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(model=model_name, contents=prompt)
                result = response.text or "No text returned."
                st.session_state["content_result"] = result
                st.session_state["product_name"] = product_name
                st.session_state["product_url"] = product_url
                (OUT / "content_package.md").write_text(result, encoding="utf-8")
        except Exception as exc:
            st.error(f"Generation failed: {exc}")

if "content_result" in st.session_state:
    st.subheader("2. Generated content package")
    st.markdown(st.session_state["content_result"])
    st.download_button(
        "Download content package (.md)",
        st.session_state["content_result"],
        file_name="affiliate_content_package.md",
        mime="text/markdown",
    )

    st.subheader("3. Create voice-over")
    voice_text = st.text_area("Review and edit the voice-over script, then generate audio", height=180)
    voice_options = {
        "English - US Female": "en-US-JennyNeural",
        "English - US Male": "en-US-GuyNeural",
        "Bangla - Bangladesh Female": "bn-BD-NabanitaNeural",
        "Bangla - Bangladesh Male": "bn-BD-PradeepNeural",
    }
    voice_label = st.selectbox("Voice", list(voice_options.keys()))
    if st.button("Generate voice-over audio"):
        if not voice_text.strip():
            st.warning("Paste the final voice-over script first.")
        else:
            try:
                audio_path = OUT / "voiceover.mp3"
                async def make_audio():
                    communicate = edge_tts.Communicate(voice_text, voice_options[voice_label])
                    await communicate.save(str(audio_path))
                with st.spinner("Creating voice-over..."):
                    asyncio.run(make_audio())
                st.success("Voice-over created.")
                st.audio(str(audio_path))
                st.download_button("Download voice-over MP3", audio_path.read_bytes(), "voiceover.mp3", "audio/mpeg")
            except Exception as exc:
                st.error(f"Voice-over failed: {exc}")

    st.subheader("4. Assemble a simple vertical video draft")
    st.write("Upload 1–8 product photos or licensed visuals. The app will make a basic slideshow with the voice-over. This is a draft, not a finished ad.")
    images = st.file_uploader("Upload permitted images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if st.button("Build 9:16 MP4 draft"):
        audio_path = OUT / "voiceover.mp3"
        if not images:
            st.warning("Upload at least one image.")
        elif not audio_path.exists():
            st.warning("Generate the voice-over first.")
        else:
            temp_paths = []
            clips = []
            audio = None
            try:
                with st.spinner("Building video draft..."):
                    for i, uploaded in enumerate(images[:8]):
                        suffix = Path(uploaded.name).suffix.lower() or ".jpg"
                        p = OUT / f"visual_{i+1}{suffix}"
                        p.write_bytes(uploaded.getvalue())
                        temp_paths.append(p)
                    audio = AudioFileClip(str(audio_path))
                    per_image = max(2.5, audio.duration / len(temp_paths))
                    for p in temp_paths:
                        clip = ImageClip(str(p)).with_duration(per_image)
                        # Crop/fit to vertical 9:16 canvas.
                        w, h = clip.size
                        target_ratio = 9 / 16
                        if w / h > target_ratio:
                            new_w = int(h * target_ratio)
                            x1 = max(0, (w - new_w) // 2)
                            clip = clip.cropped(x1=x1, y1=0, x2=x1 + new_w, y2=h)
                        else:
                            new_h = int(w / target_ratio)
                            y1 = max(0, (h - new_h) // 2)
                            clip = clip.cropped(x1=0, y1=y1, x2=w, y2=y1 + new_h)
                        clip = clip.resized(height=1920)
                        clips.append(clip)
                    video = concatenate_videoclips(clips, method="compose")
                    video = video.with_duration(audio.duration).with_audio(audio)
                    video_path = OUT / "affiliate_short_draft.mp4"
                    video.write_videofile(str(video_path), fps=24, codec="libx264", audio_codec="aac", logger=None)
                    st.success("Video draft created.")
                    st.video(str(video_path))
                    st.download_button("Download MP4 draft", video_path.read_bytes(), "affiliate_short_draft.mp4", "video/mp4")
            except Exception as exc:
                st.error(f"Video build failed: {exc}. Check that FFmpeg is installed and available in PATH.")
            finally:
                for c in clips:
                    try: c.close()
                    except Exception: pass
                if audio:
                    try: audio.close()
                    except Exception: pass

st.divider()
st.caption("Before publishing: verify every product claim, use licensed media, add a clear affiliate disclosure, and publish manually after review.")
