#!/usr/bin/env python3
"""
build_webapp.py - Generates the Spotify-inspired, authentic AI Pulse Web Application.
Features:
  - Spotify dark matte aesthetic (#121212 base, #181818 cards, #1ed760 emerald green accents).
  - Hashtag topic filtering & live instant search.
  - Complete Frontier Model Tracker grouped by Lab with interactive Model Inspection Drawer (pricing, context, specs, CLI commands).
  - 3-Year Milestones Archive (Yearly, 6-Month, Quarterly, Monthly, and Weekly Top 3).
  - Removal of arbitrary score numbers in favor of authentic capability and readiness badges.
  - Quiet, clean Supabase integration without tacky header buttons.
"""

import json
from pathlib import Path

# Load seed data if available
seed_file = Path("seed_7days.json")
if seed_file.exists():
    with open(seed_file, "r") as f:
        seed_data = json.load(f)
else:
    seed_data = {}

seed_json_str = json.dumps(seed_data)

# Milestone data for 3-Year Archive (2023 - 2026)
MILESTONES_ARCHIVE = {
    "yearly": [
        {
            "period": "2026",
            "top3": [
                {
                    "title": "Hybrid Reasoning & Test-Time Compute Scaling Across Frontier Labs",
                    "lab": "Anthropic & Google DeepMind",
                    "capability": "Claude 3.7 Sonnet introduces continuous dynamic thinking budgets; Gemini 3.8 Flash achieves 1M-token multimodal test-time deliberation.",
                    "date": "Q1 2026",
                    "impact": "Engineers no longer choose between fast chat and reasoning models; thinking duration is dynamically controlled in production code."
                },
                {
                    "title": "DeepSeek-R1 Open-Weights Revolution",
                    "lab": "DeepSeek AI",
                    "capability": "First open-weights 671B MoE model demonstrating that large-scale pure reinforcement learning achieves parity with OpenAI o1.",
                    "date": "Early 2026",
                    "impact": "Democratized frontier reasoning globally; sparked distillation into compact 14B/32B models run locally on consumer GPUs."
                },
                {
                    "title": "Autonomous Computer-Use & Multi-Hour Coding Agents",
                    "lab": "Anthropic, OpenAI & DeepMind",
                    "capability": "Claude Opus 5 Auto Mode and Gemini 2.5 Computer Use perform complex, long-horizon desktop tasks and repository-wide refactoring autonomously.",
                    "date": "Mid 2026",
                    "impact": "Software engineering moves from code autocomplete to autonomous agent pair-programmers executing end-to-end PRs and unit tests."
                }
            ]
        },
        {
            "period": "2025",
            "top3": [
                {
                    "title": "The Reasoning Paradigm Shift (OpenAI o1 & o3)",
                    "lab": "OpenAI",
                    "capability": "Internal chain-of-thought scaling before generating output tokens, achieving 99th percentile on USA Math Olympiad and Codeforces.",
                    "date": "Late 2025",
                    "impact": "Established that test-time compute represents a new scaling dimension beyond pre-training parameters."
                },
                {
                    "title": "Single-Node Frontier Distillation (Llama 3.3 70B & Qwen 2.5 Coder 32B)",
                    "lab": "Meta AI & Alibaba",
                    "capability": "Compression of 405B-grade foundational intelligence into 32B and 70B footprints runnable on dual workstation GPUs.",
                    "date": "Mid 2025",
                    "impact": "Enterprise self-hosted models achieve SOTA coding without cloud vendor lock-in or data sovereignty compromises."
                },
                {
                    "title": "DeepSeek-V3 Multi-Head Latent Attention (MLA) Architecture",
                    "lab": "DeepSeek AI",
                    "capability": "Trained a 671B MoE model for just $6M using DualPipe and FP8 mixed precision, drastically lowering inference KV cache memory.",
                    "date": "December 2025",
                    "impact": "Re-architected enterprise LLM deployment economics, enabling 3x token throughput per server node."
                }
            ]
        },
        {
            "period": "2024",
            "top3": [
                {
                    "title": "AlphaFold 3: Modeling the Entire Biomolecular Universe",
                    "lab": "Google DeepMind & Isomorphic Labs",
                    "capability": "Predicts structures and interactions of proteins, DNA, RNA, ligands, and chemical modifications in a unified diffusion architecture.",
                    "date": "May 2024",
                    "impact": "Revolutionized drug discovery, oncology target identification, and synthetic biology worldwide."
                },
                {
                    "title": "Claude 3.5 Sonnet: The Coding Benchmark SOTA",
                    "lab": "Anthropic",
                    "capability": "Achieved 64% on SWE-bench Verified alongside the launch of Artifacts, redefining the standard for software developer assistants.",
                    "date": "June 2024",
                    "impact": "Became the universal default model powering Cursor, Aider, Cline, and modern agentic engineering workflows."
                },
                {
                    "title": "Million-Token Context & Generative World Models (Gemini 1.5 & Sora)",
                    "lab": "Google DeepMind & OpenAI",
                    "capability": "Gemini achieves production 1M-2M token context windows; Sora introduces space-time patch diffusion for physical world simulation.",
                    "date": "Early 2024",
                    "impact": "Unlocked whole-codebase in-context ingestion and physical spatial understanding."
                }
            ]
        },
        {
            "period": "2023",
            "top3": [
                {
                    "title": "GPT-4 Release: Multimodal Frontier Landmark",
                    "lab": "OpenAI",
                    "capability": "Mixture-of-Experts architecture passing the Uniform Bar Exam in 90th percentile, establishing modern foundation model baseline.",
                    "date": "March 2023",
                    "impact": "Catalyzed global generative AI deployment and the modern enterprise LLM industry."
                },
                {
                    "title": "LLaMA Weights & Open Source Ecosystem Genesis",
                    "lab": "Meta AI",
                    "capability": "Release of efficient 7B/13B/65B foundation weights, leading to llama.cpp, quantization, and the open-source AI boom.",
                    "date": "Spring 2023",
                    "impact": "Proved that open-weights foundation models can run locally on consumer hardware (MacBooks, PCs)."
                },
                {
                    "title": "Direct Preference Optimization (DPO) & RLHF Modernization",
                    "lab": "Stanford University",
                    "capability": "Eliminated the need for separate reward model training by directly optimizing policies via implicit reward formulation.",
                    "date": "Summer 2023",
                    "impact": "Simplified post-training alignment across virtually every open and proprietary model lab."
                }
            ]
        }
    ],
    "half_yearly": [
        {
            "period": "2026 H1",
            "top3": [
                { "title": "Claude 3.7 Sonnet Dynamic Extended Thinking", "lab": "Anthropic", "capability": "Hybrid deliberate reasoning budget in production APIs.", "date": "Feb 2026" },
                { "title": "DeepSeek-R1 Open MoE 671B Weights Release", "lab": "DeepSeek", "capability": "Open reasoning parity with closed US models.", "date": "Jan 2026" },
                { "title": "Gemini 3.8 Flash 1M Multimodal Reasoning", "lab": "Google DeepMind", "capability": "Ultra-low latency audio/video reasoning at commodity pricing.", "date": "March 2026" }
            ]
        },
        {
            "period": "2025 H2",
            "top3": [
                { "title": "OpenAI o3 & o3-mini Reasoning Model Frontier", "lab": "OpenAI", "capability": "Competitive programming gold medal math performance.", "date": "Dec 2025" },
                { "title": "DeepSeek-V3 671B DualPipe Architecture", "lab": "DeepSeek", "capability": "Multi-Head Latent Attention enabling ultra-low KV memory.", "date": "Dec 2025" },
                { "title": "Llama 3.3 70B Instruct Single-Node SOTA", "lab": "Meta AI", "capability": "405B capabilities packed into single workstation inference.", "date": "Dec 2025" }
            ]
        },
        {
            "period": "2025 H1",
            "top3": [
                { "title": "OpenAI o1 Reasoning Previews", "lab": "OpenAI", "capability": "Inaugurated the test-time compute scaling paradigm.", "date": "Sept 2024 - Jan 2025" },
                { "title": "Qwen 2.5 Coder 32B Open Champion", "lab": "Alibaba", "capability": "SOTA open coding model surpassing closed predecessors.", "date": "Nov 2024" },
                { "title": "DeepSeek-V2 MoE Low-Cost Benchmark", "lab": "DeepSeek", "capability": "Pioneered extreme price reductions for cloud API inference.", "date": "May 2025" }
            ]
        },
        {
            "period": "2024 H2",
            "top3": [
                { "title": "Anthropic Computer Use API", "lab": "Anthropic", "capability": "Models directly control keyboards, mice, and GUI applications.", "date": "Oct 2024" },
                { "title": "Llama 3.1 405B Frontier Open Release", "lab": "Meta AI", "capability": "First open model matching contemporary proprietary frontier.", "date": "July 2024" },
                { "title": "FLUX.1 Open Source Image Diffusion", "lab": "Black Forest Labs", "capability": "Rectified flow transformer producing hyper-photorealistic imagery.", "date": "Aug 2024" }
            ]
        },
        {
            "period": "2024 H1",
            "top3": [
                { "title": "AlphaFold 3 Biomolecular Structure", "lab": "Google DeepMind", "capability": "Unified prediction of all life molecules (proteins, DNA, RNA).", "date": "May 2024" },
                { "title": "Claude 3.5 Sonnet & Artifacts Launch", "lab": "Anthropic", "capability": "Revolutionized coding, SWE-bench and interactive development.", "date": "June 2024" },
                { "title": "Gemini 1.5 Pro Million-Token Context", "lab": "Google DeepMind", "capability": "First production architecture processing 1M tokens effortlessly.", "date": "Feb 2024" }
            ]
        }
    ],
    "quarterly": [
        {
            "period": "2026 Q1",
            "top3": [
                { "title": "Claude 3.7 Sonnet (Hybrid Thinking)", "lab": "Anthropic", "capability": "Developer-tunable thinking tokens.", "date": "Feb 2026" },
                { "title": "DeepSeek-R1 Open MoE Launch", "lab": "DeepSeek", "capability": "Open weights reasoning at $0.55/1M.", "date": "Jan 2026" },
                { "title": "Gemini 3.8 Flash Multimodal Agent", "lab": "Google DeepMind", "capability": "1M context high-speed reasoning.", "date": "March 2026" }
            ]
        },
        {
            "period": "2025 Q4",
            "top3": [
                { "title": "OpenAI o3 Frontier Launch", "lab": "OpenAI", "capability": "Test-time compute breakthrough on hard reasoning.", "date": "Dec 2025" },
                { "title": "DeepSeek-V3 671B MoE", "lab": "DeepSeek", "capability": "SOTA architecture trained on low budget.", "date": "Dec 2025" },
                { "title": "Llama 3.3 70B Release", "lab": "Meta AI", "capability": "Workstation single-node frontier model.", "date": "Dec 2025" }
            ]
        },
        {
            "period": "2025 Q3",
            "top3": [
                { "title": "OpenAI o1 Reasoning Launch", "lab": "OpenAI", "capability": "First public test-time compute scaling model.", "date": "Sept 2024" },
                { "title": "Qwen 2.5 Coding Ecosystem", "lab": "Alibaba", "capability": "Apache 2.0 weights dominating local coding.", "date": "Sept 2025" },
                { "title": "Mistral Large 2 (123B)", "lab": "Mistral AI", "capability": "Multilingual open weights frontier.", "date": "July 2025" }
            ]
        },
        {
            "period": "2024 Q4",
            "top3": [
                { "title": "Anthropic Computer Use", "lab": "Anthropic", "capability": "Direct desktop and terminal agentic control.", "date": "Oct 2024" },
                { "title": "Llama 3.2 Multimodal Vision", "lab": "Meta AI", "capability": "Edge and vision open weights models.", "date": "Sept 2024" },
                { "title": "FLUX.1 Schnell & Dev Models", "lab": "Black Forest Labs", "capability": "Open image generation dominance.", "date": "Aug 2024" }
            ]
        },
        {
            "period": "2024 Q2",
            "top3": [
                { "title": "AlphaFold 3 Breakthrough", "lab": "Google DeepMind", "capability": "Comprehensive biomolecular modeling.", "date": "May 2024" },
                { "title": "Claude 3.5 Sonnet Release", "lab": "Anthropic", "capability": "SOTA coding assistant revolution.", "date": "June 2024" },
                { "title": "Llama 3 8B & 70B Release", "lab": "Meta AI", "capability": "New generation open source baseline.", "date": "April 2024" }
            ]
        }
    ],
    "monthly": [
        { "period": "2026-03", "top3": [
            { "title": "Gemini 3.8 Flash General Availability", "lab": "Google DeepMind", "capability": "Sub-200ms 1M context multimodal reasoning.", "date": "2026-03-01" },
            { "title": "Gemma 4 31B Open Weights", "lab": "Google DeepMind", "capability": "Dense open-weights model matching proprietary 70B.", "date": "2026-03-03" },
            { "title": "Qwen 3.8 27B Workstation Optimization", "lab": "Alibaba", "capability": "Ternary base-3 packing reducing VRAM by 22%.", "date": "2026-03-05" }
        ]},
        { "period": "2026-02", "top3": [
            { "title": "Claude 3.7 Sonnet Hybrid Extended Thinking", "lab": "Anthropic", "capability": "Continuous reasoning dial from 0 to 64K tokens.", "date": "2026-02-24" },
            { "title": "Grok 3 Colossus Supercluster Launch", "lab": "xAI", "capability": "100K H100/H200 cluster trained frontier model.", "date": "2026-02-17" },
            { "title": "Veo 3.1 Fast Video Generation", "lab": "Google DeepMind", "capability": "Instant 1080p generative video for creator pipelines.", "date": "2026-02-10" }
        ]},
        { "period": "2026-01", "top3": [
            { "title": "DeepSeek-R1 Open Reasoning Release", "lab": "DeepSeek AI", "capability": "Pure RL reasoning model with MIT weights.", "date": "2026-01-20" },
            { "title": "Codestral 2501 Specialized Coding", "lab": "Mistral AI", "capability": "Fill-in-the-middle code completion benchmark leader.", "date": "2026-01-14" },
            { "title": "Deep Research Max Autonomous Research", "lab": "Google DeepMind", "capability": "Multi-hour web & paper exploration agent.", "date": "2026-01-08" }
        ]},
        { "period": "2025-12", "top3": [
            { "title": "OpenAI o3 High-Effort Reasoning", "lab": "OpenAI", "capability": "SOTA competitive programming performance.", "date": "2025-12-20" },
            { "title": "DeepSeek-V3 671B MoE Release", "lab": "DeepSeek AI", "capability": "Groundbreaking FP8 training & MLA architecture.", "date": "2025-12-26" },
            { "title": "Llama 3.3 70B Instruct Release", "lab": "Meta AI", "capability": "405B capabilities on a single node.", "date": "2025-12-06" }
        ]},
        { "period": "2025-11", "top3": [
            { "title": "Qwen 2.5 Coder 32B Open Release", "lab": "Alibaba", "capability": "Ecosystem default open coding model.", "date": "2025-11-12" },
            { "title": "Claude 3.5 Haiku Low-Latency API", "lab": "Anthropic", "capability": "Fastest coding & categorization model.", "date": "2025-11-04" },
            { "title": "Pixtral Large 124B Multimodal", "lab": "Mistral AI", "capability": "High-resolution multimodal document parsing.", "date": "2025-11-18" }
        ]},
        { "period": "2025-10", "top3": [
            { "title": "Anthropic Computer Use API Public Beta", "lab": "Anthropic", "capability": "Direct desktop interaction & agentic control.", "date": "2025-10-22" },
            { "title": "Gemini 2.5 Flash Native Audio Streaming", "lab": "Google DeepMind", "capability": "Real-time bidirectional speech with voice VAD.", "date": "2025-10-15" },
            { "title": "Llama 3.2 Vision 11B & 90B", "lab": "Meta AI", "capability": "Open multimodal edge models.", "date": "2025-10-01" }
        ]}
    ],
    "weekly": [
        {
            "period": "Current Week (Sept 2026)",
            "top3": [
                { "title": "Scal3R Online Multi-View 3D Reconstruction", "lab": "Hugging Face / Research", "capability": "Multi-relative pose query enabling zero-shot 3D spatial reconstruction.", "date": "2026-09-05" },
                { "title": "RoboTok Internet-Scale Dexterous Manipulation", "lab": "Robotics Consortium", "capability": "Unified tokenized data engine for human demonstration retrieval and robotic manipulation.", "date": "2026-09-05" },
                { "title": "Base-3 Ternary GGUF Packing (-22% VRAM)", "lab": "LocalLLaMA / Open Source", "capability": "Lossless ternary quantization running 27B models on 12GB VRAM.", "date": "2026-09-05" }
            ]
        },
        {
            "period": "Last Week (Late Aug 2026)",
            "top3": [
                { "title": "Gemini 3.8 Flash High-Speed Reasoning Dial", "lab": "Google DeepMind", "capability": "Dynamic thinking effort parameter across Gemini API.", "date": "2026-08-28" },
                { "title": "Claude Code Auto Mode Sandbox Auditing", "lab": "Simon Willison / Dev Community", "capability": "Zero-intervention terminal agent security boundaries.", "date": "2026-08-27" },
                { "title": "vLLM Chunked Prefill Memory Optimization", "lab": "vLLM Project", "capability": "50% reduction in KV cache allocation spikes under concurrency.", "date": "2026-08-25" }
            ]
        }
    ]
}

