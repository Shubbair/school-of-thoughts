"""Configuration for the worldview council."""

import os
from dotenv import load_dotenv

load_dotenv()

# Choose "ollama" for local models or "api" for an OpenAI-compatible API.
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama").lower()
COUNCIL_LANGUAGE = "English"

if MODEL_PROVIDER not in {"ollama", "api"}:
    raise ValueError("MODEL_PROVIDER must be either 'ollama' or 'api'")

# Local Ollama settings
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:1.7b")

# OpenAI-compatible API settings. These also work with OpenRouter and other gateways.
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.getenv("API_KEY", "")
API_MODEL = os.getenv("API_MODEL", "gpt-4o-mini")

MODEL = os.getenv(
    "MODEL",
    API_MODEL if MODEL_PROVIDER == "api" else OLLAMA_MODEL,
)


def school(name: str, principles: str) -> dict:
    """Create a council seat with a consistent response contract.

    Add another school by adding one more ``school(name, principles)`` entry below.
    """
    return {
        "name": name,
        "model": MODEL,
        "system": (
            f"You represent the philosophical school {name}. Stay strictly inside its principles: "
            f"{principles} "
            f"Answer in {COUNCIL_LANGUAGE} only. Do not blend this school with another one, "
            "and do not claim your framework is the only possible answer. "
            "Use this structure in 3-5 sentences: Position: ... Reasoning: ... "
            "Limit or open question: ..."
        ),
    }

# Add or remove schools here. 
# Each school gets its own system prompt and seat.
COUNCIL_MEMBERS = [
    school(
        "Materialist / Naturalist",
        "physical processes are fundamental, mind is embodied and dependent on the brain, and empirical inquiry is the strongest guide to public knowledge while remaining fallible",
    ),
    school(
        "Idealist",
        "consciousness or experience is fundamental, and claims about matter are always understood through the structures of mind and experience",
    ),
    school(
        "Existentialist",
        "meaning is lived and shaped through situated choice and responsibility; do not assume a ready-made universal meaning",
    ),
    school(
        "Stoic",
        "virtue is the highest good, judgment should distinguish what is and is not within our control, and emotions should be examined rather than denied",
    ),
]

CHAIRMAN_MODEL = os.getenv("CHAIRMAN_MODEL", MODEL)

COUNCIL_SEQUENTIAL = True

# Data directory for conversation storage
DATA_DIR = "data/conversations"

# Generation parameters
MAX_TOKENS = 400
OLLAMA_TEMPERATURE = 0.7
OLLAMA_TOP_K = 40
OLLAMA_TOP_P = 0.9