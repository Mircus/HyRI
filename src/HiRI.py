#!/usr/bin/env python3
"""
NeuroGlyph Multi-Agent Conversation Platform
=============================================

A platform for structured dialogue between humans and AI agents using the NeuroGlyph protocol.
Supports text and voice input, protocol validation, and conversation archiving.
"""

import asyncio
import json
import re
import datetime
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict
from enum import Enum
import speech_recognition as sr
import pyttsx3
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import yaml

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
    """Parses and validates NeuroGlyph protocol messages"""
    
    # Core NeuroGlyph tokens mapping
    CORE_TOKENS = {
        # Core tokens
        '🚀': '/act', '📚': '/focus', '🧠': '/mind', '🎯': '/context',
        '💡': '/intent', '📦': '/deliverable', '⏰': '/timeline', 
        '🔥': '/pulse', '🏔️': '/gliph', '🔗': '/relation', '🌐': '/network',
        '🔄': '/compose', '🔍': '/zoom', '🎛️': '/switch_context', 
        '⛓️': '/chain', '📢': '/echo', '🔧': '/resolve', '📝': '/note',
        '📊': '/metric', '📡': '/channel', '👥': '/collective', '🎭': '/role',
        
        # Extended tokens
        '🏛️': '/govern', '📋': '/norm', '💰': '/resource', '🤝': '/trust',
        '🎯': '/goal', '⚡': '/trigger', '🎨': '/palette', '👤': '/character',
        '🌍': '/setting', '📖': '/lore', '🎲': '/turn', '🌱': '/seed',
        '🎵': '/motif', '🏗️': '/structure', '👁️': '/pov', '✨': '/flourish',
        
        # Research & meta tokens
        '❓': '/query', '🔄': '/ongoing', '🌉': '/bridge', '⚖️': '/dialectic',
        '🧠🧠': '/meta', '📄': '/source', '🔄': '/transform', '🔍': '/introspect'
    }
    
    # Reverse mapping for emoji to slash conversion
    SLASH_TO_EMOJI = {v: k for k, v in CORE_TOKENS.items()}
    
    def __init__(self):
        self.token_pattern = re.compile(r'([🚀📚🧠🎯💡📦⏰🔥🏔️🔗🌐🔄🔍🎛️⛓️📢🔧📝📊📡👥🎭🏛️📋💰🤝⚡🎨👤🌍📖🎲🌱🎵🏗️👁️✨❓🌉⚖️📄]|/\w+):\s*(.+?)(?=\n[🚀📚🧠🎯💡📦⏰🔥🏔️🔗🌐🔄🔍🎛️⛓️📢🔧📝📊📡👥🎭🏛️📋💰🤝⚡🎨👤🌍📖🎲🌱🎵🏗️👁️✨❓🌉⚖️📄]|/\w+:|$)', re.DOTALL | re.MULTILINE)
    
    def parse_message(self, text: str, agent: str, agent_type: AgentType) -> NeuroGlyphMessage:
        """Parse a NeuroGlyph message and extract tokens"""
        tokens = {}
        validation_errors = []
        
        # Extract tokens using regex
        matches = self.token_pattern.findall(text)
        
        for token_raw, value in matches:
            # Convert emoji to slash notation if needed
            token = self.CORE_TOKENS.get(token_raw, token_raw)
            tokens[token] = value.strip()
        
        # Validation
        is_valid = self.validate_message(tokens, validation_errors)
        
        return NeuroGlyphMessage(
            timestamp=datetime.datetime.now().isoformat(),
            agent=agent,
            agent_type=agent_type,
            tokens=tokens,
            raw_text=text,
            is_valid=is_valid,
            validation_errors=validation_errors
        )
    
    def validate_message(self, tokens: Dict[str, Any], errors: List[str]) -> bool:
        """Validate NeuroGlyph message structure"""
        is_valid = True
        
        # Check required tokens for actions
        if '/act' in tokens:
            if '/intent' not in tokens:
                errors.append("Action requires /intent declaration")
                is_valid = False
            if '/context' not in tokens:
                errors.append("Action requires /context declaration")
                is_valid = False
        
        # Check for deliverable expectations
        if any(token in tokens for token in ['/act', '/query', '/resolve']):
            if '/deliverable' not in tokens:
                errors.append("Interactive tokens should specify expected /deliverable")
        
        return is_valid
    
    def format_message(self, tokens: Dict[str, Any], use_emojis: bool = True) -> str:
        """Format tokens back into NeuroGlyph message"""
        lines = []
        for token, value in tokens.items():
            if use_emojis and token in self.SLASH_TO_EMOJI:
                display_token = self.SLASH_TO_EMOJI[token]
            else:
                display_token = token
            lines.append(f"{display_token}: {value}")
        return "\n".join(lines)

