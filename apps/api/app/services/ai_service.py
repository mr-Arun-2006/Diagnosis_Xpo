from __future__ import annotations

import json
import os
from urllib.request import Request, urlopen

from packages.ai_engine import DiagnosisEvidence, build_prompt


SUPPORTED_LANGUAGES = {"en": "English", "ta": "Tamil", "hi": "Hindi", "gu": "Gujarati"}


class AIExplanationService:
    def explain(self, evidence: DiagnosisEvidence, language: str = "en") -> dict:
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")
        prompt = build_prompt(evidence, SUPPORTED_LANGUAGES[language])
        base_url = os.getenv("AI_BASE_URL", "").rstrip("/")
        api_key = os.getenv("AI_API_KEY", "")
        model = os.getenv("AI_MODEL", "")
        if not base_url or not api_key or not model:
            return {
                "status": "not_configured",
                "language": language,
                "model": None,
                "explanation": None,
                "prompt_ready": True,
            }

        payload = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": "Return a concise educational market explanation grounded only in supplied evidence."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }).encode()
        request = Request(
            f"{base_url}/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=45) as response:
                data = json.loads(response.read().decode("utf-8"))
            text = data["choices"][0]["message"]["content"]
        except Exception as exc:
            raise RuntimeError(f"AI provider request failed: {exc}") from exc
        return {"status": "ready", "language": language, "model": model, "explanation": text, "prompt_ready": True}
