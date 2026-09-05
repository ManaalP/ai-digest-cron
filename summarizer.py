"""
Tries each configured AI provider in priority order for every article.
If one fails (rate limited, quota exhausted, outage, bad response), it
moves to the next. A provider that fails twice in a row is skipped for
the rest of the run, so a rate-limit storm doesn't cost a retry on every
remaining article.

This only rotates *away* from a failing provider -- it doesn't load-balance
across healthy ones. That's deliberate: for a small daily batch, "prefer
the first healthy provider every time" is simpler to reason about and
debug than round-robin, and cost/quality differences between providers
usually matter more than spreading load evenly.
"""

from providers import PROVIDER_CLASSES, ProviderError


class MultiProviderSummarizer:
    def __init__(self, provider_configs: dict, priority: list):
        """
        provider_configs: {"anthropic": {"api_key": "...", "model": "..."}, ...}
        priority: try-order, e.g. ["anthropic", "openai", "google"].
        Providers with no api_key configured are silently skipped -- you
        don't need all three, one is enough to run.
        """
        self.providers = []
        for name in priority:
            cfg = provider_configs.get(name) or {}
            if not cfg.get("api_key"):
                continue
            cls = PROVIDER_CLASSES.get(name)
            if not cls:
                print(f"[summarizer] Unknown provider '{name}' in priority list, skipping.")
                continue
            try:
                self.providers.append(cls(cfg["api_key"], cfg["model"]))
                print(f"[summarizer] Provider '{name}' ready (model={cfg['model']}).")
            except Exception as e:
                print(f"[summarizer] Could not initialize provider '{name}': {e}")

        if not self.providers:
            raise RuntimeError(
                "No AI providers configured. Set at least one of "
                "ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY."
            )

        self._disabled_this_run = set()
        self._fail_counts = {p.name: 0 for p in self.providers}

    def summarize(self, title: str, raw_text: str, source: str) -> dict:
        last_err = None
        for provider in self.providers:
            if provider.name in self._disabled_this_run:
                continue
            try:
                result = provider.summarize(title, raw_text, source)
                self._fail_counts[provider.name] = 0
                return result
            except ProviderError as e:
                last_err = e
                self._fail_counts[provider.name] += 1
                print(f"[summarizer] {provider.name} failed on '{title[:60]}': {e}")
                if self._fail_counts[provider.name] >= 2:
                    print(f"[summarizer] '{provider.name}' failed twice in a row -- "
                          f"disabling it for the rest of this run.")
                    self._disabled_this_run.add(provider.name)

        raise RuntimeError(
            f"All configured providers failed for '{title}'. Last error: {last_err}"
        )
