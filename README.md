# AI Content Production Engine — Virtual Studio v0.2

Windows local FB Pro studio with GPT orchestration, live trend intake, offline Indonesian neural voice and event-driven office. There are 10 roles; the Researcher, Strategist, Script Writer and Policy Auditor call GPT separately in plan/API modes. Other roles are software workers. The workflow is sequential, with recorded artifact handoffs, not autonomous parallel conversations or simulated background activity.

## Install on drive D:
1. Clone/download this project to D:\AI-Content-Production-Engine. Existing Python 3.11, Node.js >=22.12, Git and Windows PowerShell are prerequisites.
2. Run INSTALL-D.cmd to install rendering dependencies to vendor/. Run INSTALL-VOICE-ID.cmd for the local voice model. Run INSTALL-GPT-PLAN.cmd for the official OpenAI SIWC local DevKit.
3. Run START-STUDIO.cmd, visit http://127.0.0.1:8899/. Only listen on IPv4 loopback. Do not expose to the internet. All vendor, temp, voice, job data and credential files are stored on D:. Existing Python/browser/Windows may still use C: for normal OS operations.
4. In the Studio select Continue with ChatGPT, choose your own account/workspace, authorize plan usage, and return to the dashboard. Verify the displayed account and select an available model. Choose GPT plan mode and explicitly permit its plan usage for the job. Manage your allowance via ChatGPT Settings → Usage. Disconnect via the dashboard or revoke in ChatGPT settings.
5. Alternative modes: Demo (built-in script), Manual (paste 3–6 JSON scenes from a dedicated ChatGPT project chat), API (separate paid API; requires OPENAI_API_KEY and OPENAI_MODEL environment variables and per-job consent).

## GPT account safety
Uses official OpenAI Sign in with ChatGPT SDK, pinned source commit 0a36fefeb913055c8c7a1a29b63d82b96b2e841a, with local Windows CurrentUser DPAPI protection for credentials. Browser login/consent is exclusively user-controlled. No access to existing ChatGPT conversations, cookies, passwords or OTP. Identity alone does not enable plan usage. No paid API fallback. ChatGPT plan availability and limits depend on account/workspace. Never upload private/ or credential data. The installer audits runtime dependencies; remediate reported vulnerabilities before enabling sign-in. The SDK's own license and OpenAI SIWC terms apply.
- https://developers.openai.com/siwc/token-sharing-open-source
- https://github.com/openai/sign-in-with-chatgpt-devkit
- https://openai.com/policies/sign-in-with-chatgpt-terms/

## Trends
The public Google Trends Indonesia RSS is queried when the user enables trends. Store timestamped source and titles in trends.json, then pass it as untrusted evidence to GPT in live modes. It measures Google search interest, not Facebook performance or factual proof. A failed feed is explicitly marked unavailable. No Facebook scraping. GPT must not invent source URLs, metrics or earnings. Verify every factual claim before publication.

## Audio and production
Demo/manual/ChatGPT plan modes use local Piper Indonesian id_ID news_tts medium, installed separately on D:. The model is for local preview until the owner reviews the dataset license; its model card points to an external dataset license. Do not assume commercial rights. API mode uses OpenAI text-to-speech instead and is separately billed. WAVs are checked for non-silence and video decoded by FFmpeg. Preview video may be shorter than target Reel duration: based on actual narration duration. No Facebook posting. Owner checks accuracy, audio/visual rights and disclosure before uploading.

## Virtual office
Ten characters at individual desks, a meeting room and separate render area. Backend records each completed artifact handoff with sender/receiver. Live rendering displays status; optional labeled replay of recorded handoffs displays the two characters meeting. Rapid stages may complete between polls. This is a lightweight visual representation, not a claim of extra computation.
- Pixel Agents: https://www.youtube.com/watch?v=KtG5Ez7KujE
- Local real-time office: https://www.youtube.com/watch?v=knZuRQi2Gag

## Acceptance
Run node chatgpt-plan.mjs selftest (DPAPI only), python -B studio_services.py --trends, python -B studio_services.py --voice, python -B app.py --demo --trends. Optional browser test: start server, then node test-ui.cjs with PLAYWRIGHT_MODULE set to an existing Playwright installation. Tests check two production jobs, handoff replay, real trend feed, media decode and local consent/origin validation. No authenticated model inference is claimed unless the owner signs in and a real request completes.
The prior Control Center at D:\AI-COMPUTER-CONTROL remains independent. No DC required during normal Studio operation. Public repository contains source and installers only; private data, credentials, media and model binaries are excluded.

