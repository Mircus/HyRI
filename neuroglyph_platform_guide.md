# NeuroGlyph Platform - Installation & Usage Guide

A structured dialogue platform for humans and AI agents using the NeuroGlyph protocol.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API account (for GPT access)
- Anthropic API account (for Claude access)
- Microphone and speakers (optional, for voice features)

### Installation

1. **Clone or Download the Platform Code**
   ```bash
   # Save the neuroglyph_platform.py code to your local machine
   # You can copy it from the provided artifact
   ```

2. **Install Required Dependencies**
   ```bash
   pip install openai anthropic speechrecognition pyttsx3 pyaudio pyyaml
   ```

   **Note for macOS users:**
   ```bash
   brew install portaudio  # Required for pyaudio
   pip install pyaudio
   ```

   **Note for Linux users:**
   ```bash
   sudo apt-get install portaudio19-dev python3-pyaudio  # Ubuntu/Debian
   # or
   sudo yum install portaudio-devel  # CentOS/RHEL
   ```

3. **Set Up Configuration File**
   
   Create a `config.yaml` file in the same directory as the platform:
   ```yaml
   openai_api_key: "sk-your-openai-key-here"
   anthropic_api_key: "sk-ant-api-your-anthropic-key-here"
   default_participants: ["Human", "GPT-4", "Claude"]
   voice_enabled: true
   auto_save: true
   ```

### Getting API Keys

#### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign in to your OpenAI account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)

#### Anthropic API Key  
1. Go to https://console.anthropic.com/
2. Sign in with your Claude account credentials
3. Navigate to "API Keys" section
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-api-...`)

## 🎯 Running the Platform

### Basic Launch
```bash
python neuroglyph_platform.py
```

The platform will prompt you to:
1. Enter a conversation topic
2. Specify context (optional)
3. Define intent (optional)

### Example Startup Session
```
🧠 NeuroGlyph Multi-Agent Platform
========================================
📚 Conversation topic: artificial consciousness
🎯 Context (optional): philosophical exploration
💡 Intent (optional): understanding AI awareness

🚀 Initializing NeuroGlyph conversation...
============================================================
NEUROGLYPH CONVERSATION PLATFORM
============================================================
📚 Focus: artificial consciousness
👥 Participants: Human, GPT-4, Claude
🎯 Context: philosophical exploration
============================================================
```

## 📝 Using NeuroGlyph Protocol

### Basic Message Structure
Every message should include appropriate NeuroGlyph tokens:

```
🧠: Human
📚: consciousness_and_understanding
💡: exploring_the_nature_of_AI_awareness
🎯: philosophical_dialogue
📦: insights_and_questions
❓: Can AI agents truly understand or merely simulate understanding?
```

### Core Tokens Reference

| Emoji | Slash | Meaning |
|-------|-------|---------|
| 🧠 | /mind | Participants in dialogue |
| 📚 | /focus | Main topic or concept |
| 💡 | /intent | Underlying purpose |
| 🎯 | /context | Situation or frame |
| 📦 | /deliverable | Expected output |
| ❓ | /query | Open-ended question |
| 🚀 | /act | Action or performative |
| ⏰ | /timeline | Deadline or period |
| 🔥 | /pulse | Priority or urgency |

### Message Examples

**Simple Query:**
```
🧠: Human
📚: category_theory_in_programming
❓: How do functors in Haskell relate to mathematical category theory?
📦: clear_explanation
```

**Complex Discussion Starter:**
```
🧠: Human
📚: hermeneutic_communication_theory
🎯: academic_research_collaboration
💡: exploring_interpretation_in_human_AI_dialogue
📦: research_insights
⏰: ongoing_project
🤝: high_trust_academic_collaboration
❓: How does Gadamer's fusion of horizons apply to human-AI communication?
```

## 🎮 Platform Commands

### During Conversation
- `voice` - Switch to voice input mode
- `text` - Switch to text input mode
- `gpt` - Request response from GPT-4 only
- `claude` - Request response from Claude only
- `both` - Get responses from both AI agents
- `save` - Save current conversation
- `quit` - Exit the platform

### Auto-Response Triggers
Messages containing these tokens will automatically prompt AI responses:
- `/echo` - Ask AI agents to repeat or clarify
- `/query` - Open-ended question for AI agents

## 🗣️ Voice Features

### Voice Input
1. Type `voice` to switch to voice mode
2. Speak when prompted with "🎤 Listening..."
3. The system will transcribe and process your speech

### Voice Output
- AI responses are automatically spoken when in voice mode
- Text-to-speech reads the main content, skipping meta-tokens

### Troubleshooting Voice
- **No microphone detected**: Check system permissions and microphone connection
- **Recognition errors**: Speak clearly and reduce background noise
- **TTS not working**: Verify system audio output and pyttsx3 installation

## 📁 Conversation Management

### Auto-Save
Conversations are automatically saved when:
- You type `quit` to exit
- Auto-save is enabled in config (default: true)

### Manual Save
Type `save` during conversation to create an immediate backup.

### File Format
Saved conversations are JSON files with structure:
```json
{
  "conversation_id": "20240815_143022",
  "active_context": {
    "/mind": "Human, GPT-4, Claude",
    "/focus": "artificial consciousness"
  },
  "messages": [...]
}
```

## 🧪 Experiment Ideas

### 1. Philosophical Dialogue
```
Topic: "consciousness and understanding"
Context: "philosophical exploration of AI awareness"
Intent: "determine if AI can truly understand vs simulate"

