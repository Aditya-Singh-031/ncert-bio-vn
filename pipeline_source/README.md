# NCERT Bio Interactive Chapter Pipeline - Demo v0.1
Demo section: Class 11 Ch 8, cell theory + prokaryotic vs eukaryotic (6 scenes, 6 MCQs).
Run: `pip install pymupdf pillow cairosvg edge-tts jsonschema "mcp<2"`; place Ren'Py 8.5.3 SDK in ./renpy-8.5.3-sdk; `./run_pipeline.sh`
Layers: specs/ (lesson JSON) -> src/validate.py (schema+evidence) -> render.py (deterministic SVG->PNG) -> audio.py (cached TTS) -> gen_renpy.py -> Ren'Py lint -> qa.py (+asset_manifest.json) -> package.
MCP: src/mcp_server.py exposes validate_lesson, run_qa, get_source_span + resources (spans, style).
Not yet wired (need API keys/accounts): LLM lesson drafting, Runway/Veo video, ElevenLabs voice, Docling ingestion, n8n/Temporal.
