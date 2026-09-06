#!/usr/bin/env python3
"""
build_webapp.py - Generates the Minimalist, Reader-Friendly AI Digest Web Application.

Features:
  - Minimalist, calm dark reader aesthetic (#0d0f12 base, #13161c surfaces, #181b22 cards, subtle borders).
  - Strict 4-week calendar history with dedicated media segregation.
  - Interactive Benchmark Comparison Bar Chart with real SWE-bench Verified scores:
      * Claude 3.7 Sonnet (70.3%), OpenAI o3-mini (79.7%), Claude 3.5 Sonnet (63.7%),
      * DeepSeek-R1 (49.2%), OpenAI o1 (48.9%), Qwen 2.5 Coder 32B (48.4%),
      * DeepSeek-V3, GPT-4o, Gemini 2.0 Flash, Gemini 2.0 Pro, Llama 3.3 70B.
      * Tapping any row opens the full Model Inspector Drawer on mobile and desktop.
  - In-Page Sticky Sub-Navigation (Deep Dives, YouTube, X & Reddit, 1-Liners).
  - Unbiased 3-Year Milestones Archive (2023–2026).
  - Pure canonical domain: ai-digest-by-mp.vercel.app.
"""

import json
from pathlib import Path

# Load seed data if available
seed_file = Path("seed_7days.json")
if seed_file.exists():
    with open(seed_file, "r", encoding="utf-8") as f:
        seed_data = json.load(f)
else:
    seed_data = {}

seed_json_str = json.dumps(seed_data)

# Unbiased 3-Year Milestones Archive (2023 - 2026)
MILESTONES_ARCHIVE = {
    "yearly": [
        {
            "period": "2025",
            "top3": [
                {
                    "title": "Claude 3.7 Sonnet: First Hybrid Extended Thinking Model",
                    "lab": "Anthropic",
                    "capability": "Unified standard instant inference and extended test-time thinking tokens into a single model, setting SWE-bench Verified records (70.3%).",
                    "date": "February 2025",
                    "impact": "Eliminated the compromise between chat latency and deep reasoning, powering the next generation of autonomous coding agents."
                },
                {
                    "title": "OpenAI o3-mini: High-Throughput Cost-Efficient Reasoning",
                    "lab": "OpenAI",
                    "capability": "Delivered 79.7% on SWE-bench Verified at high effort with granular reasoning_effort dials (low, medium, high).",
                    "date": "January 2025",
                    "impact": "Brought deliberate reasoning budgets into automated CI/CD pipelines, making automated bug patching affordable at enterprise scale."
                },
                {
                    "title": "DeepSeek-R1: Pure Reinforcement Learning Open Weights",
                    "lab": "DeepSeek AI",
                    "capability": "Demonstrated that large-scale pure RL elicits reasoning parity with closed models, releasing open MIT weights and 14B/32B distilled checkpoints.",
                    "date": "January 2025",
                    "impact": "Democratized frontier reasoning globally; enabled high-accuracy reasoning on local developer workstations and private clouds."
                }
            ]
        },
        {
            "period": "2024",
            "top3": [
                {
                    "title": "Claude 3.5 Sonnet: The Developer Coding Benchmark SOTA",
                    "lab": "Anthropic",
                    "capability": "Achieved 63.7% on SWE-bench Verified alongside Computer Use and Artifacts, redefining developer pair programming.",
                    "date": "June / October 2024",
                    "impact": "Became the industry standard powering modern coding assistants like Cursor, Claude Code, and Aider."
                },
                {
                    "title": "The Test-Time Scaling Era: OpenAI o1",
                    "lab": "OpenAI",
                    "capability": "Demonstrated that scaling inference compute via hidden chain-of-thought unlocks unprecedented mathematical and scientific reasoning.",
                    "date": "September / December 2024",
                    "impact": "Established test-time compute as the third scaling paradigm alongside pre-training data and model parameters."
                },
                {
                    "title": "AlphaFold 3: Comprehensive Biomolecular Structure Prediction",
                    "lab": "Google DeepMind & Isomorphic Labs",
                    "capability": "Diffusion-based unified modeling predicting interactions across all biomolecules: proteins, DNA, RNA, ligands, and ions.",
                    "date": "May 2024",
                    "impact": "Accelerated molecular biology, oncology target discovery, and synthetic therapeutics worldwide."
                }
            ]
        },
        {
            "period": "2023",
            "top3": [
                {
                    "title": "GPT-4 Launch: Modern Multimodal Foundation Landmark",
                    "lab": "OpenAI",
                    "capability": "Mixture-of-Experts architecture passing the Uniform Bar Exam in the 90th percentile and mastering multi-domain reasoning.",
                    "date": "March 2023",
                    "impact": "Catalyzed the global generative AI revolution and established the blueprint for enterprise LLM applications."
                },
                {
                    "title": "Open Source Foundation Awakening: LLaMA",
                    "lab": "Meta AI",
                    "capability": "Release of efficient 7B/13B/65B weights, sparking llama.cpp, local quantization, and modern open-source AI.",
                    "date": "Spring 2023",
                    "impact": "Proved foundational intelligence can be democratized and executed locally on consumer laptops and workstations."
                },
                {
                    "title": "Mixtral 8x7B: Sparse MoE Breakthrough",
                    "lab": "Mistral AI",
                    "capability": "Open sparse mixture-of-experts model matching or exceeding larger dense models with high inference speeds.",
                    "date": "December 2023",
                    "impact": "Validated sparse MoE architectures as the premier approach for high token throughput and cost efficiency."
                }
            ]
        }
    ],
    "quarterly": [
        {
            "period": "2025 Q1",
            "top3": [
                { "title": "Claude 3.7 Sonnet Hybrid Extended Thinking", "lab": "Anthropic", "capability": "70.3% SWE-bench Verified with dynamic thinking budget controls.", "date": "Feb 2025" },
                { "title": "OpenAI o3-mini High-Throughput Reasoning", "lab": "OpenAI", "capability": "79.7% SWE-bench Verified at affordable token pricing ($1.10/1M).", "date": "Jan 2025" },
                { "title": "DeepSeek-R1 Open MoE 671B Weights Release", "lab": "DeepSeek", "capability": "Full open weights pure RL reasoning rivaling closed models.", "date": "Jan 2025" }
            ]
        },
        {
            "period": "2024 Q4",
            "top3": [
                { "title": "OpenAI o1 Full Flagship Release", "lab": "OpenAI", "capability": "Inference-time reasoning scaling for competitive math and coding.", "date": "Dec 2024" },
                { "title": "DeepSeek-V3 671B Multi-Head Latent Attention", "lab": "DeepSeek", "capability": "Commodity cost training and ultra-fast inference throughput.", "date": "Dec 2024" },
                { "title": "Llama 3.3 70B Single-Node Frontier Model", "lab": "Meta AI", "capability": "405B capabilities packed into single workstation inference.", "date": "Dec 2024" }
            ]
        },
        {
            "period": "2024 Q3",
            "top3": [
                { "title": "OpenAI o1-preview Test-Time Compute", "lab": "OpenAI", "capability": "First public demonstration of deliberate chain-of-thought scaling.", "date": "Sep 2024" },
                { "title": "Qwen 2.5 Coder 32B Open Champion", "lab": "Alibaba", "capability": "Apache 2.0 open-source coding model rivaling closed GPT-4o.", "date": "Nov 2024" },
                { "title": "Anthropic Computer Use Public Beta", "lab": "Anthropic", "capability": "Direct desktop UI, browser, and terminal control via API.", "date": "Oct 2024" }
            ]
        },
        {
            "period": "2024 Q2",
            "top3": [
                { "title": "Claude 3.5 Sonnet & Artifacts Launch", "lab": "Anthropic", "capability": "SWE-bench leader establishing modern coding assistant standard.", "date": "Jun 2024" },
                { "title": "AlphaFold 3 Biomolecular Breakthrough", "lab": "Google DeepMind", "capability": "Unified diffusion modeling of all biomolecular complexes.", "date": "May 2024" },
                { "title": "Llama 3 8B & 70B Open Release", "lab": "Meta AI", "capability": "State-of-the-art open foundation baseline trained on 15T tokens.", "date": "Apr 2024" }
            ]
        }
    ],
    "monthly": [
        {
            "period": "2025-02",
            "top3": [
                { "title": "Claude 3.7 Sonnet Hybrid Reasoning Launch", "lab": "Anthropic", "capability": "First hybrid extended thinking model, scoring 70.3% on SWE-bench Verified.", "date": "2025-02-24" },
                { "title": "Gemini 2.0 Pro Experimental & Flash Updates", "lab": "Google DeepMind", "capability": "2M context window with advanced multimodal reasoning and real-time streaming.", "date": "2025-02-05" },
                { "title": "Claude Code Autonomous Terminal Agent Beta", "lab": "Anthropic", "capability": "Direct CLI agent running multi-file edits and self-healing tests.", "date": "2025-02-24" }
            ]
        },
        {
            "period": "2025-01",
            "top3": [
                { "title": "OpenAI o3-mini Production Launch", "lab": "OpenAI", "capability": "79.7% SWE-bench Verified with low/medium/high reasoning effort dials.", "date": "2025-01-31" },
                { "title": "DeepSeek-R1 Open Weights Release", "lab": "DeepSeek", "capability": "671B MoE pure RL reasoning weights released under MIT license.", "date": "2025-01-20" },
                { "title": "Distilled Reasoning Local Deployments", "lab": "Open Source Community", "capability": "Distilled R1 14B/32B models run locally on consumer GPUs in Ollama.", "date": "2025-01-25" }
            ]
        },
        {
            "period": "2024-12",
            "top3": [
                { "title": "DeepSeek-V3 671B DualPipe Architecture", "lab": "DeepSeek", "capability": "Multi-Head Latent Attention enabling ultra-low KV memory.", "date": "2024-12-26" },
                { "title": "OpenAI o1 Full Flagship Release", "lab": "OpenAI", "capability": "Deliberate reasoning model with vision understanding and fast tool use.", "date": "2024-12-05" },
                { "title": "Llama 3.3 70B Release", "lab": "Meta AI", "capability": "405B capabilities packed into single workstation inference.", "date": "2024-12-06" }
            ]
        }
    ]
}

