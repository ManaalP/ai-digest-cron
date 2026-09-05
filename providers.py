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
- 100 to 200 words, plain prose, no headers or bullet points.
- Write it yourself in your own words; never copy sentences verbatim from \
the excerpt.
- Be concrete: what was released/claimed/found, by whom, and why it matters \
to an ML practitioner. Skip marketing language.
- If the excerpt is too thin to summarize meaningfully, say so plainly in \
under 40 words instead of padding.

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

    def __init__(self, api_key, model):
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model, system_instruction=SYSTEM_PROMPT)

    def summarize(self, title, raw_text, source):
        try:
            resp = self.model.generate_content(
                _user_content(title, raw_text, source),
                generation_config={"max_output_tokens": 500},
            )
            return _parse_json_response(resp.text)
        except Exception as e:
            raise ProviderError(f"google: {e}") from e


PROVIDER_CLASSES = {
    "anthropic": AnthropicProvider,
    "openai": OpenAIProvider,
    "google": GoogleProvider,
}
