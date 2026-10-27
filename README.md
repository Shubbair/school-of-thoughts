# School of Thoughts LLM

![llmcouncil](assets/image.png){: width="60%"}


Council of philosophical schools , default council includes four positions: materialist/naturalist, idealist, existentialist, and Stoic. Each member answers and stays inside its own framework. Then the facilitator maps what each school sees, where the frameworks conflict, and why an open-ended question may not have one winning answer.

In a bit more detail, here is what happens when you submit a query:

1. **Opening views** / The question is given to every school. Each member answers using Position, Reasoning, and Limit or open question.
2. **Rebuttals** / Each member sees the other responses and, from inside its own framework, explains the point of conflict and what its school struggles to explain.
3. **Facilitator synthesis** / The report is organized into Agreement, Disagreement, Minority View, and Bottom Line without ranking the schools or choosing a winner.

Inherit the Idea form Karpathy based repo [LLM Council](https://github.com/karpathy/llm-council), and vibe code it to make this.


## Setup

### 1. Install Dependencies

The project uses [uv](https://docs.astral.sh/uv/) for project management.

**Backend:**
```bash
uv sync
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 2. Configure the model provider

Copy `.env.example` to `.env`, then choose one provider:

```bash
# Local model (default)
MODEL_PROVIDER=ollama
OLLAMA_MODEL=qwen3:1.7b

# Or an OpenAI-compatible API
# MODEL_PROVIDER=api
# API_BASE_URL=https://api.openai.com/v1
# API_KEY=your-key
# API_MODEL=gpt-4o-mini
```

For OpenRouter, use `API_BASE_URL=https://openrouter.ai/api/v1` and set `API_KEY` to your OpenRouter key. The API provider also works with compatible gateways that expose `/chat/completions`.

### 3. Configure Models (Optional)

Edit `backend/config.py` to customize the council. Add one `school(...)` entry to `COUNCIL_MEMBERS`:

```python
school(
	"Confucian",
	"human flourishing depends on cultivated relationships, ritual, family duties, and social harmony",
),
```

The shared prompt automatically tells the new member to answer in English and requires the same organized answer structure.

## Running the Application

**Option 1: Use the start script**
```bash
./start.sh
```

**Option 2: Run manually**

Terminal 1 (Backend):
```bash
uv run python -m backend.main
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

## Tech Stack

- **Backend:** FastAPI (Python 3.10+), async httpx, OpenRouter API
- **Frontend:** React + Vite, react-markdown for rendering
- **Storage:** JSON files in `data/conversations/`
- **Package Management:** uv for Python, npm for JavaScript