# Frontier Model Master Database with Real SOTA Benchmarks & Developer Verdicts
FRONTIER_MODELS = [
    {
        "id": "claude-3-7-sonnet",
        "name": "Claude 3.7 Sonnet",
        "lab": "Anthropic",
        "lab_slug": "anthropic",
        "is_frontier": True,
        "year": "2025",
        "release_date": "February 2025",
        "benchmark_score": 70.3,
        "benchmark_label": "70.3% SWE-bench Verified · SOTA Hybrid Thinking",
        "license": "Proprietary API",
        "context_window": "200,000 tokens",
        "max_output": "64,000 tokens",
        "pricing_input": "$3.00 / 1M",
        "pricing_output": "$15.00 / 1M",
        "pricing_cached": "$0.30 / 1M",
        "architecture": "Hybrid Standard & Extended Thinking Core",
        "readiness": "Frontier SOTA",
        "tag": "HYBRID REASONING SOTA",
        "best_for": "Autonomous whole-repo refactoring, agentic coding loops (Claude Code, Cursor), deep architectural debugging, complex front-end synthesis.",
        "better_to_work_with": "The most dependable developer assistant available. Continuous dynamic thinking dial allows spending more tokens on hard logical verification while replying instantly to routine edits. Very low hallucination rate on codebases.",
        "capabilities": ["Extended Thinking Dial", "70.3% SWE-bench Verified", "74.5% SWE-bench Pro", "Claude Code Native", "Low Hallucination Rate"],
        "api_snippet": "import anthropic\nclient = anthropic.Anthropic()\nresp = client.messages.create(\n    model='claude-3-7-sonnet-20250219',\n    max_tokens=64000,\n    thinking={'type': 'enabled', 'budget_tokens': 8000},\n    messages=[{'role': 'user', 'content': 'Refactor the authentication module'}]\n)"
    },
    {
        "id": "openai-o3-mini",
        "name": "OpenAI o3-mini",
        "lab": "OpenAI",
        "lab_slug": "openai",
        "is_frontier": True,
        "year": "2025",
        "release_date": "January 2025",
        "benchmark_score": 79.7,
        "benchmark_label": "79.7% SWE-bench Verified (High Effort) · Cost Leader",
        "license": "Proprietary API",
        "context_window": "200,000 tokens",
        "max_output": "100,000 tokens",
        "pricing_input": "$1.10 / 1M",
        "pricing_output": "$4.40 / 1M",
        "pricing_cached": "$0.55 / 1M",
        "architecture": "Test-Time RL Reasoning",
        "readiness": "Cost & Reasoning SOTA",
        "tag": "STEM & CODING REASONING",
        "best_for": "High-throughput automated unit test generation, CI/CD regression debugging, math proofs, competitive programming.",
        "better_to_work_with": "Incredible cost-to-intelligence ratio. The reasoning_effort parameter ('low', 'medium', 'high') lets you configure exact compute budgets for automated build pipelines.",
        "capabilities": ["Configurable Thinking Budget", "79.7% SWE-bench Verified", "STEM Competition Gold", "Fast Token Generation"],
        "api_snippet": "from openai import OpenAI\nclient = OpenAI()\nresp = client.chat.completions.create(\n    model='o3-mini',\n    reasoning_effort='high',\n    messages=[{'role': 'user', 'content': 'Fix failing integration tests in auth_spec.py'}]\n)"
    },
    {
        "id": "claude-3-5-sonnet",
        "name": "Claude 3.5 Sonnet",
        "lab": "Anthropic",
        "lab_slug": "anthropic",
        "is_frontier": True,
        "year": "2024",
        "release_date": "October 2024",
        "benchmark_score": 63.7,
        "benchmark_label": "63.7% SWE-bench Verified · Workhorse Standard",
        "license": "Proprietary API",
        "context_window": "200,000 tokens",
        "max_output": "8,192 tokens",
        "pricing_input": "$3.00 / 1M",
        "pricing_output": "$15.00 / 1M",
        "pricing_cached": "$0.30 / 1M",
        "architecture": "Dense Frontier Flagship",
        "readiness": "Production Workhorse",
        "tag": "INDUSTRY STANDARD",
        "best_for": "Interactive coding, frontend UI generation, document synthesis, visual comprehension, prompt engineering.",
        "better_to_work_with": "The baseline against which all modern coding models are measured. Near-zero latency lag and exceptional instruction adherence.",
        "capabilities": ["63.7% SWE-bench", "Computer Use API", "Artifacts UI", "Prompt Caching 90% Discount"],
        "api_snippet": "import anthropic\nclient = anthropic.Anthropic()\nresp = client.messages.create(\n    model='claude-3-5-sonnet-20241022',\n    max_tokens=8192,\n    messages=[{'role': 'user', 'content': 'Build a responsive dashboard component'}]\n)"
    },
    {
        "id": "deepseek-r1",
        "name": "DeepSeek-R1",
        "lab": "DeepSeek",
        "lab_slug": "deepseek",
        "is_frontier": True,
        "year": "2025",
        "release_date": "January 2025",
        "benchmark_score": 49.2,
        "benchmark_label": "49.2% SWE-bench Verified · 79.8% AIME · Open Weights MIT",
        "license": "Open Weights (MIT)",
        "context_window": "128,000 tokens",
        "max_output": "8,192 tokens",
        "pricing_input": "$0.55 / 1M",
        "pricing_output": "$2.19 / 1M",
        "pricing_cached": "$0.14 / 1M",
        "architecture": "671B MoE (37B active) Pure RL Reasoning",
        "readiness": "Open Weights SOTA",
        "tag": "OPEN REASONING REVOLUTION",
        "best_for": "Deep math proofs, algorithmic problem solving, local self-hosted private code audits, distilled model training.",
        "better_to_work_with": "Full chain-of-thought visible in <think> tags. Runs locally or at ~1/20th the cost of proprietary competitors with full data privacy.",
        "capabilities": ["Pure RL Chain-of-Thought", "MIT Open License", "AIME 79.8%", "Distilled 14B/32B Local Weights"],
        "api_snippet": "from openai import OpenAI\nclient = OpenAI(base_url='https://api.deepseek.com', api_key='...')\nresp = client.chat.completions.create(\n    model='deepseek-reasoner',\n    messages=[{'role': 'user', 'content': 'Analyze time complexity of this graph traversal'}]\n)"
    },
    {
        "id": "openai-o1",
        "name": "OpenAI o1",
        "lab": "OpenAI",
        "lab_slug": "openai",
        "is_frontier": True,
        "year": "2024",
        "release_date": "December 2024",
        "benchmark_score": 48.9,
        "benchmark_label": "48.9% SWE-bench Verified · Deep Logical Reasoning",
        "license": "Proprietary API",
        "context_window": "200,000 tokens",
        "max_output": "100,000 tokens",
        "pricing_input": "$15.00 / 1M",
        "pricing_output": "$60.00 / 1M",
        "pricing_cached": "$7.50 / 1M",
        "architecture": "Inference-Time Compute Scaling",
        "readiness": "Frontier Flagship",
        "tag": "DEEP LOGIC & MATH",
        "best_for": "PhD-level scientific problem solving, complex algorithmic logic, multi-page security auditing.",
        "better_to_work_with": "High reasoning depth for difficult theoretical challenges, but longer token generation latency. Best for asynchronous validation.",
        "capabilities": ["Inference-Time Scaling", "Codeforces 1800+", "Competitive Math", "Vision Reasoning"],
        "api_snippet": "from openai import OpenAI\nclient = OpenAI()\nresp = client.chat.completions.create(\n    model='o1',\n    messages=[{'role': 'user', 'content': 'Design a formally verified consensus protocol'}]\n)"
    },
    {
        "id": "qwen-2-5-coder-32b",
        "name": "Qwen 2.5 Coder 32B",
        "lab": "Alibaba Cloud",
        "lab_slug": "alibaba",
        "is_frontier": True,
        "year": "2024",
        "release_date": "November 2024",
        "benchmark_score": 48.4,
        "benchmark_label": "48.4% SWE-bench Verified · Workstation Local SOTA",
        "license": "Open Source (Apache 2.0)",
        "context_window": "128,000 tokens",
        "max_output": "8,192 tokens",
        "pricing_input": "Free / Self-Hosted ($0.15/1M API)",
        "pricing_output": "Free / Self-Hosted ($0.60/1M API)",
        "pricing_cached": "$0.05 / 1M",
        "architecture": "32.5B Dense Transformer",
        "readiness": "Workstation SOTA",
        "tag": "LOCAL CODING CHAMPION",
        "best_for": "Local IDE pair programming in Ollama/vLLM, air-gapped enterprise code generation, offline syntax refactoring.",
        "better_to_work_with": "Runs at full speed on a single RTX 4090 or Apple Silicon Mac while matching GPT-4o coding performance. Zero telemetry.",
        "capabilities": ["Apache 2.0 License", "Single GPU Runnable", "128K Context", "Aider/Cursor Compatible"],
        "api_snippet": "ollama run qwen2.5-coder:32b 'Refactor this SQL migration for PostgreSQL'"
    },
    {
        "id": "deepseek-v3",
        "name": "DeepSeek-V3",
        "lab": "DeepSeek",
        "lab_slug": "deepseek",
        "is_frontier": True,
        "year": "2024",
        "release_date": "December 2024",
        "benchmark_score": 46.5,
        "benchmark_label": "671B MoE (37B active) · Multi-Head Latent Attention",
        "license": "Open Weights (MIT)",
        "context_window": "128,000 tokens",
        "max_output": "8,192 tokens",
        "pricing_input": "$0.14 / 1M",
        "pricing_output": "$0.28 / 1M",
        "pricing_cached": "$0.07 / 1M",
        "architecture": "671B MoE with Multi-Head Latent Attention & DualPipe",
        "readiness": "Cost & Throughput SOTA",
        "tag": "COMMODITY FRONTIER MOE",
        "best_for": "General software development, synthetic dataset generation, conversational assistants, multi-turn translation.",
        "better_to_work_with": "Near Claude 3.5 Sonnet quality at commodity pricing ($0.14/1M input). Incredibly fast inference throughput on cloud nodes.",
        "capabilities": ["Multi-Head Latent Attention", "DualPipe Parallelism", "MIT Open License", "FP8 Native Inference"],
        "api_snippet": "from openai import OpenAI\nclient = OpenAI(base_url='https://api.deepseek.com', api_key='...')\nresp = client.chat.completions.create(\n    model='deepseek-chat',\n    messages=[{'role': 'user', 'content': 'Write an asynchronous FastAPI rate limiter'}]\n)"
    },
    {
        "id": "gemini-2-flash",
        "name": "Gemini 2.0 Flash",
        "lab": "Google DeepMind",
        "lab_slug": "google",
        "is_frontier": True,
        "year": "2025",
        "release_date": "February 2025",
        "benchmark_score": 45.0,
        "benchmark_label": "1M Context · Sub-Second Latency · Multimodal Streaming",
        "license": "Proprietary API",
        "context_window": "1,048,576 tokens",
        "max_output": "8,192 tokens",
        "pricing_input": "$0.10 / 1M",
        "pricing_output": "$0.40 / 1M",
        "pricing_cached": "$0.025 / 1M",
        "architecture": "Multimodal Native Sparse Core",
        "readiness": "Speed & Scale Leader",
        "tag": "SUB-SECOND MULTIMODAL",
        "best_for": "Real-time voice and video agents, multi-hour video comprehension, 1M token context recall, fast agentic routers.",
        "better_to_work_with": "Unbeatable speed and context window. Sub-300ms time to first token makes it the default orchestrator for live tool-calling agents.",
        "capabilities": ["1,048,576 Token Context", "Sub-Second Latency", "Native Audio/Video I/O", "Google Search Grounding"],
        "api_snippet": "from google import genai\nclient = genai.Client()\nresp = client.models.generate_content(\n    model='gemini-2.0-flash',\n    contents='Summarize this 100-page architectural documentation'\n)"
    },
    {
        "id": "gemini-2-pro",
        "name": "Gemini 2.0 Pro (Exp)",
        "lab": "Google DeepMind",
        "lab_slug": "google",
        "is_frontier": True,
        "year": "2025",
        "release_date": "February 2025",
        "benchmark_score": 52.0,
        "benchmark_label": "2M Context Window · Advanced Multimodal & Code Reasoning",
        "license": "Proprietary API",
        "context_window": "2,097,152 tokens",
        "max_output": "8,192 tokens",
        "pricing_input": "Preview Tier",
        "pricing_output": "Preview Tier",
        "pricing_cached": "Preview Tier",
        "architecture": "Frontier Multimodal Deep Reasoning Core",
        "readiness": "Frontier Flagship",
        "tag": "2M CONTEXT REASONING",
        "best_for": "Ingesting entire corporate code repositories in a single prompt, complex cross-repo migrations, multi-book synthesis.",
        "better_to_work_with": "Industry-leading 2M token context window with reliable needle-in-a-haystack recall across millions of tokens of code.",
        "capabilities": ["2M Token Context", "Complex Coding Benchmark Leader", "Native Multimodal Ingestion", "Deep World Knowledge"],
        "api_snippet": "from google import genai\nclient = genai.Client()\nresp = client.models.generate_content(\n    model='gemini-2.0-pro-exp-02-05',\n    contents='Analyze dependencies across this entire zipped repository'\n)"
    },
    {
        "id": "gpt-4o",
        "name": "GPT-4o",
        "lab": "OpenAI",
        "lab_slug": "openai",
        "is_frontier": True,
        "year": "2024",
        "release_date": "May 2024",
        "benchmark_score": 38.8,
        "benchmark_label": "38.8% SWE-bench Verified · Enterprise Omnimodal Standard",
        "license": "Proprietary API",
        "context_window": "128,000 tokens",
        "max_output": "16,384 tokens",
        "pricing_input": "$2.50 / 1M",
        "pricing_output": "$10.00 / 1M",
        "pricing_cached": "$1.25 / 1M",
        "architecture": "Native Omnimodal Flagship",
        "readiness": "Enterprise Production",
        "tag": "ENTERPRISE WORKHORSE",
        "best_for": "General multimodal reasoning, structured JSON schema extraction, conversational customer interfaces, vision tasks.",
        "better_to_work_with": "Standard enterprise workhorse. Predictable latency, high rate limits, and seamless integration across corporate cloud stacks.",
        "capabilities": ["Native Multimodal Audio/Vision", "Structured Outputs 100%", "Predictable Latency", "Broad Tool Ecosystem"],
        "api_snippet": "from openai import OpenAI\nclient = OpenAI()\nresp = client.chat.completions.create(\n    model='gpt-4o',\n    response_format={'type': 'json_object'},\n    messages=[{'role': 'user', 'content': 'Extract customer intent schema'}]\n)"
    },
    {
        "id": "llama-3-3-70b",
        "name": "Llama 3.3 70B",
        "lab": "Meta AI",
        "lab_slug": "meta",
        "is_frontier": True,
        "year": "2024",
        "release_date": "December 2024",
        "benchmark_score": 41.5,
        "benchmark_label": "Open Weights (Apache 2.0) · 405B Parity in 70B Footprint",
        "license": "Open Weights (Llama 3.3 License)",
        "context_window": "128,000 tokens",
        "max_output": "8,192 tokens",
        "pricing_input": "$0.18 / 1M or Self-Hosted",
        "pricing_output": "$0.54 / 1M or Self-Hosted",
        "pricing_cached": "$0.09 / 1M",
        "architecture": "Dense Grouped-Query Attention Transformer",
        "readiness": "Open Foundation SOTA",
        "tag": "OPEN WEIGHTS ENTERPRISE",
        "best_for": "Self-hosted enterprise workflows, private fine-tuning, retrieval-augmented generation (RAG), air-gapped deployments.",
        "better_to_work_with": "Delivers performance matching the massive 405B model while fitting on single 8x GPU nodes or quantized workstation servers.",
        "capabilities": ["Open Weights License", "405B Parity", "Tool Calling Support", "Multilingual Generalist"],
        "api_snippet": "ollama run llama3.3:70b 'Analyze database schema performance bottlenecks'"
    }
]