## Desktop shortcut
Run `python -B make-icon.py` and `powershell -NoProfile -File UPDATE-DESKTOP.ps1` after installation or an icon design change. `START-STUDIO.cmd` refreshes the desktop shortcut on startup and recreates the icon if missing. The shortcut points to the stable D-drive launcher. On OneDrive-managed desktops the small .lnk file may reside on C:, while the icon and program remain on D:.

## Real GPT-plan acceptance
After a completed GPT-6.2 plan job, run `python -B verify-plan-job.py JOB_ID`. The verifier checks the role completion records, live trend source, actual non-silent WAVs, video hash, artifact existence, and 10 handoffs without making new model calls. `python -B test-narration.py` checks clean spoken text and rejects obvious narration labels and timecoded headlines. A technical pass is not publication approval. The renderer uses illustrative cards for plan-mode content, not genuine screen recordings. Verify content, audio rights, and visual accuracy before posting.

## Notebook Media Bridge (v0.2.1)
Open the companion from the Studio sidebar or run START-NOTEBOOK-BRIDGE.cmd. User-controlled integration: select a completed GPT job, enter verified non-private source notes, inspect the exported markdown and prompts, then manually upload to https://notebook.google.com/. Generate Indonesian Audio/Video Overview using the user's Google account, download it and import the actual file for local FFmpeg QC. No consumer API, automated login, or automatic upload. Video is padded to 720x1280 without deliberate watermark removal; audio is loudness-normalized. This does not validate facts or authorize commercial use. All imported assets remain preview-only; review Google terms and source/voice rights separately. Piper voice model card references an external dataset; commercial rights remain unresolved. 
For Facebook, use the companion's CSV template with actual owner-authorized per-content metrics and timezone-aware publication/observation timestamps. Compare 24h, 72h and 7d cohorts; missing metrics remain unknown. The generated analytics work order can be pasted into the project ChatGPT conversation. Meta Page Insights API does not establish access to personal professional-mode profiles. No scraping, no auto-publication. 
Run python -B notebook_bridge.py --selftest for synthetic media import, QC, rights gate and cohort calculations. Actual Notebook outputs and Facebook metrics are not included in tests.

### Imported Notebook media catalog (v0.2.2)
Run `python -B import-notebook-pair.py notebook-workspace/PROJECT` with exactly one original audio and one original video in that local folder. The utility imports both with Notebook Media Bridge, checks duration and audio loudness/peak, samples six video frames and writes `integrated-media.json`. The local Studio catalog lists completed pairs and opens the corresponding output folders. Preview-only; no posting or commercial approval. Keep all media, reports and source notes local. Audio quality measurements do not establish content accuracy or pronunciation. Review true peak after AAC encoding.

### Monetization readiness (local, no auto-publication)
- Run `python -B repair-true-peak.py PROJECT` after paired Notebook import. The script writes review-safe.wav/mp4, preserves original exports, verifies decoded true peak <= -1.5 dBTP and saves true-peak-qc.json. Video stream is copied, not re-encoded.
- Optional local Indonesian transcription: run INSTALL-ASR.cmd from D:, then `python -B transcribe-notebook.py PROJECT`. Uses faster-whisper base CPU int8, four threads, with model cache and packages on D:. ASR output is not a certified verbatim transcript; human review of pronunciation and factual claims is required. No audio uploads or paid API.
- Run `python -B monetization-readiness.py PROJECT` to record the conditional rights audit, technical status, and available owner-supplied metrics. Google account terms and source rights must be checked separately. No automatic commercial clearance or publication approval. Use the existing Notebook Media Bridge CSV template for actual per-content insights; blank values remain unknown. Source material, media, transcripts, metrics and reports are excluded from public GitHub.

### Production control v0.2.3
Open the desktop Studio shortcut. The default is GPT plan mode (explicit usage consent required; no paid API fallback). Enter a brief and start the existing ten-role pipeline. The gallery lists verified local pilot/batch outputs and completed production jobs, plays video with sound, copies captions and upload file paths, and records internal editorial review bound to the video hash. Open Facebook Reels for owner-controlled upload. No automatic publication, proof of publication, or commercial rights clearance. Notebook and Piper assets remain preview-only where rights are unresolved. Local review files and media remain excluded from GitHub.
\nBatch: enter 1–7 topics (one per line), select GPT plan, confirm usage consent, start queue. Jobs are sequential; failures stop the queue, restart does not resume it. All new pipeline outputs must pass non-silence and decoded true-peak <= -1.5 dBTP. The batch uses no paid API fallback.\n
