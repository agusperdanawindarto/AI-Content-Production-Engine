# AI Content Production Engine - Virtual Studio v0.1

A lightweight, standalone Windows FB Pro production workstation. 10 roles emit actual task events, persisted in each job's state.json. The pixel-style office reflects those events; fast tasks may complete between UI polls. No agent claims work when idle.

## Run on D:
1. Clone or download this repository to D:\AI-Content-Production-Engine. Python 3.11 is a prerequisite. Do not install to C:.
2. Run INSTALL-D.cmd to install dependencies into vendor/ on D:, with temporary files on D:. Existing Python and browser may still use C: for normal OS operations.
3. Run START-STUDIO.cmd. If browser opens before server, refresh http://127.0.0.1:8899/. Close the server console to stop; interrupted jobs remain recorded. Never expose this local server to the internet.
4. Choose Demo (built-in storyboard), Manual (paste ChatGPT scene JSON), or API (paid, explicit confirmation). No Desktop Commander required for operation.
5. Preview the MP4; download subtitle, thumbnail, caption, quality report and policy review. Publish only after owner checks accuracy, asset rights, and Meta disclosure requirements. No automatic Facebook access or publishing.

## AI configuration
Demo/manual are deterministic local tools, not live AI calls. Manual uses ChatGPT in one project chat, via copy/paste. API mode calls OpenAI Responses separately for Researcher, Strategist, Script Writer and Policy Auditor and Audio Speech for Indonesian voice; other roles are software workers. Set OPENAI_API_KEY and OPENAI_MODEL in the local process environment using your own API account. Do not paste keys into chats or GitHub. Model must support Responses API. No automatic spending until API mode is selected and confirmed. ChatGPT subscription and API billing are separate. API mode has not been validated without credentials; default speech model gpt-4o-mini-tts. No live web research tool is included: researcher makes hypotheses only. Demo/manual use silent audio preview because no installed Indonesian TTS was detected; audio production requires API or a later local Indonesian voice integration.

## Acceptance test
Run python -B app.py --demo from this directory. It produces a 720x1280 MP4 with subtitle text burned into cards, SRT, thumbnail, caption, event log and decode check. Optional original sandbox PNGs in assets/uivision-before.png and assets/uivision-after.png; if not supplied, generated illustrative cards are used. Actual account metrics remain unknown. Do not represent illustrative cards as evidence of Facebook performance.

## Design references (not copied assets)
- Pixel Agents overview: https://www.youtube.com/watch?v=KtG5Ez7KujE
- Local real-time agent office: https://www.youtube.com/watch?v=knZuRQi2Gag
- OpenAI TTS docs: https://developers.openai.com/api/docs/guides/text-to-speech

## Integration
Previous Control Center at D:\AI-COMPUTER-CONTROL remains independent (Playwright MCP and UI.Vision). Optional human-controlled sandbox capture can be transferred into assets; no dependency on browser automation for render. Owner can import authorized aggregate metrics using the previous fb-insights.py module. This repository contains production source and reproducible installation files, not private account data, screenshots, outputs, secrets, vendor binaries or prior unrelated projects.
