"""
One adapter class per AI provider, each exposing the same interface:

    provider.summarize(title, raw_text, source) -> {"summary": str, "entities": [str]}

All raise ProviderError on any failure (rate limit, quota exhausted, auth
error, network issue, malformed response) so the caller in summarizer.py
can catch just that one exception type and fall through to the next
provider, without needing to know each SDK's own exception classes.

Model names for OpenAI and Google move fast and this file can't guarantee
which ones are current -- check your provider's docs and set OPENAI_MODEL /
GOOGLE_MODEL in .env (or the matching GitHub secret) to whatever's current
and available on your account.
"""

import json

SYSTEM_PROMPT = """You are a technical AI-news summarizer. Given a title and \
raw excerpt, respond with ONLY a JSON object, no preamble, no markdown fences:

{"summary": "...", "entities": ["...", "..."]}

Rules for "summary":
- Exactly 90 to 110 words (target uniform 100 words), plain prose, no headers or bullet points.
- Uniform technical format: 1) What was released/discovered and by whom, 2) Core architecture/mechanics, 3) Concrete engineering impact.
- Write it yourself in your own words; never copy sentences verbatim from the excerpt.
- Skip promotional and marketing fluff; focus on technical substance, benchmarks, and practical developer takeaways.
- If the excerpt is too thin to summarize meaningfully, state that plainly in under 40 words instead of padding.

Rules for "entities":
- 2 to 6 short strings identifying the specific things this item is about: \
model names, company/lab names, paper titles or acronyms, benchmark names.
- Use canonical forms (e.g. "GPT-5" not "gpt5" or "GPT 5").
- These are used to detect when a future article continues this story, so \
prioritize the most specific, re-usable identifiers over generic terms like \
"AI" or "machine learning".
"""


class ProviderError(Exception):
    """Raised for any provider failure so callers can fall through to the
    next provider without needing to know each SDK's exception types."""


def _parse_json_response(text):
    text = (text or "").strip()
    text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    parsed = json.loads(text)
    summary = str(parsed.get("summary", "")).strip()
    entities = [str(e).strip() for e in parsed.get("entities", []) if str(e).strip()]
    if not summary:
        raise ValueError("empty summary field in response")
    return {"summary": summary, "entities": entities}


def _user_content(title, raw_text, source):
    return f"Source: {source}\nTitle: {title}\nExcerpt:\n{raw_text[:3000]}"


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, api_key, model):
        import anthropic
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def summarize(self, title, raw_text, source):
        try:
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": _user_content(title, raw_text, source)}],
            )
            text = "".join(
                b.text for b in resp.content if getattr(b, "type", None) == "text"
            )
            return _parse_json_response(text)
        except Exception as e:
            raise ProviderError(f"anthropic: {e}") from e


class OpenAIProvider:
    name = "openai"

    def __init__(self, api_key, model):
        import openai
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def summarize(self, title, raw_text, source):
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                max_tokens=500,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": _user_content(title, raw_text, source)},
                ],
            )
            text = resp.choices[0].message.content
            return _parse_json_response(text)
        except Exception as e:
            raise ProviderError(f"openai: {e}") from e


class GoogleProvider:
    name = "google"
    FALLBACK_MODELS = [
        "gemini-3.6-flash",
        "gemini-flash-latest",
        "gemini-flash-lite-latest",
        "gemini-2.5-flash-lite",
        "gemini-2.5-pro"
    ]

    def __init__(self, api_key, model="gemini-3.6-flash"):
        import google.generativeai as genai
        self.genai = genai
        self.api_key = api_key
        self.genai.configure(api_key=api_key)
        
        # Priority order: user-specified model first, followed by available fallbacks
        self.model_pool = [model] + [m for m in self.FALLBACK_MODELS if m != model]
        self.current_idx = 0
        self.model_name = self.model_pool[self.current_idx]
        self.model = self.genai.GenerativeModel(self.model_name, system_instruction=SYSTEM_PROMPT)

    def _rotate_model(self):
        self.current_idx = (self.current_idx + 1) % len(self.model_pool)
        self.model_name = self.model_pool[self.current_idx]
        print(f"[providers.google] Quota/Limit mitigation: Rotated active model to '{self.model_name}'")
        self.model = self.genai.GenerativeModel(self.model_name, system_instruction=SYSTEM_PROMPT)

    def summarize(self, title, raw_text, source):
        last_err = None
        for attempt in range(len(self.model_pool)):
            try:
                resp = self.model.generate_content(
                    _user_content(title, raw_text, source),
                    generation_config={"max_output_tokens": 2048, "response_mime_type": "application/json"},
                )
                return _parse_json_response(resp.text)
            except Exception as e:
                err_str = str(e)
                last_err = e
                # Rotate on 429, quota exhausted, rate limits, or model unavailability
                if any(x in err_str.lower() for x in ["429", "quota", "resource_exhausted", "ratelimit", "not available", "404", "overloaded"]):
                    print(f"[providers.google] '{self.model_name}' rate/quota notice: {err_str[:70]}...")
                    self._rotate_model()
                    continue
                else:
                    self._rotate_model()
                    continue
        raise ProviderError(f"google: all {len(self.model_pool)} rotation models exhausted. Last: {last_err}") from last_err


PROVIDER_CLASSES = {
    "anthropic": AnthropicProvider,
    "openai": OpenAIProvider,
    "google": GoogleProvider,
}
