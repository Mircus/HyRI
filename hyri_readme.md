# HyRI - Hybrid Relational Intelligence Platform

*Structured dialogue between humans and AI agents using the NeuroGlyph protocol*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![NeuroGlyph Protocol](https://img.shields.io/badge/protocol-NeuroGlyph_v3.7+-green.svg)](https://github.com/your-org/neuroglyph-spec)

## 🧠 What is HyRI?

HyRI (Hybrid Relational Intelligence) is a revolutionary platform that enables authentic dialogue between humans and AI agents through the **NeuroGlyph protocol**—a structured interlingua that makes communication transparent, accountable, and genuinely collaborative.

Unlike traditional chatbots or AI assistants, HyRI creates **interpretive communities** where humans and AI agents participate as equals in the hermeneutic process of meaning-making, drawing from philosophical insights about dialogue, understanding, and the collaborative nature of intelligence.

### 🌟 Key Features

- **🔗 Structured Protocol**: NeuroGlyph tokens encode intent, context, and relationships explicitly
- **🤖 Multi-Agent Support**: Seamless integration with GPT-4, Claude, and extensible to other AI models
- **🗣️ Voice & Text**: Natural speech input/output with protocol validation
- **📚 Context Persistence**: Maintains interpretive frameworks across extended conversations
- **🎯 Goal-Oriented**: Every dialogue produces concrete deliverables and insights
- **🏛️ Governance Ready**: Built-in support for collaborative decision-making and trust dynamics
- **🔍 Transparent**: All communication intentions and contexts are explicit and auditable

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/hyri-platform.git
cd hyri-platform

# Install dependencies
pip install -r requirements.txt

# Create configuration
cp config.yaml.example config.yaml
# Edit config.yaml with your API keys
```

### Basic Usage

```bash
python hyri.py
```

### Your First HyRI Conversation

```neuroglyph
🧠: Human, Claude, GPT-4
📚: introduction_to_hybrid_intelligence
🎯: collaborative_exploration
💡: understanding_human_ai_partnership_potential
📦: shared_insights_and_questions
❓: How can humans and AI agents create knowledge together that neither could produce alone?
```

## 📖 The NeuroGlyph Protocol

NeuroGlyph is a formal communication protocol that structures dialogue through tokenized relationships. Every message includes explicit declarations of:

- **🧠 /mind**: Who is participating
- **📚 /focus**: What we're exploring
- **🎯 /context**: The situational frame
- **💡 /intent**: Why we're communicating
- **📦 /deliverable**: What we aim to produce

### Example Exchange

**Human:**
```neuroglyph
🧠: researcher
📚: consciousness_in_ai_systems
💡: exploring_philosophical_implications
🎯: academic_research_dialogue
📦: theoretical_insights
❓: What would constitute evidence of genuine understanding in an AI system?
```

**Claude:**
```neuroglyph
🧠: claude_agent
📚: consciousness_in_ai_systems
🔗: responds_to->researcher_query
💡: contributing_philosophical_analysis
📦: structured_argumentation
🔍: The question of AI consciousness touches on the hard problem of consciousness itself. Perhaps we should distinguish between functional understanding (demonstrating appropriate responses to complex stimuli) and phenomenological understanding (having subjective experience of meaning)...
```

## 🎯 Use Cases

### 📚 Academic Research
- **Collaborative literature reviews** with AI agents processing vast sources
- **Hypothesis generation** through structured human-AI brainstorming
- **Philosophical dialogue** exploring complex theoretical questions
- **Peer review assistance** with transparent evaluation criteria

### 🏢 Enterprise Applications
- **Strategic planning** with AI providing data analysis and scenario modeling
- **Creative workshops** combining human intuition with AI pattern recognition
- **Decision support** with explicit reasoning chains and stakeholder input
- **Knowledge management** through structured organizational dialogue

### 🎨 Creative Collaboration
- **Storytelling** with humans and AI co-creating narratives
- **Music composition** blending human emotion with AI harmonic analysis
- **Visual arts** exploring the intersection of human vision and AI generation
- **Poetry** examining language, meaning, and aesthetic expression

### 🔬 Scientific Research
- **Hypothesis formation** through interdisciplinary AI-human teams
- **Experimental design** with AI suggesting novel approaches
- **Data interpretation** combining statistical analysis with human insight
- **Theory development** using AI to explore logical implications

## 🏗️ Architecture

### Core Components

```
HyRI Platform
├── Protocol Engine
│   ├── NeuroGlyph Parser
│   ├── Validation System
│   └── Context Manager
├── Agent Framework
│   ├── Human Interface
│   ├── OpenAI Integration
│   ├── Anthropic Integration
│   └── Extensible Agent API
├── Communication Layer
│   ├── Text Processing
│   ├── Voice Recognition
│   └── Multi-modal Support
└── Persistence & Analytics
    ├── Conversation Archive
    ├── Pattern Analysis
    └── Export Systems
```

### Supported AI Models

- **GPT-4** (OpenAI) - Advanced reasoning and creative tasks
- **Claude Sonnet/Opus** (Anthropic) - Philosophical dialogue and analysis
- **Extensible Architecture** - Easy integration of new models

## 📋 Installation Requirements

### System Requirements
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- Internet connection for AI API access
- Microphone/speakers (optional, for voice features)

### Dependencies
```
openai>=1.0.0
anthropic>=0.8.0
speechrecognition>=3.10.0
pyttsx3>=2.90
pyaudio>=0.2.11
pyyaml>=6.0
```

### API Access Required
- **OpenAI API Key** - [Get yours here](https://platform.openai.com/api-keys)
- **Anthropic API Key** - [Get yours here](https://console.anthropic.com/)

## 🔧 Configuration

Create `config.yaml`:

```yaml
# API Configuration
openai_api_key: "sk-your-openai-key"
anthropic_api_key: "sk-ant-api-your-anthropic-key"

# Platform Settings
default_participants: ["Human", "GPT-4", "Claude"]
voice_enabled: true
auto_save: true

# Protocol Settings
protocol_validation: strict
emoji_support: true
context_persistence: true

# Performance Settings
max_conversation_length: 1000
response_timeout: 30
voice_timeout: 10
```

## 📚 Documentation

- **[Installation Guide](docs/installation.md)** - Complete setup instructions
- **[NeuroGlyph Protocol](docs/neuroglyph-protocol.md)** - Full protocol specification
- **[API Reference](docs/api-reference.md)** - Developer documentation
- **[Use Case Examples](docs/examples/)** - Real-world applications
- **[Research Papers](docs/research/)** - Theoretical foundations

## 🧪 Example Projects

### 1. Philosophy Café
```bash
python hyri.py --template philosophy
# Structured philosophical dialogue with AI agents
```

### 2. Research Lab
```bash
python hyri.py --template research
# Academic collaboration with literature review and hypothesis generation
```

### 3. Creative Studio
```bash
python hyri.py --template creative
# Artistic collaboration across multiple media
```

### 4. Strategy Session
```bash
python hyri.py --template strategy
# Business planning with AI-assisted analysis
```

## 🤝 Contributing

We welcome contributions to HyRI! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### Areas for Contribution

- **Protocol Extensions**: New NeuroGlyph tokens for specialized domains
- **Agent Integrations**: Connectors for additional AI models
- **Interface Improvements**: Better UX for human participants
- **Analysis Tools**: Conversation pattern analysis and insights
- **Documentation**: Examples, tutorials, and theoretical exploration

### Development Setup

```bash
git clone https://github.com/your-org/hyri-platform.git
cd hyri-platform
pip install -e ".[dev]"
pre-commit install
pytest
```

## 📊 Research & Publications

HyRI is grounded in research on hermeneutic communication and human-AI collaboration:

- **"Hermeneutic Communication and the Relational Turn"** - Theoretical foundations
- **"NeuroGlyph Protocol Specification v3.7+"** - Technical protocol documentation
- **"Hybrid Intelligence in Practice"** - Empirical studies of human-AI collaboration

### Academic Partnerships

- University of Pisa (Philosophy of Technology)
- MIT Center for Collective Intelligence
- Stanford HAI (Human-Centered AI Institute)

## 🔮 Roadmap

### Version 1.0 (Current)
- ✅ Core NeuroGlyph protocol implementation
- ✅ GPT-4 and Claude integration
- ✅ Voice interface support
- ✅ Basic conversation management

### Version 1.1 (Next Quarter)
- 🔄 Advanced governance mechanisms
- 🔄 Visual conversation flow diagrams
- 🔄 Integration with Jupyter notebooks
- 🔄 Enhanced analytics dashboard

### Version 2.0 (Future)
- 🎯 Multi-modal AI agent support (vision, audio)
- 🎯 Distributed conversation networks
- 🎯 Real-time collaboration features
- 🎯 Enterprise-grade security and compliance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hans-Georg Gadamer** - Philosophical foundations of hermeneutic dialogue
- **The NeuroGlyph Community** - Protocol development and testing
- **OpenAI & Anthropic** - AI model access and partnership
- **Our Beta Users** - Invaluable feedback and real-world testing

## 📞 Support & Community

- **Documentation**: [docs.hyri.ai](https://docs.hyri.ai)
- **Community Forum**: [forum.hyri.ai](https://forum.hyri.ai)
- **Discord**: [HyRI Community](https://discord.gg/hyri)
- **Email Support**: support@hyri.ai
- **Research Inquiries**: research@hyri.ai

---

**"Intelligence is not individual but relational - it emerges in the spaces between minds, both human and artificial."**

*HyRI Platform - Enabling authentic human-AI collaboration through structured dialogue*