Try asking:
❓: What distinguishes genuine understanding from sophisticated pattern matching?
```

### 2. Creative Collaboration
```
Topic: "collaborative storytelling"
Context: "creative writing session"  
Intent: "co-create narrative with AI agents"

Use tokens like:
🎨: narrative_theme
🎭: character_development
🌱: story_seed
```

### 3. Technical Problem Solving
```
Topic: "Python category theory library design"
Context: "software architecture planning"
Intent: "design robust mathematical computing library"

Include:
🏗️: technical_architecture
📊: success_metrics
⚡: implementation_triggers
```

### 4. Research Planning
```
Topic: "hermeneutic AI communication research"
Context: "academic paper development"
Intent: "structure research methodology"

Focus on:
📖: literature_review
🌉: theoretical_bridges
🔍: research_questions
```

## 🔧 Troubleshooting

### Common Issues

**API Key Errors:**
- Verify keys are correctly formatted in `config.yaml`
- Check API key permissions and billing status
- Ensure no extra spaces or quotes around keys

**Import Errors:**
```bash
# Try installing dependencies individually
pip install --upgrade openai
pip install --upgrade anthropic
pip install speechrecognition
pip install pyttsx3
pip install PyAudio
pip install pyyaml
```

**Voice Recognition Issues:**
- Check microphone permissions in system settings
- Test microphone with other applications
- Reduce background noise
- Speak clearly and at moderate pace

**Conversation Not Saving:**
- Check write permissions in current directory
- Verify `auto_save: true` in config.yaml
- Try manual save with `save` command

### Performance Tips

**For Better AI Responses:**
- Provide clear context and intent
- Use specific NeuroGlyph tokens
- Keep individual messages focused
- Reference previous conversation elements

**For Smoother Voice Interaction:**
- Use a quality microphone
- Minimize background noise
- Speak at consistent volume
- Pause briefly between tokens and content

## 📚 Advanced Usage

### Custom Token Extensions
You can extend the token vocabulary by modifying the `CORE_TOKENS` dictionary in the code:

```python
CORE_TOKENS.update({
    '🔬': '/experiment',
    '📐': '/mathematical_proof',
    '🎼': '/composition'
})
```

### Conversation Templates
Create reusable conversation starters:

```python
# Add to your config.yaml
conversation_templates:
  philosophy:
    context: "philosophical exploration"
    intent: "deepen understanding through dialogue"
    participants: ["Human", "GPT-4", "Claude"]
  
  research:
    context: "academic research collaboration"
    intent: "generate new insights and methodologies"
    participants: ["Human", "Claude", "Domain_Expert"]
```

### Integration with Other Tools
The platform can be extended to integrate with:
- Jupyter notebooks for research documentation
- Git repositories for version-controlled conversations
- Academic databases for reference integration
- Visualization tools for conversation analysis

## 🤝 Contributing & Extending

The platform is designed to be extensible. Key areas for enhancement:

1. **Protocol Extensions**: Add domain-specific NeuroGlyph tokens
2. **Agent Integration**: Connect additional AI models or human experts
3. **Visualization**: Create conversation flow diagrams
4. **Analysis Tools**: Build conversation pattern analysis
5. **Export Formats**: Support for academic paper generation

## 📞 Support

For issues or questions:
1. Check this documentation first
2. Verify your configuration setup
3. Test with simple conversations before complex ones
4. Review the console output for error messages

The platform is experimental but designed to provide a solid foundation for exploring structured human-AI dialogue using the NeuroGlyph protocol.

---

**Happy experimenting with NeuroGlyph! 🧠✨**