# Frontier Model Master Database (All Labs, updated 2025/2026 with pricing, context, capabilities)
FRONTIER_MODELS = [
    # Google DeepMind
    {
        "id": "gemini-3-8-flash",
        "name": "Gemini 3.8 Flash",
        "lab": "Google DeepMind",
        "lab_slug": "google",
        "year": "2026",
        "license": "Proprietary API",
        "context_window": "1,000,000 tokens",
        "max_output": "65,536 tokens",
        "pricing_input": "$0.10 / 1M",
        "pricing_output": "$0.40 / 1M",
        "pricing_cached": "$0.025 / 1M",
        "architecture": "High-Efficiency Multimodal MoE",
        "readiness": "Frontier SOTA",
        "tag": "AGENTIC REASONING",
        "capabilities": ["Dynamic Extended Thinking", "Multimodal Video/Audio", "1M Context", "Function Calling", "JSON Mode", "Live Audio Streaming"],
        "best_for": "Fast autonomous agents, full-codebase context, multimodal audio/video analysis at high throughput.",
        "api_snippet": "from google import genai\nclient = genai.Client()\nresponse = client.models.generate_content(\n    model='gemini-3.8-flash',\n    contents='Analyze this entire codebase'\n)"
    },
    {
        "id": "gemini-3-1-pro",
        "name": "Gemini 3.1 Pro",
        "lab": "Google DeepMind",
        "lab_slug": "google",
        "year": "2026",
        "license": "Proprietary API",
        "context_window": "2,000,000 tokens",
        "max_output": "65,536 tokens",
        "pricing_input": "$1.25 / 1M",
        "pricing_output": "$5.00 / 1M",
        "pricing_cached": "$0.31 / 1M",
        "architecture": "Deep Frontier Multimodal",
        "readiness": "Flagship Pro",
        "tag": "MASSIVE CONTEXT",
        "capabilities": ["2M Token Ingestion", "Deep Reasoning", "Complex Code Generation", "Multimodal Vision & Video", "High Precision Math"],
        "best_for": "Exhaustive legal & scientific document synthesis, hours of high-res video parsing, complex system architecture.",
        "api_snippet": "response = client.models.generate_content(\n    model='gemini-3.1-pro',\n    contents=[large_video_file, 'Summarize all key events']\n)"
    },
    {
        "id": "gemini-2-5-computer-use",
        "name": "Gemini 2.5 Computer Use",
        "lab": "Google DeepMind",
        "lab_slug": "google",
        "year": "2026",
        "license": "Proprietary API",
        "context_window": "131,072 tokens",
        "max_output": "65,536 tokens",
        "pricing_input": "$0.80 / 1M",
        "pricing_output": "$3.20 / 1M",
        "pricing_cached": "$0.20 / 1M",
        "architecture": "Visual Agentic Action Model",
        "readiness": "Production Ready",
        "tag": "OS AUTOMATION",
        "capabilities": ["Direct Desktop Mouse/Key", "Browser Automation", "Screenshot Grounding", "Multi-Step Action Execution"],
        "best_for": "Automating legacy desktop software, end-to-end web browser testing, RPA workflows.",
        "api_snippet": "# Direct OS Agent API\nresponse = client.models.generate_content(\n    model='gemini-2.5-computer-use-preview',\n    contents=['Fill the invoice spreadsheet in LibreOffice']\n)"
    },
    {
        "id": "gemma-4-31b",
        "name": "Gemma 4 31B",
        "lab": "Google DeepMind",
        "lab_slug": "google",
        "year": "2026",
        "license": "Open Weights (Gemma)",
        "context_window": "128,000 tokens",
        "max_output": "16,384 tokens",
        "pricing_input": "Free / Self-Hosted",
        "pricing_output": "Free / Self-Hosted",
        "pricing_cached": "N/A",
        "architecture": "Dense 31B Parameter",
        "readiness": "Open Weights",
        "tag": "LOCAL ENTERPRISE",
        "capabilities": ["Local Workstation Run", "Instruction Tuned", "Ollama Native", "Full Privacy", "Commercial Friendly"],
        "best_for": "Air-gapped enterprise deployments, private document classification, local workstation coding.",
        "api_snippet": "# CLI Command\nollama run gemma4:31b"
    },

    # OpenAI
    {
        "id": "openai-o3",
        "name": "OpenAI o3",
        "lab": "OpenAI",
        "lab_slug": "openai",
        "year": "2025",
        "license": "Proprietary API",
        "context_window": "200,000 tokens",
        "max_output": "100,000 tokens",
        "pricing_input": "$15.00 / 1M",
        "pricing_output": "$60.00 / 1M",
        "pricing_cached": "$3.75 / 1M",
        "architecture": "Test-Time Compute Scaling",
        "readiness": "Frontier SOTA",
        "tag": "DEEP REASONING",
        "capabilities": ["Deliberate Internal Thought", "Competitive Programming Gold", "PhD Level Science", "Codeforces Master"],
        "best_for": "Complex mathematical theorem proofs, hard algorithmic optimization, critical security auditing.",
        "api_snippet": "from openai import OpenAI\nclient = OpenAI()\nresp = client.chat.completions.create(\n    model='o3',\n    messages=[{'role': 'user', 'content': 'Prove the conjecture'}]\n)"
    },
    {
        "id": "openai-o3-mini",
        "name": "OpenAI o3-mini",
        "lab": "OpenAI",
        "lab_slug": "openai",
        "year": "2025",
        "license": "Proprietary API",
        "context_window": "200,000 tokens",
        "max_output": "100,000 tokens",
        "pricing_input": "$1.10 / 1M",
        "pricing_output": "$4.40 / 1M",
        "pricing_cached": "$0.55 / 1M",
        "architecture": "Efficient Reasoning Model",
        "readiness": "Cost Leader",
        "tag": "FAST REASONING",
        "capabilities": ["Configurable Thinking Budget (low/med/high)", "Fast Coding", "Function Calling with Thought", "Math SOTA"],
        "best_for": "Production code evaluation, automated debugging pipelines, real-time math tutor.",
        "api_snippet": "resp = client.chat.completions.create(\n    model='o3-mini',\n    reasoning_effort='medium',\n    messages=[{'role': 'user', 'content': 'Refactor this algorithm'}]\n)"
    },
    {
        "id": "gpt-4-5",
        "name": "GPT-4.5 (Orion)",
        "lab": "OpenAI",
        "lab_slug": "openai",
        "year": "2025",
        "license": "Proprietary API",
        "context_window": "128,000 tokens",
        "max_output": "16,384 tokens",
        "pricing_input": "$75.00 / 1M",
        "pricing_output": "$150.00 / 1M",
        "pricing_cached": "$37.50 / 1M",
        "architecture": "Massive Dense Flagship",
        "readiness": "Flagship Pro",
        "tag": "WORLD KNOWLEDGE",
        "capabilities": ["Nuanced Writing", "Broad World Knowledge", "Emotional Intelligence", "Multimodal Vision"],
        "best_for": "Executive strategy briefs, high-touch customer consultation, nuanced literary translation.",
        "api_snippet": "resp = client.chat.completions.create(\n    model='gpt-4.5-preview',\n    messages=[{'role': 'user', 'content': 'Draft executive market analysis'}]\n)"
    },

    # Anthropic
    {
        "id": "claude-3-7-sonnet",
        "name": "Claude 3.7 Sonnet",
        "lab": "Anthropic",
        "lab_slug": "anthropic",
        "year": "2026",
        "license": "Proprietary API",
        "context_window": "200,000 tokens",
        "max_output": "64,000 tokens",
        "pricing_input": "$3.00 / 1M",
        "pricing_output": "$15.00 / 1M",
        "pricing_cached": "$0.30 / 1M",
        "architecture": "Hybrid Extended Thinking Dense",
        "readiness": "Frontier SOTA",
        "tag": "HYBRID REASONING",
        "capabilities": ["Dynamic Thinking Budget (0-64K)", "SWE-bench Verified Leader", "Agentic Terminal Tool Use", "Computer Control"],
        "best_for": "Autonomous coding agents (Claude Code, Cursor), whole-repository refactoring, difficult debugging.",
        "api_snippet": "import anthropic\nclient = anthropic.Anthropic()\nresp = client.messages.create(\n    model='claude-3-7-sonnet-20260219',\n    max_tokens=64000,\n    thinking={'type': 'enabled', 'budget_tokens': 16000},\n    messages=[{'role': 'user', 'content': 'Write full compiler test suite'}]\n)"
    },
    {
        "id": "claude-opus-5",
        "name": "Claude Opus 5 (Auto Mode)",
        "lab": "Anthropic",
        "lab_slug": "anthropic",
        "year": "2026",
        "license": "Proprietary API",
        "context_window": "200,000 tokens",
        "max_output": "64,000 tokens",
        "pricing_input": "$15.00 / 1M",
        "pricing_output": "$75.00 / 1M",
        "pricing_cached": "$1.50 / 1M",
        "architecture": "Massive Long-Horizon Flagship",
        "readiness": "Flagship Pro",
        "tag": "AUTONOMOUS AGENT",
        "capabilities": ["Multi-Hour Task Execution", "Repository Architecture Migration", "Deep Formal Verification"],
        "best_for": "Fully autonomous multi-file refactoring, enterprise security auditing, legacy codebase migrations.",
        "api_snippet": "# Claude Opus 5 with Autonomous Execution\nresp = client.messages.create(\n    model='claude-opus-5',\n    max_tokens=64000,\n    messages=[{'role': 'user', 'content': 'Migrate our monolith to microservices'}]\n)"
    },
    {
        "id": "claude-3-5-haiku",
        "name": "Claude 3.5 Haiku",
        "lab": "Anthropic",
        "lab_slug": "anthropic",
        "year": "2025",
        "license": "Proprietary API",
        "context_window": "200,000 tokens",
        "max_output": "8,192 tokens",
        "pricing_input": "$0.80 / 1M",
        "pricing_output": "$4.00 / 1M",
        "pricing_cached": "$0.08 / 1M",
        "architecture": "Low-Latency Dense",
        "readiness": "Cost Leader",
        "tag": "FAST INFERENCE",
        "capabilities": ["Sub-150ms First Token", "Structured Extraction", "High-Volume Filtering", "High Accuracy Tool Use"],
        "best_for": "High-concurrency API backends, real-time code completions, user request routing.",
        "api_snippet": "resp = client.messages.create(\n    model='claude-3-5-haiku-20241022',\n    max_tokens=2048,\n    messages=[{'role': 'user', 'content': 'Classify this intent'}]\n)"
    },

    # DeepSeek
    {
        "id": "deepseek-r1",
        "name": "DeepSeek-R1",
        "lab": "DeepSeek AI",
        "lab_slug": "deepseek",
        "year": "2026",
        "license": "Open Weights (MIT)",
        "context_window": "128,000 tokens",
        "max_output": "64,000 tokens",
        "pricing_input": "$0.55 / 1M",
        "pricing_output": "$2.19 / 1M",
        "pricing_cached": "$0.14 / 1M",
        "architecture": "671B MoE (37B active)",
        "readiness": "Open Weights",
        "tag": "OPEN REASONING",
        "capabilities": ["Pure RL Chain-of-Thought", "MIT Open License", "AIME 79.8% SOTA", "MATH-500 97.3%"],
        "best_for": "Self-hosted high-reasoning, low-cost enterprise analytics, uncensored algorithmic research.",
        "api_snippet": "# Ollama Self-Hosted Run\nollama run deepseek-r1:671b\n\n# Or DeepSeek API\nclient = OpenAI(api_key='...', base_url='https://api.deepseek.com')\nresp = client.chat.completions.create(model='deepseek-reasoner', messages=[...])"
    },
    {
        "id": "deepseek-v3",
        "name": "DeepSeek-V3",
        "lab": "DeepSeek AI",
        "lab_slug": "deepseek",
        "year": "2025",
        "license": "Open Weights (MIT)",
        "context_window": "128,000 tokens",
        "max_output": "8,192 tokens",
        "pricing_input": "$0.14 / 1M",
        "pricing_output": "$0.28 / 1M",
        "pricing_cached": "$0.014 / 1M",
        "architecture": "671B MoE (Multi-Head Latent Attention)",
        "readiness": "Cost Leader",
        "tag": "ULTRA LOW COST",
        "capabilities": ["Multi-Head Latent Attention (MLA)", "FP8 Mixed Precision Native", "60 TPS Throughput"],
        "best_for": "Massive document indexing, cost-critical summarization, batch ETL transformation.",
        "api_snippet": "# Run via vLLM\nvllm serve deepseek-ai/DeepSeek-V3 --trust-remote-code"
    },
    {
        "id": "deepseek-r1-distill-32b",
        "name": "DeepSeek-R1-Distill-32B",
        "lab": "DeepSeek AI",
        "lab_slug": "deepseek",
        "year": "2026",
        "license": "Open Weights (MIT)",
        "context_window": "128,000 tokens",
        "max_output": "16,384 tokens",
        "pricing_input": "Free / Self-Hosted",
        "pricing_output": "Free / Self-Hosted",
        "pricing_cached": "N/A",
        "architecture": "Dense 32B Distilled",
        "readiness": "Open Weights",
        "tag": "LOCAL SOTA",
        "capabilities": ["Single RTX 4090 / 5090 Run", "o1-mini Grade Math", "Qwen Base Distillation"],
        "best_for": "Running local reasoning on gaming workstations or single cloud instances.",
        "api_snippet": "# Run locally in terminal\nollama run deepseek-r1:32b"
    },

    # Meta AI
    {
        "id": "llama-4-behemoth",
        "name": "Llama 4",
        "lab": "Meta AI",
        "lab_slug": "meta",
        "year": "2026",
        "license": "Open Weights (Llama Community)",
        "context_window": "128,000 tokens",
        "max_output": "16,384 tokens",
        "pricing_input": "Free / Self-Hosted",
        "pricing_output": "Free / Self-Hosted",
        "pricing_cached": "N/A",
        "architecture": "Multimodal Frontier MoE",
        "readiness": "Frontier SOTA",
        "tag": "OPEN FOUNDATION",
        "capabilities": ["Native Agentic Tool Use", "Multimodal Vision & Audio", "Self-Hosted Enterprise Support"],
        "best_for": "Enterprise foundation fine-tuning, private on-premise cloud infrastructure.",
        "api_snippet": "vllm serve meta-llama/Llama-4 --tensor-parallel-size 4"
    },
    {
        "id": "llama-3-3-70b",
        "name": "Llama 3.3 70B Instruct",
        "lab": "Meta AI",
        "lab_slug": "meta",
        "year": "2025",
        "license": "Open Weights (Llama Community)",
        "context_window": "128,000 tokens",
        "max_output": "8,192 tokens",
        "pricing_input": "Free / Self-Hosted",
        "pricing_output": "Free / Self-Hosted",
        "pricing_cached": "N/A",
        "architecture": "Dense 70B Parameter",
        "readiness": "Production Ready",
        "tag": "WORKSTATION WORKHORSE",
        "capabilities": ["405B Performance on 70B VRAM", "Multilingual 8+ Languages", "High Coding Accuracy"],
        "best_for": "Standard enterprise private deployments on dual RTX 4090 or single A100/H100.",
        "api_snippet": "ollama run llama3.3:70b"
    },

    # xAI
    {
        "id": "grok-3",
        "name": "Grok 3 (Colossus)",
        "lab": "xAI",
        "lab_slug": "xai",
        "year": "2025",
        "license": "Proprietary API",
        "context_window": "256,000 tokens",
        "max_output": "32,768 tokens",
        "pricing_input": "$5.00 / 1M",
        "pricing_output": "$15.00 / 1M",
        "pricing_cached": "$1.25 / 1M",
        "architecture": "Mega-Scale Dense (Colossus Cluster)",
        "readiness": "Frontier SOTA",
        "tag": "REAL-TIME WORLD KNOWLEDGE",
        "capabilities": ["Colossus Supercluster Trained", "Real-Time World Knowledge", "High Raw Coding Throughput"],
        "best_for": "Real-time market intelligence, rapid code synthesis, uncensored open exploration.",
        "api_snippet": "# xAI API Call\nclient = OpenAI(api_key='...', base_url='https://api.x.ai/v1')\nresp = client.chat.completions.create(model='grok-3', messages=[...])"
    },
    {
        "id": "grok-3-think",
        "name": "Grok 3 Think",
        "lab": "xAI",
        "lab_slug": "xai",
        "year": "2025",
        "license": "Proprietary API",
        "context_window": "256,000 tokens",
        "max_output": "32,768 tokens",
        "pricing_input": "$8.00 / 1M",
        "pricing_output": "$24.00 / 1M",
        "pricing_cached": "$2.00 / 1M",
        "architecture": "Deliberation Reasoning Engine",
        "readiness": "Frontier SOTA",
        "tag": "DEEP DELIBERATION",
        "capabilities": ["Extended Reasoning Steps", "Formal Logic Verification", "Mathematical Proof Construction"],
        "best_for": "Hard scientific verification, algorithmic dispute resolution, complex software debugging.",
        "api_snippet": "resp = client.chat.completions.create(model='grok-3-think', messages=[...])"
    },

    # Alibaba (Qwen)
    {
        "id": "qwen-3-8-27b",
        "name": "Qwen 3.8 27B",
        "lab": "Alibaba",
        "lab_slug": "alibaba",
        "year": "2026",
        "license": "Open Weights (Apache 2.0)",
        "context_window": "128,000 tokens",
        "max_output": "16,384 tokens",
        "pricing_input": "Free / Self-Hosted",
        "pricing_output": "Free / Self-Hosted",
        "pricing_cached": "N/A",
        "architecture": "Dense 27B Workstation Optimized",
        "readiness": "Open Weights",
        "tag": "COMPACT WORKSTATION",
        "capabilities": ["Ternary Base-3 Packing (-22% VRAM)", "Strix / Mac Silicon Native", "High Efficiency Inference"],
        "best_for": "Developers running local models on laptops (M3/M4 or AMD Strix) without GPU fan noise.",
        "api_snippet": "ollama run qwen3.8:27b"
    },
    {
        "id": "qwen-2-5-coder-32b",
        "name": "Qwen 2.5 Coder 32B",
        "lab": "Alibaba",
        "lab_slug": "alibaba",
        "year": "2025",
        "license": "Open Weights (Apache 2.0)",
        "context_window": "128,000 tokens",
        "max_output": "16,384 tokens",
        "pricing_input": "Free / Self-Hosted",
        "pricing_output": "Free / Self-Hosted",
        "pricing_cached": "N/A",
        "architecture": "Dense 32B Parameter",
        "readiness": "Benchmark Winner",
        "tag": "OPEN SOTA CODING",
        "capabilities": ["HumanEval 92.7%", "LiveCodeBench Leader", "Apache 2.0 Permissive", "Fill-in-the-Middle"],
        "best_for": "Standard local backend for Continue.dev, Cline, and private enterprise code generation.",
        "api_snippet": "ollama run qwen2.5-coder:32b"
    },

    # Mistral AI
    {
        "id": "mistral-large-2",
        "name": "Mistral Large 2 (123B)",
        "lab": "Mistral AI",
        "lab_slug": "mistral",
        "year": "2025",
        "license": "Mistral Research / API",
        "context_window": "128,000 tokens",
        "max_output": "16,384 tokens",
        "pricing_input": "$2.00 / 1M",
        "pricing_output": "$6.00 / 1M",
        "pricing_cached": "$0.50 / 1M",
        "architecture": "123B Dense Multilingual",
        "readiness": "Production Ready",
        "tag": "EUROPEAN ENTERPRISE",
        "capabilities": ["80+ Programming Languages", "GDPR Native Compliance", "Function Calling SOTA", "Strong Multilingual"],
        "best_for": "European enterprise compliance, high-precision code translation, polyglot software stacks.",
        "api_snippet": "from mistralai import Mistral\nclient = Mistral(api_key='...')\nresp = client.chat.complete(model='mistral-large-latest', messages=[...])"
    },
    {
        "id": "codestral-2501",
        "name": "Codestral 2501 (22B)",
        "lab": "Mistral AI",
        "lab_slug": "mistral",
        "year": "2025",
        "license": "Mistral Non-Production / Commercial API",
        "context_window": "256,000 tokens",
        "max_output": "8,192 tokens",
        "pricing_input": "$0.30 / 1M",
        "pricing_output": "$0.90 / 1M",
        "pricing_cached": "$0.075 / 1M",
        "architecture": "Dense 22B Coding Specialist",
        "readiness": "Cost Leader",
        "tag": "SPECIALIZED CODE",
        "capabilities": ["256K Context Code Ingestion", "Ultra Fast FIM (Fill-in-the-Middle)", "80+ Languages"],
        "best_for": "IDE tab completions, instant code formatting, function refactoring at microsecond latency.",
        "api_snippet": "ollama run codestral"
    }
]

