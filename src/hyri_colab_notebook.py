# HyRI - Hybrid Relational Intelligence
# Simple NeuroGlyph Demo for Google Colab
# =====================================

# Install required packages
!pip install openai anthropic ipywidgets

import re
import json
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

# Configuration
print("🧠 HyRI - Hybrid Relational Intelligence")
print("=" * 50)
print("Simple NeuroGlyph Demo for Google Colab")
print("=" * 50)

class AgentType(Enum):
    HUMAN = "human"
    GPT = "gpt"
    CLAUDE = "claude"

@dataclass
class NeuroGlyphMessage:
    """Represents a parsed NeuroGlyph message"""
    timestamp: str
    agent: str
    agent_type: AgentType
    tokens: Dict[str, Any]
    raw_text: str
    is_valid: bool = True
    validation_errors: List[str] = None

    def __post_init__(self):
        if self.validation_errors is None:
            self.validation_errors = []

class NeuroGlyphParser:
    """Simple NeuroGlyph parser for Colab"""
    
    # Core tokens (simplified for demo)
    CORE_TOKENS = {
        '🧠': '/mind', '📚': '/focus', '🎯': '/context', '💡': '/intent',
        '📦': '/deliverable', '❓': '/query', '🚀': '/act', '⏰': '/timeline',
        '🔥': '/pulse', '🤝': '/trust', '📝': '/note', '🔍': '/introspect'
    }
    
    SLASH_TO_EMOJI = {v: k for k, v in CORE_TOKENS.items()}
    
    def parse_message(self, text: str, agent: str, agent_type: AgentType) -> NeuroGlyphMessage:
        """Parse a NeuroGlyph message and extract tokens"""
        tokens = {}
        validation_errors = []
        
        lines = text.strip().split('\n')
        for line in lines:
            if ':' in line:
                token_part, value = line.split(':', 1)
                token_part = token_part.strip()
                value = value.strip()
                
                # Convert emoji to slash notation if needed
                token = self.CORE_TOKENS.get(token_part, token_part)
                tokens[token] = value
        
        # Simple validation
        is_valid = True
        if '/act' in tokens and '/intent' not in tokens:
            validation_errors.append("Action requires /intent")
            is_valid = False
        
        return NeuroGlyphMessage(
            timestamp=datetime.datetime.now().isoformat(),
            agent=agent,
            agent_type=agent_type,
            tokens=tokens,
            raw_text=text,
            is_valid=is_valid,
            validation_errors=validation_errors
        )
    
    def format_tokens(self, tokens: Dict[str, Any]) -> str:
        """Format tokens back to NeuroGlyph"""
        lines = []
        for token, value in tokens.items():
            emoji = self.SLASH_TO_EMOJI.get(token, token)
            lines.append(f"{emoji}: {value}")
        return '\n'.join(lines)

class SimpleHyRI:
    """Simplified HyRI engine for Colab demo"""
    
    def __init__(self):
        self.parser = NeuroGlyphParser()
        self.conversation_history = []
        self.openai_client = None
        self.anthropic_client = None
    
    def set_api_keys(self, openai_key: str = "", anthropic_key: str = ""):
        """Set API keys for AI services"""
        if openai_key:
            import openai
            self.openai_client = openai.OpenAI(api_key=openai_key)
            print("✅ OpenAI client initialized")
        
        if anthropic_key:
            import anthropic
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
            print("✅ Anthropic client initialized")
    
    def add_message(self, text: str, agent: str, agent_type: AgentType):
        """Add a message to conversation"""
        message = self.parser.parse_message(text, agent, agent_type)
        self.conversation_history.append(message)
        
        # Display the message
        self.display_message(message)
        
        return message
    
    def display_message(self, message: NeuroGlyphMessage):
        """Display a message in Colab"""
        agent_emoji = {"human": "👤", "gpt": "🤖", "claude": "🎭"}.get(message.agent_type.value, "⚙️")
        
        html = f"""
        <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 5px; background-color: #f9f9f9;">
            <div style="font-weight: bold; color: #333;">
                {agent_emoji} {message.agent} <span style="font-size: 0.8em; color: #666;">({message.timestamp.split('T')[1][:8]})</span>
            </div>
            <div style="margin-top: 5px; font-family: monospace; white-space: pre-line;">
{message.raw_text}
            </div>
            {f'<div style="color: orange; font-size: 0.9em;">⚠️ {", ".join(message.validation_errors)}</div>' if not message.is_valid else ''}
        </div>
        """
        display(HTML(html))
    
    def get_conversation_context(self) -> str:
        """Build context for AI agents"""
        context = [
            "You are participating in a NeuroGlyph conversation.",
            "NeuroGlyph is a structured protocol for human-AI dialogue.",
            "Please respond using NeuroGlyph tokens like 🧠: agent_name, 📚: topic, 💡: intent, etc.",
            "Recent conversation:"
        ]
        
        for msg in self.conversation_history[-3:]:
            context.append(f"[{msg.agent}]: {msg.raw_text}")
        
        return '\n'.join(context)
    
    def get_gpt_response(self, prompt: str = "") -> str:
        """Get GPT response"""
        if not self.openai_client:
            return "❌ OpenAI client not configured"
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.get_conversation_context()},
                    {"role": "user", "content": prompt or "Continue the NeuroGlyph conversation"}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ GPT Error: {str(e)}"
    
    def get_claude_response(self, prompt: str = "") -> str:
        """Get Claude response"""
        if not self.anthropic_client:
            return "❌ Anthropic client not configured"
        
        try:
            message = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=300,
                messages=[{
                    "role": "user", 
                    "content": f"{self.get_conversation_context()}\n\nHuman: {prompt or 'Continue the conversation'}"
                }]
            )
            return message.content[0].text
        except Exception as e:
            return f"❌ Claude Error: {str(e)}"
    
    def export_conversation(self) -> str:
        """Export conversation as JSON"""
        data = {
            'conversation_id': datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            'messages': [asdict(msg) for msg in self.conversation_history]
        }
        return json.dumps(data, indent=2, ensure_ascii=False)