class ConversationEngine:
    """Manages multi-agent NeuroGlyph conversations"""
    
    def __init__(self, openai_key: str, anthropic_key: str):
        self.openai_client = AsyncOpenAI(api_key=openai_key)
        self.anthropic_client = AsyncAnthropic(api_key=anthropic_key)
        self.parser = NeuroGlyphParser()
        self.conversation_history: List[NeuroGlyphMessage] = []
        self.active_context = {}
        
        # Voice setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Adjust recognition settings
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    async def initialize_conversation(self, topic: str, participants: List[str], 
                                    context: str = "", intent: str = "") -> NeuroGlyphMessage:
        """Initialize a NeuroGlyph conversation with proper setup"""
        
        init_tokens = {
            '/mind': ', '.join(participants),
            '/focus': topic,
            '/context': context or f"Multi-agent dialogue on {topic}",
            '/intent': intent or "Collaborative exploration and understanding",
            '/deliverable': "structured_dialogue",
            '/timeline': "ongoing",
            '/channel': "text_and_voice",
            '/norm': "respectful_dialogue, ng_protocol_adherence",
            '/govern': "consensus_seeking"
        }
        
        init_message = NeuroGlyphMessage(
            timestamp=datetime.datetime.now().isoformat(),
            agent="system",
            agent_type=AgentType.HUMAN,  # System as human-initiated
            tokens=init_tokens,
            raw_text=self.parser.format_message(init_tokens)
        )
        
        self.conversation_history.append(init_message)
        self.active_context = init_tokens.copy()
        
        return init_message
    
    def get_conversation_context(self) -> str:
        """Build context string for AI agents"""
        context_parts = [
            "You are participating in a NeuroGlyph conversation. ",
            "NeuroGlyph is a structured protocol for human-AI dialogue.",
            f"Active context: {self.active_context.get('/context', 'General dialogue')}",
            f"Current focus: {self.active_context.get('/focus', 'Open discussion')}",
            f"Participants: {self.active_context.get('/mind', 'Unknown')}",
            "",
            "Recent conversation history:"
        ]
        
        # Add last 3 messages for context
        for msg in self.conversation_history[-3:]:
            context_parts.append(f"[{msg.agent}]: {msg.raw_text}")
        
        context_parts.extend([
            "",
            "Please respond using NeuroGlyph protocol. Include appropriate tokens like:",
            "/mind: your_agent_name",
            "/focus: main_topic_or_concept", 
            "/intent: your_purpose_in_responding",
            "/deliverable: what_you_aim_to_provide",
            "And your actual response content.",
            "",
            "Be conversational but maintain the structured format."
        ])
        
        return "\n".join(context_parts)
    
    async def get_gpt_response(self, prompt: str) -> str:
        """Get response from GPT using NeuroGlyph context"""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.get_conversation_context()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"GPT Error: {str(e)}"
    
    async def get_claude_response(self, prompt: str) -> str:
        """Get response from Claude using NeuroGlyph context"""
        try:
            message = await self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                messages=[
                    {
                        "role": "user", 
                        "content": f"{self.get_conversation_context()}\n\nHuman message: {prompt}"
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Claude Error: {str(e)}"
    
    def listen_for_speech(self) -> Optional[str]:
        """Capture speech input from microphone"""
        try:
            print("🎤 Listening... (speak now)")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=30)
            
            print("🔄 Processing speech...")
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            print("⏰ No speech detected")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
    
    def speak_text(self, text: str):
        """Convert text to speech"""
        try:
            # Extract main content from NG message for speaking
            content_parts = []
            for line in text.split('\n'):
                if ':' in line:
                    token, value = line.split(':', 1)
                    # Skip meta tokens, speak main content
                    if token.strip() not in ['/mind', '/context', '/intent', '/deliverable', 
                                           '/timeline', '/channel', '/norm', '/govern']:
                        content_parts.append(value.strip())
                else:
                    content_parts.append(line)
            
            speech_text = ' '.join(content_parts).strip()
            if speech_text:
                self.tts_engine.say(speech_text)
                self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    async def add_message(self, text: str, agent: str, agent_type: AgentType) -> NeuroGlyphMessage:
        """Add a message to the conversation"""
        message = self.parser.parse_message(text, agent, agent_type)
        self.conversation_history.append(message)
        
        # Update active context with new information
        if '/context' in message.tokens:
            self.active_context['/context'] = message.tokens['/context']
        if '/focus' in message.tokens:
            self.active_context['/focus'] = message.tokens['/focus']
        
        return message
    
    async def process_agent_turn(self, agent_type: AgentType, prompt: str = "") -> NeuroGlyphMessage:
        """Process a turn for an AI agent"""
        if agent_type == AgentType.GPT:
            response = await self.get_gpt_response(prompt)
            agent_name = "GPT-4"
        elif agent_type == AgentType.CLAUDE:
            response = await self.get_claude_response(prompt)
            agent_name = "Claude"
        else:
            raise ValueError(f"Invalid agent type for processing: {agent_type}")
        
        return await self.add_message(response, agent_name, agent_type)
    
    def save_conversation(self, filename: str):
        """Save conversation history to file"""
        data = {
            'conversation_id': datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            'active_context': self.active_context,
            'messages': [asdict(msg) for msg in self.conversation_history]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_conversation(self, filename: str):
        """Load conversation history from file"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.active_context = data['active_context']
        self.conversation_history = [
            NeuroGlyphMessage(**msg_data) for msg_data in data['messages']
        ]

class NeuroGlyphPlatform:
    """Main platform interface for NeuroGlyph conversations"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.load_config(config_file)
        self.engine = ConversationEngine(
            self.config['openai_api_key'],
            self.config['anthropic_api_key']
        )
    
    def load_config(self, config_file: str):
        """Load configuration from YAML file"""
        try:
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            # Create default config
            self.config = {
                'openai_api_key': 'your_openai_key_here',
                'anthropic_api_key': 'your_anthropic_key_here',
                'default_participants': ['Human', 'GPT-4', 'Claude'],
                'voice_enabled': True,
                'auto_save': True
            }
            with open(config_file, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            print(f"Created default config file: {config_file}")
            print("Please add your API keys to the config file.")
    
    async def start_conversation(self, topic: str, participants: List[str] = None, 
                               context: str = "", intent: str = ""):
        """Start a new NeuroGlyph conversation"""
        if participants is None:
            participants = self.config.get('default_participants', ['Human', 'GPT-4', 'Claude'])
        
        print("🚀 Initializing NeuroGlyph conversation...")
        init_msg = await self.engine.initialize_conversation(topic, participants, context, intent)
        
        print("\n" + "="*60)
        print("NEUROGLYPH CONVERSATION PLATFORM")
        print("="*60)
        print(f"📚 Focus: {topic}")
        print(f"👥 Participants: {', '.join(participants)}")
        print(f"🎯 Context: {context or 'General dialogue'}")
        print("="*60 + "\n")
        
        return init_msg
    
    async def conversation_loop(self):
        """Main conversation loop with human input and AI responses"""
        print("\nConversation Commands:")
        print("  'voice' - Switch to voice input")
        print("  'text' - Switch to text input") 
        print("  'gpt' - Get GPT response")
        print("  'claude' - Get Claude response")
        print("  'both' - Get both AI responses")
        print("  'save' - Save conversation")
        print("  'quit' - Exit conversation")
        print("  Or type your NeuroGlyph message directly\n")
        
        input_mode = "text"
        
        while True:
            try:
                # Get human input
                if input_mode == "voice":
                    user_input = self.engine.listen_for_speech()
                    if user_input is None:
                        continue
                    print(f"🗣️ You said: {user_input}")
                else:
                    user_input = input("\n💬 Your message (or command): ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'voice':
                    input_mode = "voice"
                    print("🎤 Switched to voice input")
                    continue
                elif user_input.lower() == 'text':
                    input_mode = "text"
                    print("⌨️ Switched to text input")
                    continue
                elif user_input.lower() == 'save':
                    filename = f"ng_conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    self.engine.save_conversation(filename)
                    print(f"💾 Conversation saved to {filename}")
                    continue
                elif user_input.lower() in ['gpt', 'claude', 'both']:
                    # Direct AI response request
                    if user_input.lower() in ['gpt', 'both']:
                        print("\n🤖 GPT-4 responding...")
                        gpt_msg = await self.engine.process_agent_turn(AgentType.GPT)
                        print(f"[GPT-4]: {gpt_msg.raw_text}")
                        if self.config.get('voice_enabled') and input_mode == "voice":
                            self.engine.speak_text(gpt_msg.raw_text)
                    
                    if user_input.lower() in ['claude', 'both']:
                        print("\n🎭 Claude responding...")
                        claude_msg = await self.engine.process_agent_turn(AgentType.CLAUDE)
                        print(f"[Claude]: {claude_msg.raw_text}")
                        if self.config.get('voice_enabled') and input_mode == "voice":
                            self.engine.speak_text(claude_msg.raw_text)
                    continue
                
                # Process as regular NeuroGlyph message
                human_msg = await self.engine.add_message(user_input, "Human", AgentType.HUMAN)
                
                # Show validation results
                if not human_msg.is_valid:
                    print(f"⚠️ Validation warnings: {', '.join(human_msg.validation_errors)}")
                
                print(f"\n[You]: {human_msg.raw_text}")
                
                # Auto-respond with AI agents if requested
                if '/echo' in human_msg.tokens or '/query' in human_msg.tokens:
                    print("\n🤖 Auto-responding with AI agents...")
                    
                    gpt_msg = await self.engine.process_agent_turn(AgentType.GPT, user_input)
                    print(f"\n[GPT-4]: {gpt_msg.raw_text}")
                    
                    claude_msg = await self.engine.process_agent_turn(AgentType.CLAUDE, user_input)
                    print(f"\n[Claude]: {claude_msg.raw_text}")
                    
                    if self.config.get('voice_enabled') and input_mode == "voice":
                        self.engine.speak_text(gpt_msg.raw_text)
                        self.engine.speak_text(claude_msg.raw_text)
            
            except KeyboardInterrupt:
                print("\n\n👋 Conversation interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                continue
        
        # Auto-save if enabled
        if self.config.get('auto_save', True):
            filename = f"ng_conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            self.engine.save_conversation(filename)
            print(f"💾 Conversation auto-saved to {filename}")

async def main():
    """Main entry point"""
    platform = NeuroGlyphPlatform()
    
    print("🧠 NeuroGlyph Multi-Agent Platform")
    print("=" * 40)
    
    # Get conversation setup
    topic = input("📚 Conversation topic: ").strip()
    if not topic:
        topic = "Open dialogue"
    
    context = input("🎯 Context (optional): ").strip()
    intent = input("💡 Intent (optional): ").strip()
    
    # Start conversation
    await platform.start_conversation(topic, context=context, intent=intent)
    
    # Enter main loop
    await platform.conversation_loop()
    
    print("\n🎯 Thanks for using NeuroGlyph! Conversation ended.")

if __name__ == "__main__":
    asyncio.run(main())

# Example usage:
"""
# Create config.yaml with your API keys:
openai_api_key: "your_openai_key_here"
anthropic_api_key: "your_anthropic_key_here"  
voice_enabled: true
auto_save: true

# Run the platform:
python neuroglyph_platform.py

# Example NeuroGlyph messages you might send:
🧠: Human
📚: artificial consciousness  
💡: exploring the nature of AI awareness
🎯: philosophical dialogue
📦: insights_and_questions
❓: Can AI agents truly understand or merely simulate understanding?

# The system will validate your messages and facilitate multi-agent dialogue
"""