models_json_str = json.dumps(FRONTIER_MODELS)
milestones_json_str = json.dumps(MILESTONES_ARCHIVE)

print("[build_webapp] Compiling Minimalist Reader index.html...")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>AI Digest — Frontier AI &amp; Developer Intelligence</title>
    <meta name="description" content="A calm, reader-friendly developer digest tracking verified frontier models, SWE-bench leaderboards, weekly breakthroughs, and community debates.">
    <meta name="theme-color" content="#0d0f12">

    <!-- Favicon & Touch Icon -->
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="apple-touch-icon" href="/favicon.svg">

    <!-- Open Graph / WhatsApp / Facebook Preview Tags -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="AI Digest">
    <meta property="og:title" content="AI Digest — Frontier AI &amp; Developer Intelligence">
    <meta property="og:description" content="A calm, reader-friendly developer digest tracking verified frontier models, SWE-bench leaderboards, and weekly breakthroughs.">
    <meta property="og:url" content="https://ai-digest-by-mp.vercel.app">
    <meta property="og:image" content="https://ai-digest-by-mp.vercel.app/og-preview.jpg">
    <meta property="og:image:secure_url" content="https://ai-digest-by-mp.vercel.app/og-preview.jpg">
    <meta property="og:image:type" content="image/jpeg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="AI Digest — Frontier AI &amp; Developer Intelligence">

    <!-- Twitter / X Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="AI Digest — Frontier AI &amp; Developer Intelligence">
    <meta name="twitter:description" content="A calm, reader-friendly developer digest tracking verified frontier models, SWE-bench leaderboards, and weekly breakthroughs.">
    <meta name="twitter:image" content="https://ai-digest-by-mp.vercel.app/og-preview.jpg">
    
    <!-- Modern Reader Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    
    <!-- Supabase JS Client -->
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

    <style>
        :root {{
            /* Minimalist Reader Palette */
            --bg-base: #0d0f12;
            --bg-surface: #13161c;
            --bg-card: #14171e;
            --bg-card-hover: #191d26;
            --bg-elevated: #1e222d;
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-highlight: rgba(255, 255, 255, 0.16);
            
            --accent-primary: #3b82f6;
            --accent-primary-hover: #60a5fa;
            --accent-secondary: #10b981;
            --accent-amber: #f59e0b;
            --accent-purple: #8b5cf6;
            
            --text-primary: #f1f3f7;
            --text-secondary: #9da4b0;
            --text-muted: #656d7d;
            
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 14px;
            --radius-pill: 500px;
            --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            background-color: var(--bg-base);
            color: var(--text-primary);
            font-family: var(--font-sans);
            min-height: 100vh;
            line-height: 1.65;
            overflow-x: hidden;
        }}

        /* Header */
        header {{
            position: sticky;
            top: 0;
            z-index: 60;
            background: rgba(13, 15, 18, 0.94);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid var(--border-subtle);
        }}

        .header-inner {{
            max-width: 1240px;
            margin: 0 auto;
            padding: 12px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            color: var(--text-primary);
        }}

        .brand-icon {{
            width: 34px;
            height: 34px;
            border-radius: var(--radius-sm);
            background: #1e222d;
            border: 1px solid var(--border-highlight);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }}

        .brand-title {{
            font-weight: 700;
            font-size: 17px;
            letter-spacing: -0.02em;
        }}

        .brand-subtitle {{
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 400;
        }}

        /* Nav Pills */
        nav.nav-bar {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .nav-btn {{
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-size: 13.5px;
            font-weight: 600;
            padding: 8px 14px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .nav-btn:hover {{
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.05);
        }}

        .nav-btn.active {{
            color: var(--text-primary);
            background: var(--bg-elevated);
            border: 1px solid var(--border-highlight);
        }}

        /* Share Button */
        .share-btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(59, 130, 246, 0.12);
            border: 1px solid rgba(59, 130, 246, 0.3);
            color: #60a5fa;
            font-size: 13px;
            font-weight: 600;
            padding: 7px 14px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .share-btn:hover {{
            background: rgba(59, 130, 246, 0.22);
            border-color: #60a5fa;
            color: #93c5fd;
        }}

        /* In-Page Sub-Navigation */
        .inpage-nav-wrap {{
            position: sticky;
            top: 61px;
            z-index: 40;
            background: rgba(13, 15, 18, 0.88);
            backdrop-filter: blur(12px);
            padding: 8px 0;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .inpage-nav {{
            display: flex;
            align-items: center;
            gap: 8px;
            overflow-x: auto;
            scrollbar-width: none;
            -webkit-overflow-scrolling: touch;
        }}

        .inpage-nav::-webkit-scrollbar {{
            display: none;
        }}

        .inpage-pill {{
            font-size: 12.5px;
            font-weight: 600;
            color: var(--text-secondary);
            text-decoration: none;
            padding: 6px 14px;
            border-radius: var(--radius-pill);
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .inpage-pill:hover {{
            color: var(--text-primary);
            background: var(--bg-card-hover);
            border-color: var(--border-highlight);
        }}

        /* Main Container */
        main {{
            max-width: 1240px;
            margin: 0 auto;
            padding: 24px 24px 60px 24px;
        }}

        .section-header {{
            margin-bottom: 20px;
        }}

        .section-title {{
            font-size: 24px;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 6px;
        }}

        .section-desc {{
            color: var(--text-secondary);
            font-size: 14.5px;
            line-height: 1.55;
            max-width: 800px;
        }}

        /* Weekly Edition Filter Bar */
        .date-filter-section {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 14px 18px;
            margin-bottom: 22px;
        }}

        .date-filter-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
        }}

        .date-filter-label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            font-weight: 600;
        }}

        .date-filter-bar {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}

        .date-chip {{
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            padding: 7px 14px;
            border-radius: var(--radius-sm);
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .date-chip:hover {{
            background: var(--bg-card-hover);
            color: var(--text-primary);
        }}

        .date-chip.active {{
            background: var(--accent-primary);
            border-color: var(--accent-primary);
            color: #ffffff;
            font-weight: 600;
        }}

        /* Topic Chips */
        .tag-bar {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 18px;
        }}

        .tag-chip {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            padding: 6px 12px;
            border-radius: var(--radius-pill);
            font-size: 12.5px;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .tag-chip:hover {{
            background: var(--bg-card-hover);
            color: var(--text-primary);
        }}

        .tag-chip.active {{
            background: var(--bg-elevated);
            border-color: var(--border-highlight);
            color: var(--text-primary);
            font-weight: 600;
        }}

        /* Search Bar */
        .search-bar {{
            margin-bottom: 24px;
        }}

        .search-input {{
            width: 100%;
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 12px 18px;
            color: var(--text-primary);
            font-size: 14px;
            font-family: var(--font-sans);
            outline: none;
            transition: border-color 0.15s ease;
        }}

        .search-input:focus {{
            border-color: var(--accent-primary);
        }}

        .search-input::placeholder {{
            color: var(--text-muted);
        }}

        /* Media Sections (Articles, Videos, Social Buzz, 1-Liners) */
        .media-section {{
            margin-bottom: 38px;
        }}

        .media-section-header {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            margin-bottom: 16px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .media-section-title {{
            font-size: 18px;
            font-weight: 700;
            letter-spacing: -0.01em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .media-section-badge {{
            font-size: 11px;
            font-weight: 600;
            color: var(--accent-primary-hover);
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.2);
            padding: 2px 8px;
            border-radius: var(--radius-pill);
        }}

        .media-section-desc {{
            font-size: 13px;
            color: var(--text-muted);
        }}

        /* Article Cards Grid */
        .articles-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 20px;
            margin-bottom: 36px;
        }}

        .article-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.15s ease, border-color 0.15s ease, background 0.15s ease;
        }}

        .article-card:hover {{
            background: var(--bg-card-hover);
            border-color: var(--border-highlight);
            transform: translateY(-2px);
        }}

        .card-top {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
        }}

        .card-source {{
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .badge {{
            font-size: 10.5px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            padding: 2px 8px;
            border-radius: 4px;
        }}

        .badge-devtools {{ background: rgba(59, 130, 246, 0.12); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }}
        .badge-local {{ background: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
        .badge-breakthrough {{ background: rgba(245, 158, 11, 0.12); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }}
        .badge-production {{ background: rgba(139, 92, 246, 0.12); color: #a78bfa; border: 1px solid rgba(139, 92, 246, 0.3); }}
        .badge-social {{ background: rgba(236, 72, 153, 0.12); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.3); }}

        .article-title {{
            font-size: 16px;
            font-weight: 700;
            line-height: 1.4;
            color: var(--text-primary);
            text-decoration: none;
            margin-bottom: 12px;
            display: block;
        }}

        .article-title:hover {{
            color: var(--accent-primary-hover);
        }}

        .article-thumb {{
            width: 100%;
            height: 170px;
            object-fit: cover;
            border-radius: var(--radius-sm);
            margin-bottom: 12px;
            border: 1px solid var(--border-subtle);
        }}

        .article-summary {{
            color: var(--text-secondary);
            font-size: 13.5px;
            line-height: 1.6;
            margin-bottom: 14px;
        }}

        .usecase-box {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-subtle);
            border-left: 3px solid var(--accent-primary);
            border-radius: var(--radius-sm);
            padding: 8px 12px;
            font-size: 12.5px;
            color: var(--text-secondary);
            margin-bottom: 14px;
            line-height: 1.5;
        }}

        .usecase-label {{
            font-size: 10.5px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            font-weight: 600;
            margin-bottom: 2px;
        }}

        .card-bottom {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 12px;
            color: var(--text-muted);
            padding-top: 10px;
            border-top: 1px solid var(--border-subtle);
        }}

        .read-link {{
            color: var(--accent-primary);
            text-decoration: none;
            font-weight: 600;
            font-size: 12.5px;
        }}

        .read-link:hover {{
            text-decoration: underline;
        }}

        /* Video Grid */
        .video-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 18px;
        }}

        .video-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }}

        .video-card:hover {{
            border-color: var(--border-highlight);
            transform: translateY(-2px);
        }}

        .video-thumb-wrap {{
            position: relative;
            width: 100%;
            height: 175px;
            background: #000000;
        }}

        .video-thumb {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .video-play-btn {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 44px;
            height: 44px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #ffffff;
            font-size: 16px;
        }}

        .video-info {{
            padding: 14px 16px;
            display: flex;
            flex-direction: column;
            flex: 1;
            justify-content: space-between;
        }}

        .video-title {{
            font-size: 14.5px;
            font-weight: 600;
            color: var(--text-primary);
            text-decoration: none;
            line-height: 1.4;
            margin-bottom: 8px;
        }}

        .video-title:hover {{
            color: var(--accent-primary-hover);
        }}

        .video-meta {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 8px;
        }}

        /* Social Buzz Grid */
        .social-buzz-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 16px;
        }}

        .social-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 16px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }}

        .social-card:hover {{
            border-color: var(--border-highlight);
            transform: translateY(-2px);
        }}

        .social-title {{
            font-size: 14.5px;
            font-weight: 600;
            color: var(--text-primary);
            text-decoration: none;
            line-height: 1.4;
            margin-bottom: 10px;
        }}

        .social-title:hover {{
            color: var(--accent-primary-hover);
        }}

        .social-snippet {{
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.5;
            margin-bottom: 12px;
        }}

        .social-meta {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 12px;
            color: var(--text-muted);
        }}

        /* 1-Liners */
        .oneliner-item {{
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 14px;
        }}

        .oneliner-item:last-child {{
            border-bottom: none;
        }}

        .oneliner-dot {{
            color: var(--accent-primary);
            font-size: 18px;
            line-height: 1;
        }}

        .oneliner-title {{
            color: var(--text-primary);
            text-decoration: none;
            font-weight: 600;
        }}

        .oneliner-title:hover {{
            color: var(--accent-primary-hover);
            text-decoration: underline;
        }}

        .oneliner-desc {{
            color: var(--text-muted);
            font-size: 13.5px;
        }}

        /* ==================== BENCHMARKS & MODELS ==================== */
        .benchmark-section {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 22px;
            margin-bottom: 30px;
        }}

        .benchmark-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 18px;
        }}

        .benchmark-title {{
            font-size: 17px;
            font-weight: 700;
        }}

        .benchmark-desc {{
            font-size: 13px;
            color: var(--text-muted);
            margin-top: 2px;
        }}

        .benchmark-bars-container {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .benchmark-row {{
            display: grid;
            grid-template-columns: 240px 1fr 90px;
            align-items: center;
            gap: 16px;
            padding: 10px 14px;
            border-radius: var(--radius-sm);
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .benchmark-row:hover {{
            background: var(--bg-card-hover);
            border-color: var(--border-highlight);
            transform: translateX(2px);
        }}

        .benchmark-row-meta {{
            display: flex;
            align-items: center;
            gap: 8px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        .benchmark-rank {{
            font-size: 11px;
            font-family: var(--font-mono);
            color: var(--text-muted);
            font-weight: 600;
            width: 24px;
        }}

        .benchmark-model-name {{
            font-size: 14px;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .benchmark-lab-pill {{
            font-size: 10.5px;
            color: var(--text-muted);
            background: rgba(255, 255, 255, 0.05);
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 500;
        }}

        .benchmark-bar-track {{
            background: rgba(255, 255, 255, 0.05);
            height: 10px;
            border-radius: 5px;
            overflow: hidden;
            position: relative;
        }}

        .benchmark-bar-fill {{
            height: 100%;
            border-radius: 5px;
            background: linear-gradient(90deg, #2563eb, #3b82f6);
            transition: width 0.4s ease;
        }}

        .benchmark-bar-fill.frontier {{
            background: linear-gradient(90deg, #3b82f6, #60a5fa);
        }}

        .benchmark-score-val {{
            font-family: var(--font-mono);
            font-size: 13.5px;
            font-weight: 700;
            color: var(--text-primary);
            text-align: right;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 6px;
        }}

        .benchmark-inspect-arrow {{
            color: var(--accent-primary);
            font-size: 12px;
        }}

        /* Lab Filter Bar */
        .lab-filter-bar {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }}

        .lab-chip {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            padding: 7px 14px;
            border-radius: var(--radius-sm);
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .lab-chip:hover {{
            background: var(--bg-card-hover);
            color: var(--text-primary);
        }}

        .lab-chip.active {{
            background: var(--accent-primary);
            border-color: var(--accent-primary);
            color: #ffffff;
            font-weight: 600;
        }}

        .models-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 20px;
        }}

        .model-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            cursor: pointer;
            transition: transform 0.15s ease, border-color 0.15s ease, background 0.15s ease;
        }}

        .model-card:hover {{
            background: var(--bg-card-hover);
            border-color: var(--border-highlight);
            transform: translateY(-2px);
        }}

        .model-lab-badge {{
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
            margin-bottom: 4px;
        }}

        .model-name {{
            font-size: 18px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 10px;
        }}

        .model-specs-row {{
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            margin-bottom: 14px;
        }}

        .spec-pill {{
            font-size: 11px;
            font-family: var(--font-mono);
            color: var(--text-secondary);
            background: rgba(255, 255, 255, 0.04);
            padding: 3px 8px;
            border-radius: 4px;
            border: 1px solid var(--border-subtle);
        }}

        .model-best-for {{
            font-size: 13.5px;
            color: var(--text-secondary);
            line-height: 1.55;
            margin-bottom: 16px;
        }}

        .model-pricing-preview {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-subtle);
            padding: 8px 12px;
            border-radius: var(--radius-sm);
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 12px;
            font-family: var(--font-mono);
        }}

        .inspect-action-text {{
            font-size: 12px;
            font-weight: 600;
            color: var(--accent-primary);
            text-align: right;
        }}

        /* ==================== MILESTONES ARCHIVE ==================== */
        .milestone-period-bar {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 24px;
        }}

        .period-chip {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            padding: 8px 18px;
            border-radius: var(--radius-sm);
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .period-chip:hover {{
            background: var(--bg-card-hover);
            color: var(--text-primary);
        }}

        .period-chip.active {{
            background: var(--accent-primary);
            border-color: var(--accent-primary);
            color: #ffffff;
        }}

        .milestone-group {{
            margin-bottom: 32px;
        }}

        .milestone-group-title {{
            font-size: 19px;
            font-weight: 700;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .milestone-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 18px;
        }}

        .milestone-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 20px;
        }}

        .milestone-lab {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            font-weight: 600;
            margin-bottom: 4px;
        }}

        .milestone-name {{
            font-size: 16px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 8px;
        }}

        .milestone-desc {{
            font-size: 13.5px;
            color: var(--text-secondary);
            line-height: 1.55;
            margin-bottom: 10px;
        }}

        .milestone-impact {{
            font-size: 12.5px;
            color: var(--accent-primary-hover);
            background: rgba(59, 130, 246, 0.08);
            border-left: 2px solid var(--accent-primary);
            padding: 6px 10px;
            border-radius: var(--radius-sm);
            line-height: 1.45;
        }}

        /* ==================== TASKS GUIDE ==================== */
        .tasks-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 20px;
        }}

        .task-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 22px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .task-title {{
            font-size: 17px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 8px;
        }}

        .task-recommendations {{
            margin-top: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .task-rec-item {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-sm);
            padding: 10px 12px;
            font-size: 13px;
            line-height: 1.45;
        }}

        .task-rec-role {{
            font-size: 10.5px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--accent-primary);
            margin-bottom: 2px;
        }}

        /* Model Inspector Drawer */
        .drawer-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.65);
            backdrop-filter: blur(4px);
            z-index: 80;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease;
        }}

        .drawer-overlay.open {{
            opacity: 1;
            pointer-events: auto;
        }}

        .drawer {{
            position: fixed;
            top: 0;
            right: -520px;
            width: 500px;
            max-width: 90vw;
            height: 100vh;
            background: var(--bg-surface);
            border-left: 1px solid var(--border-subtle);
            z-index: 90;
            padding: 28px 24px;
            overflow-y: auto;
            transition: right 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .drawer.open {{
            right: 0;
        }}

        .drawer-close {{
            position: absolute;
            top: 18px;
            right: 18px;
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            color: var(--text-muted);
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .drawer-close:hover {{
            background: var(--bg-card-hover);
            color: var(--text-primary);
        }}

        .tooltip-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }}

        .tooltip-item-label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            font-weight: 600;
        }}

        .tooltip-item-val {{
            font-size: 13.5px;
            font-family: var(--font-mono);
            color: var(--text-primary);
            margin-top: 2px;
        }}

        .code-block {{
            background: #090a0d;
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-sm);
            padding: 12px;
            font-family: var(--font-mono);
            font-size: 12px;
            color: #d1d5db;
            overflow-x: auto;
            white-space: pre;
            line-height: 1.5;
        }}

        /* Share & Modal Styles */
        .share-modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(6px);
            z-index: 100;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease;
        }}

        .share-modal-overlay.open {{
            opacity: 1;
            pointer-events: auto;
        }}

        .share-modal {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0.96);
            width: 440px;
            max-width: 92vw;
            background: var(--bg-surface);
            border: 1px solid var(--border-highlight);
            border-radius: var(--radius-md);
            padding: 24px;
            z-index: 101;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
            opacity: 0;
            pointer-events: none;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .share-modal.open {{
            opacity: 1;
            pointer-events: auto;
            transform: translate(-50%, -50%) scale(1);
        }}

        .share-modal-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }}

        .share-modal-title {{
            font-size: 18px;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .modal-close-btn {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 22px;
            cursor: pointer;
            line-height: 1;
            padding: 4px;
        }}

        .modal-close-btn:hover {{
            color: var(--text-primary);
        }}

        .share-modal-desc {{
            font-size: 13.5px;
            color: var(--text-secondary);
            margin-bottom: 18px;
            line-height: 1.5;
        }}

        .share-preview-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-sm);
            overflow: hidden;
            margin-bottom: 20px;
        }}

        .share-card-thumb {{
            width: 100%;
            height: 150px;
            object-fit: cover;
            display: block;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .share-card-info {{
            padding: 12px 14px;
        }}

        .share-card-title {{
            font-size: 14px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 4px;
            line-height: 1.35;
        }}

        .share-card-desc {{
            font-size: 12px;
            color: var(--text-muted);
            line-height: 1.4;
            margin-bottom: 8px;
        }}

        .share-card-domain {{
            font-size: 11px;
            font-family: var(--font-mono);
            color: #60a5fa;
            text-transform: lowercase;
        }}

        .share-buttons-row {{
            display: flex;
            gap: 10px;
        }}

        .whatsapp-share-btn {{
            flex: 1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background: #25d366;
            color: #0d0f12;
            font-size: 13.5px;
            font-weight: 700;
            padding: 11px 16px;
            border-radius: var(--radius-sm);
            border: none;
            cursor: pointer;
            transition: background 0.15s ease, transform 0.1s ease;
        }}

        .whatsapp-share-btn:hover {{
            background: #20bd5a;
            transform: translateY(-1px);
        }}

        .copy-link-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background: var(--bg-elevated);
            border: 1px solid var(--border-highlight);
            color: var(--text-primary);
            font-size: 13.5px;
            font-weight: 600;
            padding: 11px 16px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .copy-link-btn:hover {{
            background: var(--bg-card-hover);
            border-color: #ffffff;
        }}

        /* Toast notification */
        .toast-notify {{
            position: fixed;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%) translateY(20px);
            background: var(--bg-elevated);
            border: 1px solid var(--border-highlight);
            color: var(--text-primary);
            padding: 10px 20px;
            border-radius: var(--radius-pill);
            font-size: 13px;
            font-weight: 600;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            z-index: 120;
            opacity: 0;
            pointer-events: none;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .toast-notify.show {{
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }}

        /* Responsive Mobile Styles */
        @media (max-width: 768px) {{
            .header-inner {{
                padding: 10px 16px;
                flex-wrap: wrap;
            }}
            .brand-subtitle {{
                display: none;
            }}
            .header-nav-wrap {{
                order: 3;
                width: 100%;
                display: flex;
                align-items: center;
                gap: 8px;
                margin-top: 6px;
                overflow-x: auto;
                padding-bottom: 2px;
            }}
            nav.nav-bar {{
                flex: 1;
                justify-content: flex-start;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }}
            .nav-btn {{
                padding: 7px 11px;
                font-size: 12.5px;
            }}
            .articles-grid, .models-grid, .milestone-grid, .tasks-grid {{
                grid-template-columns: 1fr;
            }}
            .video-grid, .social-buzz-grid {{
                grid-template-columns: 1fr;
            }}
            .benchmark-row {{
                grid-template-columns: 1fr auto;
                gap: 6px 12px;
                padding: 10px 12px;
                background: var(--bg-card);
                margin-bottom: 8px;
                border: 1px solid var(--border-subtle);
            }}
            .benchmark-row-meta {{
                grid-column: 1 / 2;
            }}
            .benchmark-score-val {{
                grid-column: 2 / 3;
                font-size: 13px;
                font-weight: 700;
            }}
            .benchmark-bar-track {{
                grid-column: 1 / 3;
                height: 8px;
            }}
            .milestone-period-bar {{
                gap: 8px;
                flex-wrap: wrap;
            }}
            .period-chip {{
                flex: 1 1 auto;
                text-align: center;
                padding: 8px 12px;
            }}
            .inpage-nav {{
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }}
            .drawer {{
                width: 100vw;
                max-width: 100vw;
                padding: 20px 16px;
            }}
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="header-inner">
            <a href="#" class="brand" onclick="switchView('feed')">
                <div class="brand-icon">⚡</div>
                <div>
                    <div class="brand-title">AI Digest</div>
                    <div class="brand-subtitle">Frontier AI &amp; Developer Intelligence</div>
                </div>
            </a>

            <div class="header-nav-wrap" style="display: flex; align-items: center; gap: 10px;">
                <nav class="nav-bar">
                    <button class="nav-btn active" id="tab-feed" onclick="switchView('feed')">Weekly Digest</button>
                    <button class="nav-btn" id="tab-models" onclick="switchView('models')">Models &amp; Benchmarks</button>
                    <button class="nav-btn" id="tab-milestones" onclick="switchView('milestones')">3-Year Milestones</button>
                    <button class="nav-btn" id="tab-tasks" onclick="switchView('tasks')">Task Guide</button>
                </nav>

                <button class="share-btn" onclick="openShareModal()" title="Share link on WhatsApp or copy URL">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>
                    <span>Share</span>
                </button>
            </div>
        </div>
    </header>

    <!-- Main Content Area -->
    <main>
        <!-- ==================== SECTION 1: WEEKLY DIGEST ==================== -->
        <section id="view-feed">
            <div class="section-header">
                <h1 class="section-title">Weekly AI Intelligence Digest</h1>
                <p class="section-desc">Frontier models, famous Substack analyses, viral community debates, and developer breakthroughs across the past 4 rolling weeks.</p>
            </div>

            <!-- In-Page Sub-Navigation -->
            <div class="inpage-nav-wrap">
                <nav class="inpage-nav" aria-label="Digest Sections">
                    <a href="#articles-section" class="inpage-pill active">📰 Deep Dives</a>
                    <a href="#videos-section" class="inpage-pill">🎥 YouTube</a>
                    <a href="#social-buzz-section" class="inpage-pill">💬 X &amp; Reddit</a>
                    <a href="#oneliners-container" class="inpage-pill">⚡ 1-Liners</a>
                </nav>
            </div>

            <!-- Weekly Edition Filter -->
            <div class="date-filter-section">
                <div class="date-filter-header">
                    <span class="date-filter-label">Weekly Edition (Past 4 Weeks)</span>
                    <span id="active-date-label" style="font-size:12px;color:var(--text-muted);font-family:var(--font-mono);"></span>
                </div>
                <div class="date-filter-bar" id="date-filter-bar">
                    <!-- Dynamically populated weekly chips -->
                </div>
            </div>

            <!-- Topic Filters -->
            <div class="tag-bar">
                <button class="tag-chip active" onclick="setTopicFilter('ALL')">All Stories</button>
                <button class="tag-chip" onclick="setTopicFilter('DEV TOOLS')">💻 Dev Tooling</button>
                <button class="tag-chip" onclick="setTopicFilter('LOCAL AI')">⚡ Local AI &amp; Quant</button>
                <button class="tag-chip" onclick="setTopicFilter('RESEARCH')">🔬 Applied Research</button>
                <button class="tag-chip" onclick="setTopicFilter('PRODUCTION')">🚀 Production &amp; Security</button>
            </div>

            <!-- Instant Search -->
            <div class="search-bar">
                <input type="text" id="search-input" class="search-input" placeholder="Filter stories by model, topic, or keyword (e.g., 'Claude', 'vLLM', '3D')..." oninput="filterArticles()">
            </div>

            <!-- Main Articles Section -->
            <div class="media-section" id="articles-section">
                <div class="media-section-header">
                    <div class="media-section-title">
                        <span>📰 Featured Technical Articles &amp; Research</span>
                        <span class="media-section-badge">Verified Technical In-Depth</span>
                    </div>
                    <div class="media-section-desc">Concise, uniform 100-word deep-dives into models, architectures, and engineering breakthroughs.</div>
                </div>
                <div class="articles-grid" id="articles-grid">
                    <!-- Dynamically populated article cards -->
                </div>
            </div>

            <!-- Featured AI Videos Section -->
            <div class="media-section" id="videos-section">
                <div class="media-section-header">
                    <div class="media-section-title">
                        <span>🎥 Featured AI Videos &amp; Tech Breakdowns</span>
                        <span class="media-section-badge">Fireship, Karpathy &amp; Creators</span>
                    </div>
                    <div class="media-section-desc">Hand-picked high-signal video breakdowns, architectural deep dives, and creator tutorials from the past week.</div>
                </div>
                <div class="video-grid" id="videos-grid">
                    <!-- Dynamically populated video cards -->
                </div>
            </div>

            <!-- Social Media Buzz & Founder Takes Section -->
            <div class="media-section" id="social-buzz-section">
                <div class="media-section-header">
                    <div class="media-section-title">
                        <span>💬 Social Media Buzz &amp; Founder Takes</span>
                        <span class="media-section-badge">Reddit • X / Twitter • Hacker News</span>
                    </div>
                    <div class="media-section-desc">Curated community sentiment, viral engineering debates, founder perspectives, and model releases.</div>
                </div>
                <div class="social-buzz-grid" id="social-buzz-grid">
                    <!-- Dynamically populated social buzz cards -->
                </div>
            </div>

            <!-- Quick-Hit 1-Liners -->
            <div class="media-section" id="oneliners-container">
                <div class="media-section-header">
                    <div class="media-section-title">
                        <span>⚡ Quick-Hit 1-Liners</span>
                        <span class="media-section-badge">Headlines &amp; Snapshots</span>
                    </div>
                    <div class="media-section-desc">Rapid-fire highlights you can scan in under a minute.</div>
                </div>
                <div id="oneliners-list">
                    <!-- Dynamically populated 1-liners -->
                </div>
            </div>
        </section>

        <!-- ==================== SECTION 2: FRONTIER MODELS & BENCHMARKS ==================== -->
        <section id="view-models" style="display:none;">
            <div class="section-header">
                <h1 class="section-title">Frontier Model Intelligence &amp; Benchmarks</h1>
                <p class="section-desc">Verified SWE-bench rankings and comprehensive model specifications. Click any model row to inspect full architectural capabilities, pricing, and developer verdicts.</p>
            </div>

            <!-- Interactive Benchmark Bar Graph -->
            <div class="benchmark-section">
                <div class="benchmark-header">
                    <div>
                        <div class="benchmark-title">🏆 Frontier Benchmark Leaderboard (SWE-bench Verified)</div>
                        <div class="benchmark-desc">Ranked by verified real-world software engineering and deliberate reasoning capabilities.</div>
                        <div style="font-size:11px;color:var(--text-muted);margin-top:4px;font-style:italic;">SWE-bench Verified · Click any row to inspect complete specs, pricing, and developer verdict</div>
                    </div>
                </div>

                <div class="benchmark-bars-container" id="benchmark-bars-container">
                    <!-- Populated dynamically via renderBenchmarkChart() -->
                </div>
            </div>

            <!-- Lab Filter Bar -->
            <div class="lab-filter-bar" id="lab-filter-bar">
                <button class="lab-chip active" onclick="filterModelsByLab('all')">All Labs (Frontier Flagships)</button>
                <button class="lab-chip" onclick="filterModelsByLab('anthropic')">Anthropic</button>
                <button class="lab-chip" onclick="filterModelsByLab('openai')">OpenAI</button>
                <button class="lab-chip" onclick="filterModelsByLab('deepseek')">DeepSeek</button>
                <button class="lab-chip" onclick="filterModelsByLab('google')">Google DeepMind</button>
                <button class="lab-chip" onclick="filterModelsByLab('alibaba')">Alibaba (Qwen)</button>
                <button class="lab-chip" onclick="filterModelsByLab('meta')">Meta AI</button>
            </div>

            <div id="models-view-hint" style="margin-bottom:14px;font-size:13px;color:var(--text-muted);">
                Showing <strong>Frontier Flagships</strong>. Click an organization chip above to view models for that lab.
            </div>

            <!-- Models Grid -->
            <div class="models-grid" id="models-grid">
                <!-- Dynamically populated model cards -->
            </div>
        </section>

        <!-- ==================== SECTION 3: 3-YEAR MILESTONES ARCHIVE ==================== -->
        <section id="view-milestones" style="display:none;">
            <div class="section-header">
                <h1 class="section-title">Landmark AI Milestones Archive (2023 – 2026)</h1>
                <p class="section-desc">Documenting major inflection points, model releases, and architectural breakthroughs across 36 months of AI progress.</p>
            </div>

            <!-- Period Selector Bar -->
            <div class="milestone-period-bar">
                <button class="period-chip" id="pchip-yearly" onclick="switchMilestonePeriod('yearly')">Yearly</button>
                <button class="period-chip active" id="pchip-quarterly" onclick="switchMilestonePeriod('quarterly')">Quarterly</button>
                <button class="period-chip" id="pchip-monthly" onclick="switchMilestonePeriod('monthly')">Monthly</button>
            </div>

            <div id="milestones-container">
                <!-- Dynamically populated milestone groups -->
            </div>
        </section>

        <!-- ==================== SECTION 4: TASK GUIDE ==================== -->
        <section id="view-tasks" style="display:none;">
            <div class="section-header">
                <h1 class="section-title">Task-Based Model Selection Guide</h1>
                <p class="section-desc">Practical engineering recommendations based on latency, benchmark scores, reasoning depth, and cost economics.</p>
            </div>

            <div class="tasks-grid">
                <div class="task-card">
                    <div>
                        <div class="task-title">💻 Agentic Coding &amp; Whole-Repo Refactoring</div>
                        <p style="font-size:14px;color:var(--text-secondary);line-height:1.5;">Tasks requiring multi-file analysis, unit test generation, and autonomous terminal PR execution.</p>
                        <div class="task-recommendations">
                            <div class="task-rec-item">
                                <div class="task-rec-role">Frontier Autonomous Agent</div>
                                <strong>Claude 3.7 Sonnet &amp; Claude 3.5 Sonnet</strong> &bull; #1 SWE-bench Verified (70.3%–74.5%) &amp; Claude Code leader.
                            </div>
                            <div class="task-rec-item">
                                <div class="task-rec-role">Open Weights Champion</div>
                                <strong>Qwen 2.5 Coder 32B &amp; DeepSeek-R1</strong> &bull; SOTA open models runnable on local workstation GPUs.
                            </div>
                        </div>
                    </div>
                </div>

                <div class="task-card">
                    <div>
                        <div class="task-title">📐 Deep Mathematical &amp; Algorithmic Proofs</div>
                        <p style="font-size:14px;color:var(--text-secondary);line-height:1.5;">Heavy formal logic, theorem proving, contest programming, and competitive algorithmic challenges.</p>
                        <div class="task-recommendations">
                            <div class="task-rec-item">
                                <div class="task-rec-role">Maximum Reasoning Throughput</div>
                                <strong>OpenAI o3-mini &amp; OpenAI o1</strong> &bull; Test-time compute scaling leaders (79.7% SWE-bench, 99th percentile math).
                            </div>
                            <div class="task-rec-item">
                                <div class="task-rec-role">Open Architecture Equivalent</div>
                                <strong>DeepSeek-R1 (671B MoE)</strong> &bull; Pure RL chain-of-thought matching proprietary models at 1/20th cost.
                            </div>
                        </div>
                    </div>
                </div>

                <div class="task-card">
                    <div>
                        <div class="task-title">📚 Massive Multi-Document &amp; Codebase Context (1M+ Tokens)</div>
                        <p style="font-size:14px;color:var(--text-secondary);line-height:1.5;">Analyzing whole codebases, legal portfolios, or large audio/video archives in one prompt.</p>
                        <div class="task-recommendations">
                            <div class="task-rec-item">
                                <div class="task-rec-role">2M Token Champion</div>
                                <strong>Gemini 2.0 Pro (2,000,000 Tokens)</strong> &bull; Whole repository comprehension with deep multimodal reasoning.
                            </div>
                            <div class="task-rec-item">
                                <div class="task-rec-role">Ultra-Fast 1M Context</div>
                                <strong>Gemini 2.0 Flash ($0.10/1M)</strong> &bull; Sub-second latency and real-time streaming tool orchestration.
                            </div>
                        </div>
                    </div>
                </div>

                <div class="task-card">
                    <div>
                        <div class="task-title">🔒 Air-Gapped &amp; Private Local Inference</div>
                        <p style="font-size:14px;color:var(--text-secondary);line-height:1.5;">Strict zero-data-leakage environments, offline mobile devices, or high-security applications.</p>
                        <div class="task-recommendations">
                            <div class="task-rec-item">
                                <div class="task-rec-role">High Reasoning on Single GPU</div>
                                <strong>DeepSeek-R1-Distill-Qwen-32B</strong> &bull; Runs locally on single RTX 4090 or Apple Silicon Mac.
                            </div>
                            <div class="task-rec-item">
                                <div class="task-rec-role">Open Foundation Flagship</div>
                                <strong>Llama 3.3 70B</strong> &bull; Full enterprise weights ownership without cloud vendor lock-in.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Model Detail Drawer -->
    <div class="drawer-overlay" id="drawer-overlay" onclick="closeModelDrawer()"></div>
    <div class="drawer" id="model-drawer">
        <button class="drawer-close" onclick="closeModelDrawer()">&times;</button>
        <div id="drawer-content">
            <!-- Dynamically populated model detail -->
        </div>
    </div>

    <!-- Share Modal -->
    <div id="share-modal-overlay" class="share-modal-overlay" onclick="closeShareModal()"></div>
    <div id="share-modal" class="share-modal">
        <div class="share-modal-header">
            <div class="share-modal-title">Share AI Digest</div>
            <button class="modal-close-btn" onclick="closeShareModal()">&times;</button>
        </div>
        <p class="share-modal-desc">Send this link to anyone on WhatsApp, Slack, or Twitter with populated rich preview metadata.</p>
        
        <div class="share-preview-card">
            <img src="/og-preview.jpg" alt="Preview Thumbnail" class="share-card-thumb">
            <div class="share-card-info">
                <div class="share-card-title" id="share-card-title">AI Digest — Frontier AI &amp; Developer Intelligence</div>
                <div class="share-card-desc">Frontier models, verified SWE-bench leaderboards, community debates, and developer benchmarks.</div>
                <div class="share-card-domain" id="share-card-domain">ai-digest-by-mp.vercel.app</div>
            </div>
        </div>

        <div class="share-buttons-row">
            <button class="whatsapp-share-btn" onclick="shareToWhatsApp()">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.698.058-2.124-.537-1.708-.713-2.799-2.464-2.883-2.578-.086-.115-.695-.925-.695-1.764s.438-1.25.594-1.42c.156-.17.34-.213.454-.213.113 0 .227.002.326.007.104.005.244-.04.382.29.144.346.491 1.198.534 1.285.043.085.072.186.014.3-.058.115-.088.186-.174.288-.087.101-.183.226-.262.304-.087.086-.177.18-.076.353.101.173.449.741.964 1.201.663.591 1.221.774 1.394.86.173.086.275.072.376-.044.101-.115.433-.505.549-.678.115-.173.231-.144.39-.086.159.058 1.01.477 1.184.564.173.086.289.13.332.202.043.072.043.419-.101.824zM12 2C6.477 2 2 6.477 2 12c0 1.891.524 3.66 1.434 5.174L2 22l4.981-1.306A9.957 9.957 0 0 0 12 22c5.523 0 10-4.477 10-10S17.523 2 12 2z"/></svg>
                <span>Send via WhatsApp</span>
            </button>
            <button class="copy-link-btn" onclick="copyCurrentLink()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                <span id="copy-btn-text">Copy Link</span>
            </button>
        </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast-notify" class="toast-notify">Link copied to clipboard!</div>

    <!-- Application Logic -->
    <script>
        // Injected Datasets
        const EMBEDDED_SEED = {seed_json_str};
        const FRONTIER_MODELS = {models_json_str};
        const MILESTONES_ARCHIVE = {milestones_json_str};

        let currentActiveWeekId = null;
        let selectedTopicFilter = "ALL";
        let activeView = "feed";

        // URL Deep-Linking & State Synchronization
        function updateUrlState(params) {{
            const url = new URL(window.location);
            Object.keys(params).forEach(key => {{
                if (params[key] === null || params[key] === undefined) {{
                    url.searchParams.delete(key);
                }} else {{
                    url.searchParams.set(key, params[key]);
                }}
            }});
            window.history.replaceState({{}}, '', url);
        }}

        function initFromUrl() {{
            const params = new URLSearchParams(window.location.search);
            const tab = params.get("tab") || "feed";
            const inspectModel = params.get("inspect");
            const weekParam = params.get("week");

            if (tab && ["feed", "models", "milestones", "tasks"].includes(tab)) {{
                switchView(tab, false);
            }}

            if (weekParam && EMBEDDED_SEED[weekParam]) {{
                currentActiveWeekId = weekParam;
            }}

            if (inspectModel) {{
                setTimeout(() => openModelDrawer(inspectModel, false), 300);
            }}
        }}

        window.addEventListener("popstate", () => {{
            const params = new URLSearchParams(window.location.search);
            const tab = params.get("tab") || "feed";
            switchView(tab, false);
            const inspect = params.get("inspect");
            if (inspect) {{
                openModelDrawer(inspect, false);
            }} else {{
                closeModelDrawer(false);
            }}
        }});

        // 1. Navigation Controller
        function switchView(viewId, updateHistory = true) {{
            activeView = viewId;
            document.querySelectorAll("main > section").forEach(sec => sec.style.display = "none");
            document.querySelectorAll(".nav-btn").forEach(btn => btn.classList.remove("active"));
            
            const targetSec = document.getElementById(`view-${{viewId}}`);
            const targetBtn = document.getElementById(`tab-${{viewId}}`);
            if (targetSec) targetSec.style.display = "block";
            if (targetBtn) targetBtn.classList.add("active");

            if (updateHistory) {{
                updateUrlState({{ tab: viewId === 'feed' ? null : viewId }});
            }}

            const titles = {{
                feed: "AI Digest — Frontier AI & Developer Intelligence",
                models: "Frontier Models & Benchmarks — AI Digest",
                milestones: "3-Year AI Milestones Archive — AI Digest",
                tasks: "Developer Task Guide — AI Digest"
            }};
            document.title = titles[viewId] || titles.feed;

            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        // Share Dialog Functions
        function openShareModal() {{
            const modal = document.getElementById("share-modal");
            const overlay = document.getElementById("share-modal-overlay");
            const domainElem = document.getElementById("share-card-domain");
            const titleElem = document.getElementById("share-card-title");
            if (domainElem) domainElem.innerText = window.location.host || "ai-digest-by-mp.vercel.app";
            if (titleElem) titleElem.innerText = document.title;
            overlay.classList.add("open");
            modal.classList.add("open");
        }}

        function closeShareModal() {{
            document.getElementById("share-modal-overlay").classList.remove("open");
            document.getElementById("share-modal").classList.remove("open");
        }}

        function shareToWhatsApp() {{
            const text = `${{document.title}}: ${{window.location.href}}`;
            window.open(`https://api.whatsapp.com/send?text=${{encodeURIComponent(text)}}`, "_blank");
            closeShareModal();
        }}

        async function copyCurrentLink() {{
            try {{
                await navigator.clipboard.writeText(window.location.href);
                showToast("Link copied to clipboard! Ready to share.");
                closeShareModal();
            }} catch(e) {{
                showToast("Could not copy link automatically: " + window.location.href);
            }}
        }}

        function shareModelToWhatsApp(modelId, modelName) {{
            const shareUrl = new URL(window.location.origin + window.location.pathname);
            shareUrl.searchParams.set("tab", "models");
            shareUrl.searchParams.set("inspect", modelId);
            const text = `Check out ${{modelName}} on AI Digest: ${{shareUrl.toString()}}`;
            window.open(`https://api.whatsapp.com/send?text=${{encodeURIComponent(text)}}`, "_blank");
        }}

        function copyModelLink(modelId) {{
            const shareUrl = new URL(window.location.origin + window.location.pathname);
            shareUrl.searchParams.set("tab", "models");
            shareUrl.searchParams.set("inspect", modelId);
            navigator.clipboard.writeText(shareUrl.toString()).then(() => {{
                showToast("Model link copied to clipboard!");
            }});
        }}

        function showToast(msg) {{
            const toast = document.getElementById("toast-notify");
            if (!toast) return;
            toast.innerText = msg;
            toast.classList.add("show");
            setTimeout(() => toast.classList.remove("show"), 3200);
        }}

        // Weekly Editions Setup
        const DEFAULT_WEEKLY_WINDOWS = [
            {{ id: "2026-08-30_2026-09-05", label: "Aug 30 – Sep 05, 2026", short_label: "Aug 30 – Sep 05", start: "2026-08-30", end: "2026-09-05", is_current: true }},
            {{ id: "2026-08-23_2026-08-29", label: "Aug 23 – Aug 29, 2026", short_label: "Aug 23 – Aug 29", start: "2026-08-23", end: "2026-08-29", is_current: false }},
            {{ id: "2026-08-16_2026-08-22", label: "Aug 16 – Aug 22, 2026", short_label: "Aug 16 – Aug 22", start: "2026-08-16", end: "2026-08-22", is_current: false }},
            {{ id: "2026-08-09_2026-08-15", label: "Aug 09 – Aug 15, 2026", short_label: "Aug 09 – Aug 15", start: "2026-08-09", end: "2026-08-15", is_current: false }}
        ];

        function getWeeksList() {{
            const seedKeys = Object.keys(EMBEDDED_SEED);
            if (seedKeys.length > 0) {{
                return seedKeys.sort().reverse().map((k, idx) => ({{
                    id: k,
                    label: EMBEDDED_SEED[k].week_label || k,
                    short_label: EMBEDDED_SEED[k].short_label || k,
                    is_current: idx === 0
                }}));
            }}
            return DEFAULT_WEEKLY_WINDOWS;
        }}

        function loadSeedDataset() {{
            const weeks = getWeeksList();
            renderWeeklyChips(weeks);
            const initialWeek = currentActiveWeekId || weeks[0].id;
            selectWeeklyEdition(initialWeek);
        }}

        function renderWeeklyChips(weeks) {{
            const container = document.getElementById("date-filter-bar");
            container.innerHTML = weeks.map((w, idx) => `
                <button class="date-chip ${{w.id === currentActiveWeekId || (!currentActiveWeekId && idx === 0) ? 'active' : ''}}" 
                        id="chip-${{w.id}}" 
                        onclick="selectWeeklyEdition('${{w.id}}')">
                    ${{escapeHtml(w.short_label)}} ${{w.is_current ? '⚡' : ''}}
                </button>
            `).join("");
        }}

        function selectWeeklyEdition(weekId) {{
            currentActiveWeekId = weekId;
            document.querySelectorAll(".date-chip").forEach(c => c.classList.remove("active"));
            const activeChip = document.getElementById(`chip-${{weekId}}`);
            if (activeChip) activeChip.classList.add("active");

            const weekObj = EMBEDDED_SEED[weekId];
            const dateLabel = document.getElementById("active-date-label");
            if (weekObj) {{
                dateLabel.innerText = `${{weekObj.week_label || weekId}} · SOTA Intelligence`;
            }} else {{
                dateLabel.innerText = weekId;
            }}

            updateUrlState({{ week: weekId }});
            filterArticles();
        }}

        function setTopicFilter(topic) {{
            selectedTopicFilter = topic;
            document.querySelectorAll(".tag-chip").forEach(c => c.classList.remove("active"));
            if (window.event && window.event.target) {{
                window.event.target.classList.add("active");
            }}
            filterArticles();
        }}

        function filterArticles() {{
            const query = (document.getElementById("search-input").value || "").toLowerCase().trim();
            const weekObj = EMBEDDED_SEED[currentActiveWeekId];
            
            const articlesGrid = document.getElementById("articles-grid");
            const videosGrid = document.getElementById("videos-grid");
            const socialGrid = document.getElementById("social-buzz-grid");
            const onelinersList = document.getElementById("oneliners-list");
            const videosSection = document.getElementById("videos-section");
            const socialSection = document.getElementById("social-buzz-section");

            if (!weekObj) {{
                articlesGrid.innerHTML = `<div style="grid-column: 1/-1; padding: 40px; text-align: center; color: var(--text-muted);">No items recorded for this weekly edition.</div>`;
                videosSection.style.display = "none";
                socialSection.style.display = "none";
                onelinersList.innerHTML = "";
                return;
            }}

            const topArticles = weekObj.top_articles || weekObj.top_10 || [];
            const videos = weekObj.videos || [];
            const socialBuzz = weekObj.social_buzz || [];
            const oneliners = weekObj.one_liners || [];

            // Filter & Render Top Articles (Strictly genuine articles, no social media, no YouTube)
            const filteredArticles = topArticles.filter(art => matchesSearchAndTopic(art, query, selectedTopicFilter));
            if (filteredArticles.length === 0) {{
                articlesGrid.innerHTML = `<div style="grid-column: 1/-1; padding: 30px 0; color: var(--text-muted);">No matching articles found for this filter.</div>`;
            }} else {{
                articlesGrid.innerHTML = filteredArticles.map(art => renderArticleCard(art)).join("");
            }}

            // Filter & Render Featured Videos
            const filteredVideos = videos.filter(v => matchesSearchAndTopic(v, query, selectedTopicFilter));
            if (filteredVideos.length > 0) {{
                videosSection.style.display = "block";
                videosGrid.innerHTML = filteredVideos.map(v => renderVideoCard(v)).join("");
            }} else {{
                videosSection.style.display = "none";
            }}

            // Filter & Render Social Media Buzz & Founder Takes
            const filteredSocial = socialBuzz.filter(s => matchesSearchAndTopic(s, query, selectedTopicFilter));
            if (filteredSocial.length > 0) {{
                socialSection.style.display = "block";
                socialGrid.innerHTML = filteredSocial.map(s => renderSocialCard(s)).join("");
            }} else {{
                socialSection.style.display = "none";
            }}

            // Filter & Render 1-Liners (Safe check on count element)
            const filteredOneLiners = oneliners.filter(art => matchesSearchAndTopic(art, query, selectedTopicFilter)).slice(0, 15);
            const onelinerCountEl = document.getElementById("oneliner-count");
            if (onelinerCountEl) {{
                onelinerCountEl.innerText = `(${{filteredOneLiners.length}} items)`;
            }}

            if (filteredOneLiners.length === 0) {{
                onelinersList.innerHTML = `<div style="color:var(--text-muted);font-size:13px;padding:8px 0;">No quick-hit items for this week.</div>`;
            }} else {{
                onelinersList.innerHTML = filteredOneLiners.map(art => `
                    <div class="oneliner-item">
                        <span class="oneliner-dot">&bull;</span>
                        <div>
                            <a href="${{art.url}}" target="_blank" class="oneliner-title">${{escapeHtml(art.title)}}</a>
                            <span class="oneliner-desc"> — ${{escapeHtml(art.one_liner || art.summary || '')}}</span>
                        </div>
                    </div>
                `).join("");
            }}
        }}

        function matchesSearchAndTopic(art, query, topic) {{
            if (topic !== "ALL" && art.category_tag !== topic) return false;
            if (!query) return true;
            const fullStr = `${{art.title || ''}} ${{art.summary || ''}} ${{art.source || ''}} ${{art.dev_use_case || ''}}`.toLowerCase();
            return fullStr.includes(query);
        }}

        function renderVideoCard(v) {{
            const thumbUrl = v.image_url || (v.video_id ? `https://i3.ytimg.com/vi/${{v.video_id}}/hqdefault.jpg` : '');
            const dateStr = v.published ? new Date(v.published).toLocaleDateString("en-US", {{ month: 'short', day: 'numeric' }}) : '';
            return `
                <div class="video-card">
                    <a href="${{v.url}}" target="_blank" class="video-thumb-wrap">
                        <img src="${{thumbUrl}}" alt="Video Thumbnail" class="video-thumb" onerror="this.style.display='none'">
                        <div class="video-play-btn">▶</div>
                    </a>
                    <div class="video-info">
                        <div>
                            <a href="${{v.url}}" target="_blank" class="video-title">${{escapeHtml(v.title)}}</a>
                        </div>
                        <div class="video-meta">
                            <span>${{escapeHtml(v.source)}}</span>
                            <span>${{dateStr}}</span>
                        </div>
                    </div>
                </div>
            `;
        }}

        function renderSocialCard(s) {{
            const dateStr = s.published ? new Date(s.published).toLocaleDateString("en-US", {{ month: 'short', day: 'numeric' }}) : '';
            return `
                <div class="social-card">
                    <div>
                        <div class="card-top">
                            <span class="badge badge-social">${{escapeHtml(s.source)}}</span>
                            <span class="card-source">${{s.community_score ? `🔥 ${{s.community_score}} points` : ''}}</span>
                        </div>
                        <a href="${{s.url}}" target="_blank" class="social-title">${{escapeHtml(s.title)}}</a>
                        <p class="social-snippet">${{escapeHtml(s.summary || s.raw_text || '')}}</p>
                    </div>
                    <div class="card-bottom">
                        <span>${{dateStr}}</span>
                        <a href="${{s.url}}" target="_blank" class="read-link">View Thread ↗</a>
                    </div>
                </div>
            `;
        }}

        function renderArticleCard(art) {{
            let badgeClass = "badge-devtools";
            let badgeLabel = "DEV TOOLS";
            if (art.category_tag === "LOCAL AI") {{ badgeClass = "badge-local"; badgeLabel = "LOCAL AI"; }}
            else if (art.category_tag === "BREAKTHROUGH") {{ badgeClass = "badge-breakthrough"; badgeLabel = "BREAKTHROUGH"; }}
            else if (art.category_tag === "PRODUCTION") {{ badgeClass = "badge-production"; badgeLabel = "PRODUCTION"; }}

            const dateStr = art.published ? new Date(art.published).toLocaleDateString("en-US", {{ month: 'short', day: 'numeric' }}) : '';
            const imgHtml = art.image_url ? `<img src="${{art.image_url}}" alt="" class="article-thumb" onerror="this.style.display='none'">` : '';
            const useCaseHtml = art.dev_use_case ? `
                <div class="usecase-box">
                    <div class="usecase-label">Takeaway for Engineers</div>
                    ${{escapeHtml(art.dev_use_case)}}
                </div>
            ` : '';

            return `
                <article class="article-card">
                    <div>
                        <div class="card-top">
                            <span class="badge ${{badgeClass}}">${{badgeLabel}}</span>
                            <span class="card-source">${{escapeHtml(art.source)}}</span>
                        </div>
                        <a href="${{art.url}}" target="_blank" class="article-title">${{escapeHtml(art.title)}}</a>
                        ${{imgHtml}}
                        <p class="article-summary">${{escapeHtml(art.summary || '')}}</p>
                        ${{useCaseHtml}}
                    </div>
                    <div class="card-bottom">
                        <span>${{dateStr}}</span>
                        <a href="${{art.url}}" target="_blank" class="read-link">Read Source ↗</a>
                    </div>
                </article>
            `;
        }}

        // Interactive Benchmark Bar Chart (Clean, responsive, zero placeholder tooltips)
        function renderBenchmarkChart() {{
            const container = document.getElementById("benchmark-bars-container");
            const sortedModels = [...FRONTIER_MODELS].sort((a, b) => b.benchmark_score - a.benchmark_score);
            const maxScore = 85.0;

            container.innerHTML = sortedModels.map((m, idx) => {{
                const pct = Math.min(100, ((m.benchmark_score / maxScore) * 100)).toFixed(1);
                return `
                    <div class="benchmark-row" 
                         data-model-id="${{m.id}}"
                         onclick="openModelDrawer('${{m.id}}')"
                         role="button"
                         tabindex="0"
                         title="Click to inspect ${{escapeHtml(m.name)}} full specs">
                        <div class="benchmark-row-meta">
                            <span class="benchmark-rank">#${{idx + 1}}</span>
                            <span class="benchmark-model-name">${{escapeHtml(m.name)}}</span>
                            <span class="benchmark-lab-pill">${{escapeHtml(m.lab)}}</span>
                        </div>
                        <div class="benchmark-bar-track">
                            <div class="benchmark-bar-fill ${{m.is_frontier ? 'frontier' : ''}}" style="width: ${{pct}}%;"></div>
                        </div>
                        <div class="benchmark-score-val">
                            <span>${{m.benchmark_score}}%</span>
                            <span class="benchmark-inspect-arrow">↗</span>
                        </div>
                    </div>
                `;
            }}).join("");
        }}

        // Models Grid: Frontier Flagships vs Full Org
        function filterModelsByLab(labSlug, btnEl) {{
            document.querySelectorAll(".lab-chip").forEach(c => c.classList.remove("active"));
            const target = btnEl || (window.event && window.event.target) || document.querySelector(".lab-chip");
            if (target && target.classList) target.classList.add("active");

            const hintEl = document.getElementById("models-view-hint");

            if (labSlug === "all") {{
                const frontierOnly = FRONTIER_MODELS.filter(m => m.is_frontier);
                hintEl.innerHTML = `Showing <strong>Frontier Flagships</strong> (${{frontierOnly.length}} models). Click a specific lab chip above to see models for that organization.`;
                renderModelsGrid(frontierOnly);
            }} else {{
                const orgModels = FRONTIER_MODELS.filter(m => m.lab_slug === labSlug);
                const labName = orgModels.length > 0 ? orgModels[0].lab : labSlug;
                hintEl.innerHTML = `Showing all <strong>${{escapeHtml(labName)}}</strong> models (${{orgModels.length}} models).`;
                renderModelsGrid(orgModels);
            }}
        }}

        function renderModelsGrid(models) {{
            const grid = document.getElementById("models-grid");
            grid.innerHTML = models.map(m => `
                <div class="model-card" onclick="openModelDrawer('${{m.id}}')">
                    <div>
                        <div class="model-lab-badge">${{escapeHtml(m.lab)}} &bull; ${{m.release_date || m.year}}</div>
                        <div class="model-name">${{escapeHtml(m.name)}}</div>
                        <div class="model-specs-row">
                            <span class="spec-pill">${{m.context_window}}</span>
                            <span class="spec-pill">${{m.pricing_input}}</span>
                            <span class="spec-pill" style="color:#60a5fa;">${{m.benchmark_score}}% SWE-bench</span>
                        </div>
                        <p class="model-best-for">${{escapeHtml(m.best_for)}}</p>
                    </div>
                    <div>
                        <div class="model-pricing-preview">
                            <span>In: ${{m.pricing_input}}</span>
                            <span>Out: ${{m.pricing_output}}</span>
                        </div>
                        <div class="inspect-action-text">Inspect Full Specs &amp; Verdict ↗</div>
                    </div>
                </div>
            `).join("");
        }}

        // Model Inspector Drawer
        function openModelDrawer(modelId, updateHistory = true) {{
            const m = FRONTIER_MODELS.find(x => x.id === modelId);
            if (!m) return;

            if (updateHistory) {{
                updateUrlState({{ tab: 'models', inspect: modelId }});
            }}

            const content = document.getElementById("drawer-content");
            content.innerHTML = `
                <div class="model-lab-badge">${{escapeHtml(m.lab)}} &bull; Released ${{m.release_date || m.year}}</div>
                <h2 style="font-size: 22px; font-weight: 700; margin-bottom: 12px; color: #ffffff;">${{escapeHtml(m.name)}}</h2>
                
                <div class="usecase-box" style="margin-bottom: 20px;">
                    <div class="usecase-label">Developer Verdict: Is it better to work with?</div>
                    ${{escapeHtml(m.better_to_work_with || 'Proven production reliability for engineering workflows.')}}
                </div>

                <div class="tooltip-grid" style="margin-bottom: 20px;">
                    <div>
                        <div class="tooltip-item-label">Context Window</div>
                        <div class="tooltip-item-val">${{m.context_window}}</div>
                    </div>
                    <div>
                        <div class="tooltip-item-label">Max Output Tokens</div>
                        <div class="tooltip-item-val">${{m.max_output}}</div>
                    </div>
                    <div>
                        <div class="tooltip-item-label">Input Pricing</div>
                        <div class="tooltip-item-val">${{m.pricing_input}}</div>
                    </div>
                    <div>
                        <div class="tooltip-item-label">Output Pricing</div>
                        <div class="tooltip-item-val">${{m.pricing_output}}</div>
                    </div>
                    <div>
                        <div class="tooltip-item-label">Cached Input</div>
                        <div class="tooltip-item-val">${{m.pricing_cached}}</div>
                    </div>
                    <div>
                        <div class="tooltip-item-label">Benchmark Score</div>
                        <div class="tooltip-item-val">${{m.benchmark_score}}% (${{escapeHtml(m.benchmark_label)}})</div>
                    </div>
                </div>

                <div style="margin-bottom: 18px;">
                    <div class="tooltip-item-label" style="margin-bottom: 6px;">Key Capabilities</div>
                    <div style="display: flex; gap: 6px; flex-wrap: wrap;">
                        ${{m.capabilities.map(c => `<span class="spec-pill">${{escapeHtml(c)}}</span>`).join("")}}
                    </div>
                </div>

                <div style="margin-bottom: 20px;">
                    <div class="tooltip-item-label" style="margin-bottom: 6px;">Best Used For</div>
                    <p style="font-size: 14px; color: var(--text-secondary); line-height: 1.5;">${{escapeHtml(m.best_for)}}</p>
                </div>

                <div>
                    <div class="tooltip-item-label" style="margin-bottom: 6px;">Integration Snippet</div>
                    <div class="code-block">${{escapeHtml(m.api_snippet)}}</div>
                </div>

                <div style="display: flex; gap: 8px; margin-top: 20px;">
                    <button class="whatsapp-share-btn" style="flex: 1; padding: 10px 14px; font-size: 13px;" onclick="shareModelToWhatsApp('${{m.id}}', '${{escapeHtml(m.name)}}')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.698.058-2.124-.537-1.708-.713-2.799-2.464-2.883-2.578-.086-.115-.695-.925-.695-1.764s.438-1.25.594-1.42c.156-.17.34-.213.454-.213.113 0 .227.002.326.007.104.005.244-.04.382.29.144.346.491 1.198.534 1.285.043.085.072.186.014.3-.058.115-.088.186-.174.288-.087.101-.183.226-.262.304-.087.086-.177.18-.076.353.101.173.449.741.964 1.201.663.591 1.221.774 1.394.86.173.086.289.13.332.202.043.072.043.419-.101.824zM12 2C6.477 2 2 6.477 2 12c0 1.891.524 3.66 1.434 5.174L2 22l4.981-1.306A9.957 9.957 0 0 0 12 22c5.523 0 10-4.477 10-10S17.523 2 12 2z"/></svg>
                        <span>Share on WhatsApp</span>
                    </button>
                    <button class="copy-link-btn" style="padding: 10px 14px; font-size: 13px;" onclick="copyModelLink('${{m.id}}')">
                        <span>Copy Link</span>
                    </button>
                </div>
            `;

            document.getElementById("drawer-overlay").classList.add("open");
            document.getElementById("model-drawer").classList.add("open");
        }}

        function closeModelDrawer(updateHistory = true) {{
            document.getElementById("drawer-overlay").classList.remove("open");
            document.getElementById("model-drawer").classList.remove("open");
            if (updateHistory) {{
                updateUrlState({{ inspect: null }});
            }}
        }}

        // Milestones Archive
        function switchMilestonePeriod(periodKey) {{
            document.querySelectorAll(".period-chip").forEach(c => c.classList.remove("active"));
            const activeChip = document.getElementById(`pchip-${{periodKey}}`);
            if (activeChip) activeChip.classList.add("active");

            const container = document.getElementById("milestones-container");
            const dataList = MILESTONES_ARCHIVE[periodKey] || [];

            if (dataList.length === 0) {{
                container.innerHTML = `<div class="empty-state" style="padding:40px;text-align:center;color:var(--text-muted);">No milestones recorded for this period.</div>`;
                return;
            }}

            container.innerHTML = dataList.map(group => `
                <div class="milestone-group">
                    <div class="milestone-group-title">
                        <span>🏆 ${{group.period}}</span>
                    </div>
                    <div class="milestone-grid">
                        ${{group.top3.map(item => `
                            <div class="milestone-card">
                                <div class="milestone-lab">${{escapeHtml(item.lab)}} &bull; ${{item.date}}</div>
                                <div class="milestone-name">${{escapeHtml(item.title)}}</div>
                                <p class="milestone-desc">${{escapeHtml(item.capability)}}</p>
                                ${{item.impact ? `
                                    <div class="milestone-impact">
                                        <strong>Engineering Impact:</strong> ${{escapeHtml(item.impact)}}
                                    </div>
                                ` : ''}}
                            </div>
                        `).join("")}}
                    </div>
                </div>
            `).join("");
        }}

        // Utility
        function escapeHtml(str) {{
            if (!str) return "";
            return String(str)
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;");
        }}

        // Initialize on load
        window.addEventListener("DOMContentLoaded", () => {{
            loadSeedDataset();
            renderBenchmarkChart();
            filterModelsByLab("all");
            switchMilestonePeriod("quarterly");
            initFromUrl();

            // Client-side Canonical & OG synchronization
            try {{
                const origin = window.location.origin;
                if (origin && !origin.startsWith("file://")) {{
                    const ogUrl = document.querySelector('meta[property="og:url"]');
                    if (ogUrl) ogUrl.setAttribute("content", window.location.href);
                    const ogImg = document.querySelector('meta[property="og:image"]');
                    if (ogImg && ogImg.getAttribute("content").startsWith("https://ai-digest-by-mp.vercel.app")) {{
                        ogImg.setAttribute("content", `${{origin}}/og-preview.jpg`);
                    }}
                }}
            }} catch(e) {{}}
        }});
    </script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Successfully built Minimalist Reader index.html!")
