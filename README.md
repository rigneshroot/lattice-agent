# Lattice Agent

![Lattice Welcome Banner](docs/images/lattice_welcome_banner.png)

Lattice is a production-grade autonomous research agent framework written in Python. It rejects overly complex state-graph architectures in favor of a lean, iterative execution loop reinforced by token-based Jaccard self-validation loop guards, declarative tool registries, and plug-and-play LLM providers.

Inspired by Charlie Munger’s mental models of multi-dimensional understanding, Lattice is designed to systematically explore queries, cross-reference sources, prevent cognitive loops, and synthesize deep analytical resolutions.

---

## Core Features

- **Recursive Orchestration Loop**: A unified, step-by-step reasoning cycle executing thoughts, actions, and observations.
- **Jaccard Similarity Validation**: Proactively tokenizes, cleans, and computes word overlap (threshold >= 0.7) between consecutive queries to immediately flag and block infinite agent execution loops.
- **Durable Identity Layer (SOUL.md)**: Fully decouples the agent's cognitive persona, behavioral protocols, and domain directives from source code.
- **Model-Agnostic Routing**: Integrated adapters to swap between Google Gemini (google-genai), OpenAI (openai), and offline Ollama backends.
- **Declarative Tools**: Clean, schema-driven tool creation using standard parameter validation maps.
- **Aesthetic Terminal REPL**: An interactive command-line experience with loading spinners, ANSI typography, and visual step indicators.

---

## Project Structure

```bash
lattice-agent/
├── SOUL.md              # Cognitive personality and analytical bounds
├── main.py              # Application entry point & bootstrap loading
├── examples.py          # Programmatic API & custom tool examples
├── requirements.txt     # Essential library dependencies
├── LICENSE              # Software license agreement
├── agent/
│   ├── agent.py         # Main execution loop and JSON tool parsers
│   ├── prompts.py       # Prompt compilers (SOUL.md integration)
│   ├── scratchpad.py    # State manager tracking thoughts & actions
│   └── validation.py    # Tokenizer & Jaccard Index calculator
├── providers/
│   └── router.py        # LLM client adapters (Gemini, OpenAI, Ollama)
├── tools/
│   ├── base.py          # Abstract BaseTool blueprint class
│   ├── registry.py      # Centralized loading and tool execution
│   ├── web_search.py    # Serper API + DuckDuckGo HTML scraping
│   └── reader.py        # Web reader and HTML tag stripping
├── gateways/
│   └── terminal.py      # Interactive console shell gateway
├── docs/
│   ├── architecture.md  # Deep technical architecture details
│   ├── getting_started.md # Installation & operation handbook
│   └── images/          # Branding, blueprints, and console mockups
└── tests/
    ├── test_jaccard.py  # Jaccard index unit tests
    └── test_loop_detection.py # Validation triggers assertions
```

---

## Programmatic Developer Examples

You can run our curated developer script to observe programmatic execution flow and see how easy it is to register custom tools in the registry:

```bash
python examples.py
```

---

## Guided Resources

Embark on the Lattice journey by exploring our highly detailed visual documents:

1. **[Technical Architecture Guide](docs/architecture.md)**: Explore the cognitive pipeline, Jaccard calculations, and provider wrappers.
2. **[Getting Started Handbook](docs/getting_started.md)**: Set up virtual environments, configure environment parameters, and launch the interactive REPL terminal.

---

## Author
Developed and maintained by **Rignesh P**.

## License
Lattice is open-source software licensed under the [MIT License](LICENSE).