# Initialize HyRI
hyri = SimpleHyRI()

# Setup UI
print("\n🔧 Setup")
print("Enter your API keys below (at least one required):")

# API Key input
openai_key_widget = widgets.Password(
    placeholder="sk-...",
    description="OpenAI Key:",
    style={'description_width': 'initial'}
)

anthropic_key_widget = widgets.Password(
    placeholder="sk-ant-api-...", 
    description="Anthropic Key:",
    style={'description_width': 'initial'}
)

setup_button = widgets.Button(
    description="Initialize HyRI",
    button_style='success'
)

def setup_hyri(b):
    with setup_output:
        clear_output()
        hyri.set_api_keys(openai_key_widget.value, anthropic_key_widget.value)
        if hyri.openai_client or hyri.anthropic_client:
            print("🚀 HyRI is ready! Start your NeuroGlyph conversation below.")
        else:
            print("❌ Please provide at least one API key")

setup_button.on_click(setup_hyri)
setup_output = widgets.Output()

display(openai_key_widget, anthropic_key_widget, setup_button, setup_output)

print("\n💬 Conversation Interface")
print("Use NeuroGlyph tokens in your messages:")

# Message input
message_widget = widgets.Textarea(
    placeholder="""🧠: Human
📚: artificial_consciousness
💡: exploring_AI_awareness
🎯: philosophical_dialogue
📦: insights_and_questions
❓: Can AI agents truly understand or just simulate understanding?""",
    layout=widgets.Layout(width='100%', height='120px'),
    description="Your Message:"
)

# Buttons
send_button = widgets.Button(description="📤 Send", button_style='primary')
gpt_button = widgets.Button(description="🤖 Get GPT Response", button_style='info')
claude_button = widgets.Button(description="🎭 Get Claude Response", button_style='info')
both_button = widgets.Button(description="🔄 Both Agents", button_style='warning')

# Button functions
def send_message(b):
    if message_widget.value.strip():
        hyri.add_message(message_widget.value, "Human", AgentType.HUMAN)
        message_widget.value = ""

def get_gpt_response(b):
    response = hyri.get_gpt_response()
    hyri.add_message(response, "GPT-4", AgentType.GPT)

def get_claude_response(b):
    response = hyri.get_claude_response()
    hyri.add_message(response, "Claude", AgentType.CLAUDE)

def get_both_responses(b):
    if hyri.openai_client:
        gpt_response = hyri.get_gpt_response()
        hyri.add_message(gpt_response, "GPT-4", AgentType.GPT)
    
    if hyri.anthropic_client:
        claude_response = hyri.get_claude_response()
        hyri.add_message(claude_response, "Claude", AgentType.CLAUDE)

send_button.on_click(send_message)
gpt_button.on_click(get_gpt_response)
claude_button.on_click(get_claude_response)
both_button.on_click(get_both_responses)

button_box = widgets.HBox([send_button, gpt_button, claude_button, both_button])
display(message_widget, button_box)

print("\n📖 NeuroGlyph Token Reference:")
print("🧠 /mind: Participants    💡 /intent: Purpose")
print("📚 /focus: Topic          📦 /deliverable: Output") 
print("🎯 /context: Situation    ❓ /query: Question")
print("🚀 /act: Action           ⏰ /timeline: Time")
print("🔥 /pulse: Priority       🤝 /trust: Trust level")

print("\n✨ Example Templates:")

example1 = widgets.Button(description="📚 Philosophy Question", button_style='')
example2 = widgets.Button(description="🚀 Project Planning", button_style='')
example3 = widgets.Button(description="🔍 Research Query", button_style='')

def load_example1(b):
    message_widget.value = """🧠: Human
📚: consciousness_and_AI
💡: exploring_philosophical_implications
🎯: academic_dialogue
📦: theoretical_insights
❓: What distinguishes genuine understanding from sophisticated pattern matching in AI systems?"""

def load_example2(b):
    message_widget.value = """🧠: Human
🚀: design_category_theory_library
💡: create_mathematical_computing_toolkit
🎯: software_development_project
📦: python_library_with_documentation
⏰: 8_weeks_development_timeline"""

def load_example3(b):
    message_widget.value = """🧠: Human
🔍: analyze_human_AI_collaboration_patterns
💡: understanding_effective_partnership_dynamics
🎯: research_investigation
📦: structured_findings_and_recommendations"""

example1.on_click(load_example1)
example2.on_click(load_example2)
example3.on_click(load_example3)

example_box = widgets.HBox([example1, example2, example3])
display(example_box)

# Export functionality
print("\n💾 Export Conversation")
export_button = widgets.Button(description="📄 Export as JSON", button_style='success')
export_output = widgets.Output()

def export_conversation(b):
    with export_output:
        clear_output()
        if hyri.conversation_history:
            json_data = hyri.export_conversation()
            print("📄 Conversation Export:")
            print("=" * 40)
            print(json_data)
        else:
            print("No conversation to export yet.")

export_button.on_click(export_conversation)
display(export_button, export_output)

print("\n🎯 Instructions:")
print("1. Set your API keys above")
print("2. Click 'Initialize HyRI'") 
print("3. Type a NeuroGlyph message or use an example template")
print("4. Send your message and get AI responses")
print("5. Export your conversation when done")
print("\nEnjoy exploring Hybrid Relational Intelligence! 🧠✨")