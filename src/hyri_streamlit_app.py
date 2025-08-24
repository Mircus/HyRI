#!/usr/bin/env python3
"""
HyRI Streamlit Web Application
==============================

A web interface for the Hybrid Relational Intelligence platform,
enabling structured dialogue between humans and AI agents using NeuroGlyph protocol.
"""

import streamlit as st
import asyncio
import json
import datetime
import re
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict
from enum import Enum
import openai
import anthropic
import pandas as pd
from io import StringIO

# Set page config
st.set_page_config(
    page_title="HyRI - Hybrid Relational Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

class HyRIEngine:
    """Core HyRI conversation engine for Streamlit"""
    
    def __init__(self):
        self.parser = NeuroGlyphParser()
        self.conversation_history: List[NeuroGlyphMessage] = []
        self.active_context = {}
        
        # Initialize API clients
        self.openai_client = None
        self.anthropic_client = None
    
    def initialize_clients(self, openai_key: str, anthropic_key: str):
        """Initialize API clients with provided keys"""
        if openai_key:
            self.openai_client = openai.OpenAI(api_key=openai_key)
        if anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
    
    def initialize_conversation(self, topic: str, participants: List[str], 
                              context: str = "", intent: str = "") -> NeuroGlyphMessage:
        """Initialize a NeuroGlyph conversation with proper setup"""
        
        init_tokens = {
            '/mind': ', '.join(participants),
            '/focus': topic,
            '/context': context or f"Structured dialogue on {topic}",
            '/intent': intent or "Collaborative exploration and understanding",
            '/deliverable': "structured_dialogue",
            '/timeline': "ongoing",
            '/channel': "web_interface",
            '/norm': "respectful_dialogue, ng_protocol_adherence",
            '/govern': "consensus_seeking"
        }
        
        init_message = NeuroGlyphMessage(
            timestamp=datetime.datetime.now().isoformat(),
            agent="system",
            agent_type=AgentType.HUMAN,
            tokens=init_tokens,
            raw_text=self.parser.format_message(init_tokens)
        )
        
        self.conversation_history.append(init_message)
        self.active_context = init_tokens.copy()
        
        return init_message
    
    def get_conversation_context(self) -> str:
        """Build context string for AI agents"""
        context_parts = [
            "You are participating in a NeuroGlyph conversation through the HyRI platform.",
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
            "Please respond using NeuroGlyph protocol with appropriate tokens.",
            "Be conversational but maintain the structured format.",
            "Include meaningful content beyond just the protocol structure."
        ])
        
        return "\n".join(context_parts)
    
    def get_gpt_response(self, prompt: str) -> str:
        """Get response from GPT using NeuroGlyph context"""
        if not self.openai_client:
            return "GPT Error: API client not initialized. Please check your OpenAI API key."
        
        try:
            response = self.openai_client.chat.completions.create(
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
    
    def get_claude_response(self, prompt: str) -> str:
        """Get response from Claude using NeuroGlyph context"""
        if not self.anthropic_client:
            return "Claude Error: API client not initialized. Please check your Anthropic API key."
        
        try:
            message = self.anthropic_client.messages.create(
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
    
    def add_message(self, text: str, agent: str, agent_type: AgentType) -> NeuroGlyphMessage:
        """Add a message to the conversation"""
        message = self.parser.parse_message(text, agent, agent_type)
        self.conversation_history.append(message)
        
        # Update active context with new information
        if '/context' in message.tokens:
            self.active_context['/context'] = message.tokens['/context']
        if '/focus' in message.tokens:
            self.active_context['/focus'] = message.tokens['/focus']
        
        return message

# Initialize session state
if 'hyri_engine' not in st.session_state:
    st.session_state.hyri_engine = HyRIEngine()
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False
if 'api_keys_set' not in st.session_state:
    st.session_state.api_keys_set = False

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🧠 HyRI - Hybrid Relational Intelligence")
    st.subtitle("Structured Dialogue Between Humans and AI Agents")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Keys
        st.subheader("API Keys")
        openai_key = st.text_input("OpenAI API Key", type="password", 
                                 help="Required for GPT-4 integration")
        anthropic_key = st.text_input("Anthropic API Key", type="password",
                                    help="Required for Claude integration")
        
        if st.button("Set API Keys"):
            if openai_key or anthropic_key:
                st.session_state.hyri_engine.initialize_clients(openai_key, anthropic_key)
                st.session_state.api_keys_set = True
                st.success("API keys configured!")
            else:
                st.error("Please provide at least one API key")
        
        # Conversation Setup
        st.subheader("Conversation Setup")
        
        if not st.session_state.conversation_started:
            topic = st.text_input("Topic", placeholder="e.g., artificial consciousness")
            context = st.text_area("Context", placeholder="e.g., philosophical exploration")
            intent = st.text_area("Intent", placeholder="e.g., exploring AI awareness")
            
            participants = st.multiselect(
                "Participants",
                ["Human", "GPT-4", "Claude"],
                default=["Human", "GPT-4", "Claude"]
            )
            
            if st.button("Start Conversation"):
                if topic and st.session_state.api_keys_set:
                    init_msg = st.session_state.hyri_engine.initialize_conversation(
                        topic, participants, context, intent
                    )
                    st.session_state.conversation_started = True
                    st.rerun()
                else:
                    st.error("Please provide a topic and set API keys first")
        else:
            st.success("✅ Conversation Active")
            if st.button("Reset Conversation"):
                st.session_state.hyri_engine = HyRIEngine()
                st.session_state.conversation_started = False
                st.rerun()
        
        # NeuroGlyph Reference
        st.subheader("📖 NeuroGlyph Tokens")
        with st.expander("Core Tokens"):
            st.code("""
🧠 /mind: Participants
📚 /focus: Topic/concept
🎯 /context: Situation
💡 /intent: Purpose
📦 /deliverable: Output
❓ /query: Question
🚀 /act: Action
⏰ /timeline: Time
🔥 /pulse: Priority
🤝 /trust: Trust level
            """)
    
    # Main conversation area
    if st.session_state.conversation_started:
        # Display conversation history
        st.header("💬 Conversation History")
        
        for msg in st.session_state.hyri_engine.conversation_history:
            with st.container():
                cols = st.columns([1, 8, 1])
                
                with cols[0]:
                    if msg.agent_type == AgentType.HUMAN:
                        st.markdown("👤")
                    elif msg.agent_type == AgentType.GPT:
                        st.markdown("🤖")
                    elif msg.agent_type == AgentType.CLAUDE:
                        st.markdown("🎭")
                    else:
                        st.markdown("⚙️")
                
                with cols[1]:
                    st.markdown(f"**{msg.agent}** *({msg.timestamp.split('T')[1][:8]})*")
                    
                    # Parse and display tokens nicely
                    if msg.tokens:
                        for token, value in msg.tokens.items():
                            emoji = st.session_state.hyri_engine.parser.SLASH_TO_EMOJI.get(token, token)
                            st.markdown(f"**{emoji}** {value}")
                    else:
                        st.markdown(msg.raw_text)
                    
                    if not msg.is_valid and msg.validation_errors:
                        st.warning(f"⚠️ Validation: {', '.join(msg.validation_errors)}")
                
                with cols[2]:
                    if st.button("📋", key=f"copy_{len(st.session_state.hyri_engine.conversation_history)}_{msg.timestamp}"):
                        st.code(msg.raw_text)
                
                st.divider()
        
        # Message input area
        st.header("✍️ Compose Message")
        
        # Quick compose templates
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📚 Ask Question"):
                st.session_state.message_template = """🧠: Human
📚: [your_topic]
❓: [your_question]
📦: insights_and_answers"""
        
        with col2:
            if st.button("🚀 Propose Action"):
                st.session_state.message_template = """🧠: Human
🚀: [action_to_take]
💡: [intent_behind_action]
🎯: [current_context]
📦: [expected_outcome]"""
        
        with col3:
            if st.button("🔄 Switch Context"):
                st.session_state.message_template = """🧠: Human
🎛️: [new_context]
📚: [new_focus]
💡: [reason_for_switch]"""
        
        # Message composition
        message_text = st.text_area(
            "Your NeuroGlyph Message",
            value=getattr(st.session_state, 'message_template', ''),
            height=150,
            help="Use NeuroGlyph tokens to structure your message"
        )
        
        # Control buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📤 Send Message") and message_text:
                # Add human message
                human_msg = st.session_state.hyri_engine.add_message(
                    message_text, "Human", AgentType.HUMAN
                )
                
                # Clear template
                if hasattr(st.session_state, 'message_template'):
                    del st.session_state.message_template
                
                st.rerun()
        
        with col2:
            if st.button("🤖 Get GPT Response") and st.session_state.hyri_engine.openai_client:
                with st.spinner("GPT-4 thinking..."):
                    gpt_response = st.session_state.hyri_engine.get_gpt_response(
                        message_text or "Continue the conversation"
                    )
                    gpt_msg = st.session_state.hyri_engine.add_message(
                        gpt_response, "GPT-4", AgentType.GPT
                    )
                st.rerun()
        
        with col3:
            if st.button("🎭 Get Claude Response") and st.session_state.hyri_engine.anthropic_client:
                with st.spinner("Claude thinking..."):
                    claude_response = st.session_state.hyri_engine.get_claude_response(
                        message_text or "Continue the conversation"
                    )
                    claude_msg = st.session_state.hyri_engine.add_message(
                        claude_response, "Claude", AgentType.CLAUDE
                    )
                st.rerun()
        
        with col4:
            if st.button("🔄 Both Agents"):
                if st.session_state.hyri_engine.openai_client:
                    with st.spinner("Getting responses..."):
                        gpt_response = st.session_state.hyri_engine.get_gpt_response(
                            message_text or "Continue the conversation"
                        )
                        st.session_state.hyri_engine.add_message(
                            gpt_response, "GPT-4", AgentType.GPT
                        )
                
                if st.session_state.hyri_engine.anthropic_client:
                    claude_response = st.session_state.hyri_engine.get_claude_response(
                        message_text or "Continue the conversation"
                    )
                    st.session_state.hyri_engine.add_message(
                        claude_response, "Claude", AgentType.CLAUDE
                    )
                
                st.rerun()
        
        # Analytics and Export
        if len(st.session_state.hyri_engine.conversation_history) > 1:
            st.header("📊 Conversation Analytics")
            
            # Basic stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Messages", len(st.session_state.hyri_engine.conversation_history))
            
            with col2:
                human_msgs = sum(1 for msg in st.session_state.hyri_engine.conversation_history 
                               if msg.agent_type == AgentType.HUMAN)
                st.metric("Human Messages", human_msgs)
            
            with col3:
                ai_msgs = len(st.session_state.hyri_engine.conversation_history) - human_msgs
                st.metric("AI Messages", ai_msgs)
            
            with col4:
                invalid_msgs = sum(1 for msg in st.session_state.hyri_engine.conversation_history 
                                 if not msg.is_valid)
                st.metric("Validation Warnings", invalid_msgs)
            
            # Export options
            st.subheader("📁 Export Conversation")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📄 Export as JSON"):
                    data = {
                        'conversation_id': datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
                        'active_context': st.session_state.hyri_engine.active_context,
                        'messages': [asdict(msg) for msg in st.session_state.hyri_engine.conversation_history]
                    }
                    
                    json_str = json.dumps(data, indent=2, ensure_ascii=False)
                    st.download_button(
                        "Download JSON",
                        json_str,
                        f"hyri_conversation_{data['conversation_id']}.json",
                        "application/json"
                    )
            
            with col2:
                if st.button("📋 Export as Text"):
                    text_export = []
                    text_export.append("HyRI Conversation Export")
                    text_export.append("=" * 30)
                    text_export.append(f"Focus: {st.session_state.hyri_engine.active_context.get('/focus', 'Unknown')}")
                    text_export.append(f"Context: {st.session_state.hyri_engine.active_context.get('/context', 'Unknown')}")
                    text_export.append("")
                    
                    for msg in st.session_state.hyri_engine.conversation_history:
                        text_export.append(f"[{msg.agent} - {msg.timestamp}]")
                        text_export.append(msg.raw_text)
                        text_export.append("")
                    
                    text_str = "\n".join(text_export)
                    st.download_button(
                        "Download Text",
                        text_str,
                        f"hyri_conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        "text/plain"
                    )
    
    else:
        # Welcome screen
        st.header("🌟 Welcome to HyRI")
        st.markdown("""
        **Hybrid Relational Intelligence** enables structured dialogue between humans and AI agents 
        using the NeuroGlyph protocol - a formal communication system that makes every conversation 
        transparent, accountable, and genuinely collaborative.
        
        ### Getting Started
        1. **Set your API keys** in the sidebar (OpenAI and/or Anthropic)
        2. **Define your conversation** topic, context, and intent
        3. **Start dialoguing** using NeuroGlyph tokens to structure your communication
        
        ### What Makes HyRI Special?
        - **🔗 Structured Protocol**: Every message includes explicit intent, context, and relationships
        - **🤖 Multi-Agent Support**: Seamless integration with GPT-4 and Claude
        - **🎯 Goal-Oriented**: Every conversation produces concrete deliverables
        - **📊 Transparent**: All communication is auditable and analyzable
        """)
        
        # Example conversation
        st.subheader("📖 Example NeuroGlyph Exchange")
        
        with st.expander("See Example Conversation"):
            st.code("""
Human:
🧠: Human
📚: consciousness_in_ai_systems  
💡: exploring_philosophical_implications
🎯: academic_research_dialogue
📦: theoretical_insights
❓: What would constitute evidence of genuine understanding in an AI system?

Claude:
🧠: claude_agent
📚: consciousness_in_ai_systems
🔗: responds_to->human_query
💡: contributing_philosophical_analysis  
📦: structured_argumentation
🔍: The question touches on the hard problem of consciousness. Perhaps we should 
distinguish between functional understanding (appropriate responses to stimuli) 
and phenomenological understanding (subjective experience of meaning)...
            """)

if __name__ == "__main__":
    main()