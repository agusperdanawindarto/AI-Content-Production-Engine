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