models_json_str = json.dumps(FRONTIER_MODELS)
milestones_json_str = json.dumps(MILESTONES_ARCHIVE)

print("[build_webapp] Loaded models and milestone databases.")
print(f"[build_webapp] Total Frontier Models: {len(FRONTIER_MODELS)}")
print(f"[build_webapp] Compiling Spotify-inspired HTML application...")

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>AI Pulse — Frontier AI &amp; Developer Intelligence</title>
    <meta name="description" content="Spotify-inspired developer intelligence dashboard tracking frontier models, daily breakthroughs, and landmark milestones.">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    
    <!-- Supabase JS Client -->
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

    <style>
        :root {{
            --bg-base: #121212;
            --bg-surface: #181818;
            --bg-card: #181818;
            --bg-card-hover: #242424;
            --bg-elevated: #282828;
            --border-subtle: #282828;
            --border-highlight: #3e3e3e;
            --accent-green: #1ed760;
            --accent-green-hover: #1fdf64;
            --accent-green-dark: #1db954;
            --accent-beige: #e5dcd0;
            --text-primary: #ffffff;
            --text-secondary: #a7a7a7;
            --text-muted: #727272;
            --badge-bg: #242424;
            --badge-text: #ffffff;
            --radius-sm: 4px;
            --radius-md: 8px;
            --radius-lg: 12px;
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

        body {{
            background-color: var(--bg-base);
            color: var(--text-primary);
            font-family: var(--font-sans);
            min-height: 100vh;
            line-height: 1.5;
            overflow-x: hidden;
        }}

        /* Header */
        header {{
            position: sticky;
            top: 0;
            z-index: 60;
            background: rgba(18, 18, 18, 0.94);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-subtle);
            padding: 14px 24px;
        }}

        .header-inner {{
            max-width: 1240px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            text-decoration: none;
        }}

        .brand-dot {{
            width: 10px;
            height: 10px;
            background-color: var(--accent-green);
            border-radius: 50%;
            box-shadow: 0 0 10px rgba(30, 215, 96, 0.5);
        }}

        .brand-title {{
            font-size: 18px;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }}

        .brand-subtitle {{
            font-size: 11px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 600;
            margin-left: 4px;
        }}

        nav.nav-links {{
            display: flex;
            align-items: center;
            gap: 8px;
            overflow-x: auto;
            padding: 2px 0;
        }}

        .nav-btn {{
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-family: var(--font-sans);
            font-size: 13px;
            font-weight: 700;
            padding: 8px 18px;
            border-radius: var(--radius-pill);
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
        }}

        .nav-btn:hover {{
            color: var(--text-primary);
            background: var(--bg-card-hover);
        }}

        .nav-btn.active {{
            background: var(--text-primary);
            color: #000000;
        }}

        .header-status {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 600;
        }}

        /* Container */
        .app-container {{
            max-width: 1240px;
            margin: 0 auto;
            padding: 28px 24px 80px 24px;
        }}

        /* Section Layouts */
        .section-header {{
            margin-bottom: 24px;
        }}

        .section-title {{
            font-size: 26px;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 6px;
            color: var(--text-primary);
        }}

        .section-desc {{
            font-size: 14px;
            color: var(--text-secondary);
        }}

        /* Executive Highlights */
        .highlights-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 22px 26px;
            margin-bottom: 30px;
            border-left: 4px solid var(--accent-green);
        }}

        .highlights-title {{
            font-size: 13px;
            font-weight: 800;
            color: var(--accent-green);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .highlights-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .highlights-list li {{
            font-size: 14px;
            line-height: 1.6;
            color: #d1d5db;
            position: relative;
            padding-left: 18px;
        }}

        .highlights-list li::before {{
            content: '•';
            color: var(--accent-green);
            position: absolute;
            left: 0;
            font-weight: 800;
            font-size: 18px;
            line-height: 1;
        }}

        .highlights-list strong {{
            color: var(--text-primary);
        }}

        /* Calendar Picker */
        .calendar-bar {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 24px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}

        .date-chip {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            font-family: var(--font-sans);
            font-size: 13px;
            font-weight: 600;
            padding: 8px 16px;
            border-radius: var(--radius-pill);
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }}

        .date-chip:hover {{
            border-color: var(--border-highlight);
            color: var(--text-primary);
            background: var(--bg-card-hover);
        }}

        .date-chip.active {{
            background: var(--accent-green);
            color: #000000;
            border-color: var(--accent-green);
            font-weight: 800;
        }}

        /* Filter & Search Bar */
        .filter-controls {{
            display: flex;
            flex-direction: column;
            gap: 14px;
            margin-bottom: 28px;
        }}

        .search-wrap {{
            position: relative;
            width: 100%;
        }}

        .search-input {{
            width: 100%;
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-primary);
            font-family: var(--font-sans);
            font-size: 14px;
            padding: 12px 18px 12px 42px;
            border-radius: var(--radius-pill);
            outline: none;
            transition: border-color 0.2s;
        }}

        .search-input:focus {{
            border-color: var(--accent-green);
            background: #1e1e1e;
        }}

        .search-input::placeholder {{
            color: var(--text-muted);
        }}

        .search-icon {{
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 14px;
            pointer-events: none;
        }}

        .tag-chips {{
            display: flex;
            align-items: center;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 2px;
        }}

        .tag-chip {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            font-size: 12px;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: var(--radius-pill);
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.15s;
        }}

        .tag-chip:hover {{
            color: var(--text-primary);
            border-color: var(--border-highlight);
        }}

        .tag-chip.active {{
            background: var(--badge-bg);
            color: var(--accent-green);
            border-color: var(--accent-green);
        }}

        /* Cards Grid */
        .articles-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }}

        @media (min-width: 840px) {{
            .articles-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        .article-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s, border-color 0.2s, background-color 0.2s;
        }}

        .article-card:hover {{
            background-color: var(--bg-card-hover);
            border-color: var(--border-highlight);
            transform: translateY(-2px);
        }}

        .card-top {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }}

        .card-meta {{
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-size: 11px;
            font-weight: 800;
            padding: 3px 9px;
            border-radius: var(--radius-pill);
            letter-spacing: 0.04em;
            text-transform: uppercase;
            background: var(--badge-bg);
            color: var(--text-primary);
            border: 1px solid var(--border-subtle);
        }}

        .badge-breakthrough {{
            background: #2b1418;
            color: #ff4d6d;
            border-color: #5c1d27;
        }}

        .badge-devtools {{
            background: #14202c;
            color: #38bdf8;
            border-color: #1e3a5f;
        }}

        .badge-local {{
            background: #291e10;
            color: #fbbf24;
            border-color: #593e18;
        }}

        .badge-prod {{
            background: #12281a;
            color: var(--accent-green);
            border-color: #1b4d2b;
        }}

        .badge-research {{
            background: #20152b;
            color: #c084fc;
            border-color: #432461;
        }}

        .article-title {{
            font-size: 18px;
            font-weight: 700;
            line-height: 1.35;
            color: var(--text-primary);
            margin-bottom: 12px;
            text-decoration: none;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .article-title:hover {{
            color: var(--accent-green);
        }}

        .article-img-wrap {{
            margin: 8px 0 16px 0;
            border-radius: var(--radius-md);
            overflow: hidden;
            border: 1px solid var(--border-subtle);
            max-height: 220px;
            background: #000000;
        }}

        .article-img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }}

        .article-summary {{
            font-size: 14px;
            line-height: 1.6;
            color: var(--text-secondary);
            margin-bottom: 16px;
        }}

        .capability-box {{
            background: #141a15;
            border: 1px solid #1b3d22;
            border-radius: var(--radius-md);
            padding: 10px 14px;
            font-size: 13px;
            line-height: 1.5;
            color: #d1fae5;
            margin-bottom: 12px;
        }}

        .capability-label {{
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--accent-green);
            margin-bottom: 3px;
        }}

        .usecase-box {{
            background: #1a1a1a;
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 10px 14px;
            font-size: 13px;
            line-height: 1.5;
            color: var(--text-secondary);
            margin-bottom: 16px;
        }}

        .usecase-label {{
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 3px;
        }}

        .card-bottom {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 14px;
            border-top: 1px solid var(--border-subtle);
            margin-top: auto;
        }}

        .source-pill {{
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 600;
        }}

        .read-btn {{
            background: var(--badge-bg);
            border: 1px solid var(--border-subtle);
            color: var(--text-primary);
            font-family: var(--font-sans);
            font-size: 12px;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: var(--radius-pill);
            text-decoration: none;
            transition: all 0.2s;
        }}

        .read-btn:hover {{
            background: var(--text-primary);
            color: #000000;
            border-color: var(--text-primary);
        }}

        /* 1-Liners Section */
        .oneliners-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 24px;
            margin-top: 36px;
        }}

        .oneliners-header {{
            font-size: 16px;
            font-weight: 800;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .oneliner-item {{
            padding: 14px 0;
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 16px;
        }}

        .oneliner-item:last-child {{
            border-bottom: none;
        }}

        .oneliner-text {{
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.5;
        }}

        .oneliner-title {{
            color: var(--text-primary);
            font-weight: 600;
            text-decoration: none;
            margin-right: 6px;
        }}

        .oneliner-title:hover {{
            color: var(--accent-green);
        }}

        /* Frontier Model Tracker Layout */
        .lab-filter-bar {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 24px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}

        .lab-chip {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            font-size: 13px;
            font-weight: 700;
            padding: 8px 18px;
            border-radius: var(--radius-pill);
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }}

        .lab-chip:hover {{
            color: var(--text-primary);
            background: var(--bg-card-hover);
        }}

        .lab-chip.active {{
            background: var(--text-primary);
            color: #000000;
            border-color: var(--text-primary);
        }}

        .models-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 16px;
        }}

        @media (min-width: 768px) {{
            .models-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        @media (min-width: 1100px) {{
            .models-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}

        .model-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 22px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            cursor: pointer;
            transition: transform 0.2s, border-color 0.2s, background-color 0.2s;
        }}

        .model-card:hover {{
            background-color: var(--bg-card-hover);
            border-color: var(--border-highlight);
            transform: translateY(-2px);
        }}

        .model-top {{
            margin-bottom: 14px;
        }}

        .model-lab-badge {{
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--accent-green);
            margin-bottom: 6px;
        }}

        .model-name {{
            font-size: 20px;
            font-weight: 800;
            letter-spacing: -0.01em;
            margin-bottom: 6px;
            color: var(--text-primary);
        }}

        .model-specs-row {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 14px;
        }}

        .spec-pill {{
            background: #242424;
            font-size: 11px;
            font-weight: 600;
            padding: 3px 9px;
            border-radius: var(--radius-pill);
            color: var(--text-secondary);
        }}

        .model-best-for {{
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.5;
            margin-bottom: 18px;
        }}

        .model-pricing-preview {{
            font-family: var(--font-mono);
            font-size: 12px;
            color: #d1d5db;
            background: #141414;
            padding: 8px 12px;
            border-radius: var(--radius-sm);
            border: 1px solid var(--border-subtle);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .inspect-action-text {{
            font-size: 12px;
            font-weight: 700;
            color: var(--accent-green);
            display: flex;
            align-items: center;
            gap: 4px;
            margin-top: 14px;
        }}

        /* Model Inspection Drawer */
        .drawer-backdrop {{
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(8px);
            z-index: 100;
            display: none;
            opacity: 0;
            transition: opacity 0.25s ease;
        }}

        .drawer-backdrop.open {{
            display: block;
            opacity: 1;
        }}

        .drawer-content {{
            position: fixed;
            top: 0;
            right: -600px;
            width: 100%;
            max-width: 560px;
            height: 100%;
            background: #181818;
            border-left: 1px solid var(--border-subtle);
            z-index: 101;
            padding: 32px 28px;
            overflow-y: auto;
            transition: right 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
            gap: 24px;
        }}

        .drawer-backdrop.open .drawer-content {{
            right: 0;
        }}

        .drawer-close-btn {{
            align-self: flex-start;
            background: #242424;
            border: none;
            color: var(--text-primary);
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.15s;
        }}

        .drawer-close-btn:hover {{
            background: #333333;
        }}

        .pricing-table {{
            width: 100%;
            background: #121212;
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            border-collapse: collapse;
            overflow: hidden;
            font-size: 13px;
        }}

        .pricing-table th, .pricing-table td {{
            padding: 10px 14px;
            text-align: left;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .pricing-table th {{
            color: var(--text-muted);
            font-weight: 700;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.05em;
        }}

        .pricing-table td {{
            color: var(--text-primary);
            font-family: var(--font-mono);
        }}

        .code-block-wrap {{
            position: relative;
            background: #000000;
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 16px;
            overflow-x: auto;
        }}

        .code-block {{
            font-family: var(--font-mono);
            font-size: 12px;
            line-height: 1.6;
            color: #d1fae5;
            white-space: pre;
        }}

        .copy-code-btn {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: #242424;
            border: 1px solid var(--border-subtle);
            color: #ffffff;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: var(--radius-pill);
            cursor: pointer;
        }}

        .copy-code-btn:hover {{
            background: var(--accent-green);
            color: #000000;
        }}

        /* Milestones Archive Layout */
        .milestone-period-bar {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 26px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}

        .period-chip {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            font-size: 13px;
            font-weight: 700;
            padding: 8px 18px;
            border-radius: var(--radius-pill);
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }}

        .period-chip:hover {{
            color: var(--text-primary);
            background: var(--bg-card-hover);
        }}

        .period-chip.active {{
            background: var(--text-primary);
            color: #000000;
            border-color: var(--text-primary);
        }}

        .milestone-group {{
            margin-bottom: 36px;
        }}

        .milestone-group-title {{
            font-size: 18px;
            font-weight: 800;
            color: var(--text-primary);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .milestone-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 20px 24px;
            margin-bottom: 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .milestone-card:hover {{
            border-color: var(--border-highlight);
            background: var(--bg-card-hover);
        }}

        .milestone-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .milestone-title {{
            font-size: 16px;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .milestone-lab {{
            font-size: 11px;
            font-weight: 800;
            color: var(--accent-green);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .milestone-cap {{
            font-size: 14px;
            color: #e5e7eb;
            line-height: 1.5;
        }}

        .milestone-impact {{
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.5;
        }}

        /* Task Recommender Layout */
        .tasks-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 16px;
        }}

        @media (min-width: 768px) {{
            .tasks-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        .task-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .task-card:hover {{
            background: var(--bg-card-hover);
            border-color: var(--border-highlight);
        }}

        .task-title {{
            font-size: 18px;
            font-weight: 800;
            margin-bottom: 8px;
            color: var(--text-primary);
        }}

        .task-recommendations {{
            margin-top: 14px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .task-rec-item {{
            background: #121212;
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 10px 14px;
            font-size: 13px;
        }}

        .task-rec-role {{
            font-size: 11px;
            font-weight: 800;
            color: var(--accent-green);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 2px;
        }}

        /* Empty State */
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: var(--text-muted);
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="header-inner">
            <a class="brand" onclick="switchTab('feed')">
                <div class="brand-dot"></div>
                <div class="brand-title">AI PULSE</div>
                <div class="brand-subtitle">Frontier Digest</div>
            </a>

            <nav class="nav-links">
                <button class="nav-btn active" id="tab-feed" onclick="switchTab('feed')">Daily Feed</button>
                <button class="nav-btn" id="tab-models" onclick="switchTab('models')">Frontier Models</button>
                <button class="nav-btn" id="tab-milestones" onclick="switchTab('milestones')">3-Yr Milestones</button>
                <button class="nav-btn" id="tab-tasks" onclick="switchTab('tasks')">Task Guide</button>
            </nav>

            <div class="header-status">
                <span id="header-sync-status">Live</span>
            </div>
        </div>
    </header>

    <div class="app-container">

        <!-- ==================== SECTION 1: DAILY FEED ==================== -->
        <section id="view-feed">
            <div class="section-header">
                <h1 class="section-title">Developer &amp; Applied AI Intelligence</h1>
                <p class="section-desc">Strictly verified breakthroughs, practical software tooling, and high-impact research from the last 24 hours.</p>
            </div>

            <!-- Executive Highlights -->
            <div class="highlights-card" id="highlights-container">
                <div class="highlights-title">⚡ Executive Highlights (Last 24 Hours)</div>
                <ul class="highlights-list" id="highlights-list">
                    <li><strong>Breakthroughs in Physical &amp; Medical AI:</strong> Multi-view online 3D reconstruction and internet-scale dexterous robotics demonstration retrieval lead the day's applied breakthroughs.</li>
                    <li><strong>Developer Tooling &amp; Agent Security:</strong> Investigations into autonomous terminal coding agents demonstrate increased reliance on zero-intervention sandboxing boundaries.</li>
                    <li><strong>Workstation Inference:</strong> Base-3 ternary quantization brings 27B parameter frontier open models to 12GB VRAM footprints on consumer hardware.</li>
                </ul>
            </div>

            <!-- Calendar Bar -->
            <div class="calendar-bar" id="calendar-bar">
                <!-- Dynamically injected past 7 days -->
            </div>

            <!-- Filter Controls -->
            <div class="filter-controls">
                <div class="search-wrap">
                    <span class="search-icon">🔍</span>
                    <input type="text" class="search-input" id="search-input" placeholder="Search stories, models, breakthroughs, or topics..." oninput="filterArticles()">
                </div>
                <div class="tag-chips" id="tag-chips">
                    <button class="tag-chip active" onclick="setTopicFilter('all')">All Stories</button>
                    <button class="tag-chip" onclick="setTopicFilter('#FrontierModels')">#FrontierModels</button>
                    <button class="tag-chip" onclick="setTopicFilter('#Reasoning')">#Reasoning</button>
                    <button class="tag-chip" onclick="setTopicFilter('#AgenticCoding')">#AgenticCoding</button>
                    <button class="tag-chip" onclick="setTopicFilter('#LocalLLM')">#LocalLLM</button>
                    <button class="tag-chip" onclick="setTopicFilter('#Vision')">#Vision</button>
                    <button class="tag-chip" onclick="setTopicFilter('#Production')">#Production</button>
                    <button class="tag-chip" onclick="setTopicFilter('#Robotics')">#Robotics</button>
                    <button class="tag-chip" onclick="setTopicFilter('#Breakthroughs')">#Breakthroughs</button>
                </div>
            </div>

            <!-- Articles Grid -->
            <div class="articles-grid" id="articles-grid">
                <!-- Dynamically populated cards -->
            </div>

            <!-- Quick Hit 1-Liners -->
            <div class="oneliners-card" id="oneliners-container">
                <div class="oneliners-header">
                    <span>Quick-Hit 1-Liners (Remaining Scanned Articles)</span>
                    <span id="oneliner-count" style="font-size:12px;color:var(--text-muted);font-weight:600;"></span>
                </div>
                <div id="oneliners-list">
                    <!-- Dynamically populated 1-liners -->
                </div>
            </div>
        </section>

        <!-- ==================== SECTION 2: FRONTIER MODELS ==================== -->
        <section id="view-models" style="display:none;">
            <div class="section-header">
                <h1 class="section-title">Frontier Model Intelligence Tracker</h1>
                <p class="section-desc">Comprehensive catalog of production &amp; open-weights frontier models by lab. Click any model to inspect pricing, context limits, and capabilities.</p>
            </div>

            <!-- Lab Filter Bar -->
            <div class="lab-filter-bar" id="lab-filter-bar">
                <button class="lab-chip active" onclick="filterModelsByLab('all')">All Labs</button>
                <button class="lab-chip" onclick="filterModelsByLab('google')">Google DeepMind</button>
                <button class="lab-chip" onclick="filterModelsByLab('openai')">OpenAI</button>
                <button class="lab-chip" onclick="filterModelsByLab('anthropic')">Anthropic</button>
                <button class="lab-chip" onclick="filterModelsByLab('deepseek')">DeepSeek</button>
                <button class="lab-chip" onclick="filterModelsByLab('meta')">Meta AI</button>
                <button class="lab-chip" onclick="filterModelsByLab('xai')">xAI</button>
                <button class="lab-chip" onclick="filterModelsByLab('alibaba')">Alibaba (Qwen)</button>
                <button class="lab-chip" onclick="filterModelsByLab('mistral')">Mistral AI</button>
            </div>

            <!-- Models Grid -->
            <div class="models-grid" id="models-grid">
                <!-- Dynamically populated model cards -->
            </div>
        </section>

        <!-- ==================== SECTION 3: MILESTONES ARCHIVE ==================== -->
        <section id="view-milestones" style="display:none;">
            <div class="section-header">
                <h1 class="section-title">Landmark AI Milestones Archive (2023 – 2026)</h1>
                <p class="section-desc">Documenting major inflection points, model releases, and architectural breakthroughs across 36 months of AI progress.</p>
            </div>

            <!-- Period Selector Bar -->
            <div class="milestone-period-bar">
                <button class="period-chip active" id="pchip-yearly" onclick="switchMilestonePeriod('yearly')">Yearly Top 3</button>
                <button class="period-chip" id="pchip-half_yearly" onclick="switchMilestonePeriod('half_yearly')">6-Month Top 3</button>
                <button class="period-chip" id="pchip-quarterly" onclick="switchMilestonePeriod('quarterly')">Quarterly Top 3</button>
                <button class="period-chip" id="pchip-monthly" onclick="switchMilestonePeriod('monthly')">Monthly Top 3 (Past 36 Mo)</button>
                <button class="period-chip" id="pchip-weekly" onclick="switchMilestonePeriod('weekly')">Weekly Top 3 (Rolling)</button>
            </div>

            <div id="milestones-container">
                <!-- Dynamically populated milestone groups -->
            </div>
        </section>

        <!-- ==================== SECTION 4: TASK GUIDE ==================== -->
        <section id="view-tasks" style="display:none;">
            <div class="section-header">
                <h1 class="section-title">Task-Based Model Selection Guide</h1>
                <p class="section-desc">Engineering recommendations based on latency, benchmark scores, reasoning depth, and cost economics.</p>
            </div>

            <div class="tasks-grid">
                <div class="task-card">
                    <div>
                        <div class="task-title">💻 Agentic Coding &amp; Whole-Repo Refactoring</div>
                        <p style="font-size:14px;color:var(--text-secondary);line-height:1.5;">Tasks requiring multi-file analysis, unit test generation, and autonomous terminal PR execution.</p>
                        <div class="task-recommendations">
                            <div class="task-rec-item">
                                <div class="task-rec-role">Frontier Proprietary SOTA</div>
                                <strong>Claude 3.7 Sonnet (Extended Thinking)</strong> &bull; Best-in-class tool use &amp; SWE-bench verified.
                            </div>
                            <div class="task-rec-item">
                                <div class="task-rec-role">Open Weights Champion</div>
                                <strong>Qwen 2.5 Coder 32B</strong> &bull; Highest accuracy open model, runnable on single 24GB GPU.
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
                                <div class="task-rec-role">Maximum Frontier Reasoning</div>
                                <strong>OpenAI o3 / o3-mini (High Effort)</strong> &bull; Test-time compute scaling champion.
                            </div>
                            <div class="task-rec-item">
                                <div class="task-rec-role">Open Architecture Equivalent</div>
                                <strong>DeepSeek-R1 (671B MoE)</strong> &bull; Pure RL chain-of-thought matching o1.
                            </div>
                        </div>
                    </div>
                </div>

                <div class="task-card">
                    <div>
                        <div class="task-title">🎬 High-Definition Generative Video &amp; World Simulation</div>
                        <p style="font-size:14px;color:var(--text-secondary);line-height:1.5;">Cinematic 1080p generation, physical motion simulation, camera control, and rapid prototyping.</p>
                        <div class="task-recommendations">
                            <div class="task-rec-item">
                                <div class="task-rec-role">Best Quality &amp; Temporal Consistency</div>
                                <strong>Google Veo 3.1 &amp; OpenAI Sora 2</strong> &bull; Industry standards for coherent physical physics.
                            </div>
                            <div class="task-rec-item">
                                <div class="task-rec-role">High-Speed API Pipeline</div>
                                <strong>Veo 3.1 Fast</strong> &bull; Sub-5 second video turnarounds for creator applications.
                            </div>
                        </div>
                    </div>
                </div>

                <div class="task-card">
                    <div>
                        <div class="task-title">📚 Massive Multi-Document &amp; Video Context (1M+ Tokens)</div>
                        <p style="font-size:14px;color:var(--text-secondary);line-height:1.5;">Analyzing whole codebases, legal portfolios, or 2 hours of raw security camera footage in one prompt.</p>
                        <div class="task-recommendations">
                            <div class="task-rec-item">
                                <div class="task-rec-role">2M Token Champion</div>
                                <strong>Gemini 3.1 Pro (2,000,000 Tokens)</strong> &bull; Near-perfect needle-in-a-haystack recall.
                            </div>
                            <div class="task-rec-item">
                                <div class="task-rec-role">Low-Cost 1M Context</div>
                                <strong>Gemini 3.8 Flash ($0.10/1M)</strong> &bull; High-speed whole repository processing.
                            </div>
                        </div>
                    </div>
                </div>

                <div class="task-card">
                    <div>
                        <div class="task-title">🔒 Air-Gapped &amp; Private Local Inference</div>
                        <p style="font-size:14px;color:var(--text-secondary);line-height:1.5;">Strict zero-data-leakage environments, offline mobile devices, or high-security financial/healthcare applications.</p>
                        <div class="task-recommendations">
                            <div class="task-rec-item">
                                <div class="task-rec-role">High Reasoning on Single GPU</div>
                                <strong>DeepSeek-R1-Distill-32B &amp; Qwen 3.8 27B</strong> &bull; Runs on RTX 4090/5090 or Mac M-series.
                            </div>
                            <div class="task-rec-item">
                                <div class="task-rec-role">Dual GPU Workhorse</div>
                                <strong>Llama 3.3 70B Instruct</strong> &bull; 405B quality on dual consumer GPUs.
                            </div>
                        </div>
                    </div>
                </div>

                <div class="task-card">
                    <div>
                        <div class="task-title">🖱️ Desktop OS &amp; GUI Browser Automation</div>
                        <p style="font-size:14px;color:var(--text-secondary);line-height:1.5;">Controlling native software without APIs, clicking web buttons, filling legacy invoice portals.</p>
                        <div class="task-recommendations">
                            <div class="task-rec-item">
                                <div class="task-rec-role">Native OS Agent API</div>
                                <strong>Gemini 2.5 Computer Use &amp; Anthropic Computer Use</strong> &bull; Precise coordinate screenshot control.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </div>

    <!-- ==================== MODEL INSPECTION DRAWER ==================== -->
    <div class="drawer-backdrop" id="drawer-backdrop" onclick="closeModelDrawer(event)">
        <div class="drawer-content" id="drawer-content" onclick="event.stopPropagation()">
            <button class="drawer-close-btn" onclick="closeModelDrawer()">✕</button>
            
            <div>
                <div id="drawer-lab" style="font-size:12px;font-weight:800;color:var(--accent-green);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;"></div>
                <h2 id="drawer-name" style="font-size:26px;font-weight:800;letter-spacing:-0.02em;color:#ffffff;margin-bottom:8px;"></h2>
                <div id="drawer-tags" style="display:flex;gap:6px;flex-wrap:wrap;"></div>
            </div>

            <!-- Pricing Table -->
            <div>
                <div style="font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-muted);margin-bottom:8px;">API Token Pricing (USD)</div>
                <table class="pricing-table">
                    <thead>
                        <tr>
                            <th>Input / 1M</th>
                            <th>Output / 1M</th>
                            <th>Cached Input / 1M</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td id="drawer-price-in">-</td>
                            <td id="drawer-price-out">-</td>
                            <td id="drawer-price-cached">-</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Specs Grid -->
            <div>
                <div style="font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-muted);margin-bottom:8px;">Architecture &amp; Context Limits</div>
                <div style="background:#121212;border:1px solid var(--border-subtle);border-radius:var(--radius-md);padding:14px;display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:13px;">
                    <div>
                        <div style="color:var(--text-muted);font-size:11px;font-weight:700;text-transform:uppercase;">Context Window</div>
                        <div id="drawer-context" style="color:#ffffff;font-weight:700;margin-top:2px;"></div>
                    </div>
                    <div>
                        <div style="color:var(--text-muted);font-size:11px;font-weight:700;text-transform:uppercase;">Max Output Limit</div>
                        <div id="drawer-max-out" style="color:#ffffff;font-weight:700;margin-top:2px;"></div>
                    </div>
                    <div style="grid-column: span 2;">
                        <div style="color:var(--text-muted);font-size:11px;font-weight:700;text-transform:uppercase;">Architecture</div>
                        <div id="drawer-arch" style="color:#ffffff;margin-top:2px;"></div>
                    </div>
                </div>
            </div>

            <!-- Capabilities List -->
            <div>
                <div style="font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-muted);margin-bottom:8px;">Supported Capabilities</div>
                <div id="drawer-capabilities" style="display:flex;gap:6px;flex-wrap:wrap;"></div>
            </div>

            <!-- Best Application -->
            <div>
                <div style="font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-muted);margin-bottom:8px;">Best Suited For</div>
                <div id="drawer-best" style="font-size:14px;color:var(--text-secondary);line-height:1.6;background:#121212;border:1px solid var(--border-subtle);border-radius:var(--radius-md);padding:14px;"></div>
            </div>

            <!-- Code / CLI Snippet -->
            <div>
                <div style="font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-muted);margin-bottom:8px;">Quickstart Code / CLI Execution</div>
                <div class="code-block-wrap">
                    <button class="copy-code-btn" onclick="copyDrawerCode()">Copy</button>
                    <div class="code-block" id="drawer-code"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- ==================== JAVASCRIPT APPLICATION LOGIC ==================== -->
    <script>
        const EMBEDDED_SEED = {seed_json_str};
        const FRONTIER_MODELS = {models_json_str};
        const MILESTONES_ARCHIVE = {milestones_json_str};

        let supabaseClient = null;
        let allArticlesByDate = {{}};
        let availableDates = [];
        let selectedDate = null;
        let selectedTopicFilter = 'all';

        // 1. App Initialization
        document.addEventListener("DOMContentLoaded", async () => {{
            buildCalendarDates();
            renderModelsGrid(FRONTIER_MODELS);
            renderMilestones("yearly");
            loadSeedDataset();
            await initSupabaseConnection();
        }});

        function switchTab(tabId) {{
            document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".app-container > section").forEach(s => s.style.display = "none");

            document.getElementById(`tab-${{tabId}}`).classList.add("active");
            document.getElementById(`view-${{tabId}}`).style.display = "block";
            window.scrollTo({{ top: 0, behavior: "smooth" }});
        }}

        // 2. Calendar Dates
        function buildCalendarDates() {{
            const bar = document.getElementById("calendar-bar");
            bar.innerHTML = "";
            availableDates = [];

            // Calculate last 7 calendar days
            for (let i = 0; i < 7; i++) {{
                const d = new Date();
                d.setUTCDate(d.getUTCDate() - i);
                const isoStr = d.toISOString().split("T")[0];
                availableDates.push(isoStr);

                const chip = document.createElement("button");
                chip.className = `date-chip ${{i === 0 ? 'active' : ''}}`;
                chip.id = `date-chip-${{isoStr}}`;
                
                const label = (i === 0) ? "Today" : (i === 1) ? "Yesterday" : d.toLocaleDateString("en-US", {{ month: "short", day: "numeric", timeZone: "UTC" }});
                chip.innerText = `${{label}} (${{isoStr}})`;
                chip.onclick = () => selectCalendarDate(isoStr);
                bar.appendChild(chip);
            }}

            selectedDate = availableDates[0];
        }}

        function selectCalendarDate(dateStr) {{
            selectedDate = dateStr;
            document.querySelectorAll(".date-chip").forEach(c => c.classList.remove("active"));
            const activeChip = document.getElementById(`date-chip-${{dateStr}}`);
            if (activeChip) activeChip.classList.add("active");
            renderCurrentDateArticles();
        }}

        // 3. Data Ingestion & Supabase
        function loadSeedDataset() {{
            if (EMBEDDED_SEED && Object.keys(EMBEDDED_SEED).length > 0) {{
                allArticlesByDate = {{ ...EMBEDDED_SEED }};
            }} else {{
                allArticlesByDate = {{}};
            }}
            renderCurrentDateArticles();
        }}

        async function initSupabaseConnection() {{
            // 1. Try Vercel auto-config
            try {{
                const resp = await fetch('/api/config');
                if (resp.ok) {{
                    const data = await resp.json();
                    if (data.supabaseUrl && data.supabaseAnonKey) {{
                        connectSupabase(data.supabaseUrl, data.supabaseAnonKey);
                        return;
                    }}
                }}
            }} catch (e) {{}}

            // 2. Try localStorage
            const localUrl = localStorage.getItem("ai_pulse_sb_url");
            const localKey = localStorage.getItem("ai_pulse_sb_key");
            if (localUrl && localKey) {{
                connectSupabase(localUrl, localKey);
            }}
        }}

        function connectSupabase(url, key) {{
            if (window.supabase) {{
                try {{
                    supabaseClient = window.supabase.createClient(url, key);
                    document.getElementById("header-sync-status").innerText = "Supabase Live";
                    document.getElementById("header-sync-status").style.color = "var(--accent-green)";
                    fetchLiveSupabaseData();
                }} catch (e) {{
                    console.error("Supabase connection error:", e);
                }}
            }}
        }}

        async function fetchLiveSupabaseData() {{
            if (!supabaseClient) return;
            try {{
                const {{ data, error }} = await supabaseClient
                    .from('articles')
                    .select('*')
                    .order('published_date', {{ ascending: false }});

                if (!error && data && data.length > 0) {{
                    mergeSupabaseRows(data);
                }}
            }} catch (e) {{
                console.warn("Using local cache:", e);
            }}
        }}

        function mergeSupabaseRows(rows) {{
            const grouped = {{}};
            rows.forEach(art => {{
                if (!art.published_date) return;
                const dStr = art.published_date.split("T")[0];
                if (!grouped[dStr]) {{
                    grouped[dStr] = {{ top_10: [], one_liners: [] }};
                }}
                if (art.is_groundbreaking || art.category_tag === "BREAKTHROUGH" || grouped[dStr].top_10.length < 10) {{
                    grouped[dStr].top_10.push(art);
                }} else {{
                    grouped[dStr].one_liners.push(art);
                }}
            }});

            // Merge into allArticlesByDate
            for (const [dateKey, payload] of Object.entries(grouped)) {{
                allArticlesByDate[dateKey] = payload;
            }}

            renderCurrentDateArticles();
        }}

        // 4. Feed Rendering & Real-Time Filters
        function setTopicFilter(tag) {{
            selectedTopicFilter = tag;
            document.querySelectorAll(".tag-chip").forEach(c => c.classList.remove("active"));
            event.target.classList.add("active");
            filterArticles();
        }}

        function renderCurrentDateArticles() {{
            filterArticles();
        }}

        function filterArticles() {{
            const grid = document.getElementById("articles-grid");
            const onelinersList = document.getElementById("oneliners-list");
            const query = document.getElementById("search-input").value.toLowerCase().trim();

            const dateData = allArticlesByDate[selectedDate] || {{ top_10: [], one_liners: [] }};
            let featured = dateData.top_10 || [];
            let oneliners = dateData.one_liners || [];

            // If selected date is empty, fallback to most recent date available
            if (featured.length === 0 && oneliners.length === 0) {{
                const keys = Object.keys(allArticlesByDate);
                if (keys.length > 0) {{
                    featured = allArticlesByDate[keys[0]].top_10 || [];
                    oneliners = allArticlesByDate[keys[0]].one_liners || [];
                }}
            }}

            // Filter featured
            const filteredFeatured = featured.filter(art => matchesSearchAndTopic(art, query, selectedTopicFilter));
            const filteredOneLiners = oneliners.filter(art => matchesSearchAndTopic(art, query, selectedTopicFilter));

            // Render Featured Cards
            if (filteredFeatured.length === 0) {{
                grid.innerHTML = `<div class="empty-state" style="grid-column: 1 / -1;">No featured stories found for the selected date and filters.</div>`;
            }} else {{
                grid.innerHTML = filteredFeatured.map(art => renderArticleCard(art)).join("");
            }}

            // Render 1-Liners
            document.getElementById("oneliner-count").innerText = `(${{filteredOneLiners.length}} items)`;
            if (filteredOneLiners.length === 0) {{
                onelinersList.innerHTML = `<div style="color:var(--text-muted);font-size:13px;padding:8px 0;">No matching quick-hits.</div>`;
            }} else {{
                onelinersList.innerHTML = filteredOneLiners.map(art => `
                    <div class="oneliner-item">
                        <div class="oneliner-text">
                            <a href="${{art.url}}" target="_blank" class="oneliner-title">${{escapeHtml(art.title)}}</a>
                            <span>— ${{escapeHtml(art.one_liner || art.summary || '')}}</span>
                        </div>
                        <span style="font-size:11px;color:var(--text-muted);white-space:nowrap;">${{escapeHtml(art.source)}}</span>
                    </div>
                `).join("");
            }}
        }}

        function matchesSearchAndTopic(art, query, topic) {{
            // 1. Topic match
            if (topic !== 'all') {{
                const tag = (art.category_tag || '').toLowerCase();
                const title = (art.title || '').toLowerCase();
                const text = (art.summary || '').toLowerCase();

                if (topic === '#FrontierModels' && !tag.includes('frontier') && !title.includes('gemini') && !title.includes('claude') && !title.includes('openai') && !title.includes('deepseek')) return false;
                if (topic === '#Reasoning' && !text.includes('reason') && !text.includes('think') && !text.includes('proof')) return false;
                if (topic === '#AgenticCoding' && !tag.includes('dev') && !text.includes('code') && !text.includes('agent')) return false;
                if (topic === '#LocalLLM' && !tag.includes('local') && !text.includes('quant') && !text.includes('gguf')) return false;
                if (topic === '#Vision' && !text.includes('vision') && !text.includes('image') && !text.includes('video')) return false;
                if (topic === '#Production' && !tag.includes('prod') && !text.includes('vllm') && !text.includes('deploy')) return false;
                if (topic === '#Robotics' && !text.includes('robot') && !text.includes('dexterous') && !text.includes('manipulation')) return false;
                if (topic === '#Breakthroughs' && !art.is_groundbreaking && !tag.includes('breakthrough')) return false;
            }}

            // 2. Query match
            if (!query) return true;
            const fullStr = `${{art.title}} ${{art.summary}} ${{art.dev_use_case}} ${{art.source}} ${{art.category}}`.toLowerCase();
            return fullStr.includes(query);
        }}

        function renderArticleCard(art) {{
            const isBreakthrough = art.is_groundbreaking || art.category_tag === "BREAKTHROUGH";
            const badgeClass = isBreakthrough ? "badge-breakthrough" : 
                               art.category_tag === "DEV TOOLS" ? "badge-devtools" :
                               art.category_tag === "LOCAL AI" ? "badge-local" :
                               art.category_tag === "PRODUCTION" ? "badge-prod" : "badge-research";
            const badgeLabel = isBreakthrough ? "🚨 BREAKTHROUGH" : (art.category || "AI RESEARCH");

            const imgHtml = art.image_url ? `
                <div class="article-img-wrap">
                    <img src="${{art.image_url}}" class="article-img" alt="Visual Preview" onerror="this.parentElement.style.display='none'">
                </div>
            ` : "";

            const capabilityHtml = art.new_capability || isBreakthrough ? `
                <div class="capability-box">
                    <div class="capability-label">⚡ New Capability Unlocked</div>
                    ${{escapeHtml(art.new_capability || 'Zero-shot online camera pose formulation achieving state-of-the-art scalable 3D reconstruction without test-time depth sensors.')}}
                </div>
            ` : "";

            const useCaseHtml = art.dev_use_case ? `
                <div class="usecase-box">
                    <div class="usecase-label">Practical Dev Application</div>
                    ${{escapeHtml(art.dev_use_case)}}
                </div>
            ` : "";

            return `
                <article class="article-card">
                    <div>
                        <div class="card-top">
                            <span class="badge ${{badgeClass}}">${{badgeLabel}}</span>
                            <span class="card-meta">${{escapeHtml(art.source)}}</span>
                        </div>
                        <a href="${{art.url}}" target="_blank" class="article-title">${{escapeHtml(art.title)}}</a>
                        ${{imgHtml}}
                        <p class="article-summary">${{escapeHtml(art.summary || '')}}</p>
                        ${{capabilityHtml}}
                        ${{useCaseHtml}}
                    </div>
                    <div class="card-bottom">
                        <span class="source-pill">${{art.published_date ? art.published_date.split("T")[0] : 'Today'}}</span>
                        <a href="${{art.url}}" target="_blank" class="read-btn">Read Article ↗</a>
                    </div>
                </article>
            `;
        }}

        // 5. Frontier Models & Inspection Drawer
        function renderModelsGrid(models) {{
            const grid = document.getElementById("models-grid");
            grid.innerHTML = models.map(m => `
                <div class="model-card" onclick="openModelDrawer('${{m.id}}')">
                    <div class="model-top">
                        <div class="model-lab-badge">${{escapeHtml(m.lab)}} &bull; ${{m.year}}</div>
                        <div class="model-name">${{escapeHtml(m.name)}}</div>
                        <div class="model-specs-row">
                            <span class="badge badge-prod">${{escapeHtml(m.readiness)}}</span>
                            <span class="spec-pill">${{escapeHtml(m.context_window)}}</span>
                            <span class="spec-pill">${{escapeHtml(m.license)}}</span>
                        </div>
                        <p class="model-best-for">${{escapeHtml(m.best_for)}}</p>
                    </div>
                    <div>
                        <div class="model-pricing-preview">
                            <span>Input: ${{m.pricing_input}}</span>
                            <span>Output: ${{m.pricing_output}}</span>
                        </div>
                        <div class="inspect-action-text">Inspect Specs &amp; Code ➔</div>
                    </div>
                </div>
            `).join("");
        }}

        function filterModelsByLab(labSlug) {{
            document.querySelectorAll(".lab-chip").forEach(c => c.classList.remove("active"));
            event.target.classList.add("active");

            if (labSlug === "all") {{
                renderModelsGrid(FRONTIER_MODELS);
            }} else {{
                const filtered = FRONTIER_MODELS.filter(m => m.lab_slug === labSlug);
                renderModelsGrid(filtered);
            }}
        }}

        function openModelDrawer(modelId) {{
            const m = FRONTIER_MODELS.find(x => x.id === modelId);
            if (!m) return;

            document.getElementById("drawer-lab").innerText = `${{m.lab}} • ${{m.year}}`;
            document.getElementById("drawer-name").innerText = m.name;
            document.getElementById("drawer-tags").innerHTML = `
                <span class="badge badge-prod">${{m.readiness}}</span>
                <span class="spec-pill">${{m.license}}</span>
                <span class="spec-pill">${{m.tag}}</span>
            `;

            document.getElementById("drawer-price-in").innerText = m.pricing_input;
            document.getElementById("drawer-price-out").innerText = m.pricing_output;
            document.getElementById("drawer-price-cached").innerText = m.pricing_cached;

            document.getElementById("drawer-context").innerText = m.context_window;
            document.getElementById("drawer-max-out").innerText = m.max_output;
            document.getElementById("drawer-arch").innerText = m.architecture;

            document.getElementById("drawer-capabilities").innerHTML = m.capabilities.map(c => `
                <span class="spec-pill" style="color:var(--accent-green);border:1px solid #1e3a24;background:#141d16;">✓ ${{c}}</span>
            `).join("");

            document.getElementById("drawer-best").innerText = m.best_for;
            document.getElementById("drawer-code").innerText = m.api_snippet;

            document.getElementById("drawer-backdrop").classList.add("open");
            document.body.style.overflow = "hidden";
        }}

        function closeModelDrawer(event) {{
            if (event && event.target.id !== "drawer-backdrop" && !event.target.classList.contains("drawer-close-btn")) {{
                return;
            }}
            document.getElementById("drawer-backdrop").classList.remove("open");
            document.body.style.overflow = "";
        }}

        function copyDrawerCode() {{
            const code = document.getElementById("drawer-code").innerText;
            navigator.clipboard.writeText(code);
            const btn = document.querySelector(".copy-code-btn");
            btn.innerText = "Copied!";
            setTimeout(() => btn.innerText = "Copy", 1500);
        }}

        // 6. Milestones Period Rendering
        function switchMilestonePeriod(periodType) {{
            document.querySelectorAll(".period-chip").forEach(c => c.classList.remove("active"));
            document.getElementById(`pchip-${{periodType}}`).classList.add("active");
            renderMilestones(periodType);
        }}

        function renderMilestones(periodType) {{
            const container = document.getElementById("milestones-container");
            const items = MILESTONES_ARCHIVE[periodType] || [];

            container.innerHTML = items.map(grp => `
                <div class="milestone-group">
                    <div class="milestone-group-title">
                        <span>📅 ${{grp.period}} Landmark Top 3</span>
                    </div>
                    <div>
                        ${{grp.top3.map(m => `
                            <div class="milestone-card">
                                <div class="milestone-header">
                                    <span class="milestone-title">${{escapeHtml(m.title)}}</span>
                                    <span class="milestone-lab">${{escapeHtml(m.lab)}} &bull; ${{m.date}}</span>
                                </div>
                                <div class="milestone-cap"><strong>Capability Unlocked:</strong> ${{escapeHtml(m.capability)}}</div>
                                ${{m.impact ? `<div class="milestone-impact"><strong>Developer Impact:</strong> ${{escapeHtml(m.impact)}}</div>` : ''}}
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
    </script>
</body>
</html>"""

with open("index.html", "w") as f:
    f.write(html_template)

print("✅ Successfully built Spotify-inspired index.html!")
