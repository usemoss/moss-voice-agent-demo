# Moss Voice Agent - Complete Setup Guide

A complete voice agent system built with Moss Voice Platform, featuring a Python-based agent deployment manager and a Next.js web interface for real-time voice interactions.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Part 1: Deploy the Voice Agent (Manager)](#part-1-deploy-the-voice-agent-manager)
- [Part 2: Run the Web Interface (Agent UI)](#part-2-run-the-web-interface-agent-ui)
- [Voice Server Package (@moss-tools/voice-server)](#voice-server-package-moss-toolsvoice-server)
- [Customizing Your Agent](#customizing-your-agent)
- [Additional Resources](#additional-resources)
- [Support](#support)

---

## 🎯 Overview

- **Manager (Python)**: Deploys voice agent with custom tools
- **Agent UI (Next.js)**: Web interface for voice interactions

## 🏗️ Architecture

```
Manager (Python) → Moss Platform ← Agent UI (Next.js)
```

---

## ✅ Prerequisites

### Required Software

- **Python+** (for Manager)
- **Node.js+** (for Agent UI)
- **pnpm** (package manager for Agent UI)
- **Git** (optional, for version control)

### Moss Platform Credentials

You'll need three pieces of information from your Moss Platform account:

1. **MOSS_PROJECT_ID** - Your project UUID
2. **MOSS_PROJECT_KEY** - Your project read key (starts with `moss_`)
3. **MOSS_VOICE_AGENT_ID** - Your voice agent UUID

**How to get these:**
1. Sign up at [Moss Platform](https://portal.usemoss.dev/)
2. Create a new project
3. Navigate to your project settings to find your Project ID,  API Key and Voice Agent ID

---

## 🚀 Getting Started

### Clone or Navigate to Your Project

```bash
cd voice-manage-test
```

Your project structure should look like this:

```
voice-manage-test/
├── manager/              # Python deployment manager
│   ├── main.py          # Agent deployment script
│   ├── pyproject.toml   # Python dependencies
│   └── .env             # Environment variables
└── agent-ui/            # Next.js web interface
    ├── app/             # Next.js app directory
    ├── package.json     # Node dependencies
    └── .env.local       # Environment variables
```

---

## 📦 Part 1: Deploy the Voice Agent (Manager)

The Manager is a Python script that deploys your voice agent configuration to the Moss Platform.

### Step 1.1: Navigate to Manager Directory

```bash
cd manager
```

### Step 1.2: Set Up Environment Variables

Create or edit the `.env` file with your Moss credentials:

```bash
# manager/.env
MOSS_PROJECT_ID=your-project-uuid-here
MOSS_PROJECT_KEY=moss_your-project-key-here
MOSS_VOICE_AGENT_ID=your-voice-agent-uuid-here
```

### Step 1.3: Create Virtual Environment

```bash
# Create a Python virtual environment using uv
uv venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate
```

### Step 1.4: Install Dependencies

```bash
# Install required Python packages from PyPI
uv pip install moss-voice-agent-manager python-dotenv


This will install:
- `moss-voice-agent-manager` - SDK for deploying agents
- `python-dotenv` - For loading environment variables

### Step 1.5: Deploy Your Agent

```bash
python main.py
```

**Expected Output:**

```
============================================================
🚀 Deploying voice agent with custom tools
============================================================
✅ Deployment successful!
🎯 Voice Agent ID: 9c11b621-44bf-42ee-9e40-9b81804b48f0
============================================================
```

---

## 🌐 Part 2: Run the Web Interface (Agent UI)

### Step 2.1: Navigate to Agent UI Directory

```bash
# From the manager directory, go back and enter agent-ui
cd ../agent-ui
```

### Step 2.2: Set Up Environment Variables

Create or edit `.env.local` with your Moss credentials:

```bash
# agent-ui/.env.local
MOSS_PROJECT_ID=your-project-uuid-here
MOSS_PROJECT_KEY=moss_your-project-key-here
MOSS_VOICE_AGENT_ID=your-voice-agent-uuid-here
```

**Note:** Use the same credentials as `manager/.env`

### Step 2.3: Install Dependencies

```bash
pnpm install
```

### Step 2.4: Run the Development Server

```bash
pnpm dev
```

**Expected Output:**

```
  ▲ Next.js 15.5.9
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Starting...
 ✓ Ready in 2.3s
```

### Step 2.5: Open the Application

1. Open your web browser
2. Navigate to: **http://localhost:3000**
3. You should see the voice agent interface

### Step 2.6: Start a Voice Conversation

1. Click the "Start" button
2. Allow microphone access when prompted
3. Start speaking to the agent

---

## 🔌 Voice Server Package (@moss-tools/voice-server)

The Agent UI uses `@moss-tools/voice-server` to connect to your deployed agent.

### Key Files

- [app/api/connection-details/route.ts](agent-ui/app/api/connection-details/route.ts) - Creates voice server connections
- [lib/utils.ts](agent-ui/lib/utils.ts) - Handles token fetching

### API Usage in route.ts

```typescript
import { MossVoiceServer } from "@moss-tools/voice-server";

// Create voice server instance
const voiceServer = await MossVoiceServer.create({
  projectId: process.env.MOSS_PROJECT_ID!,
  projectKey: process.env.MOSS_PROJECT_KEY!,
  voiceAgentId: process.env.MOSS_VOICE_AGENT_ID!,
});

// Get server URL
const serverUrl = voiceServer.getServerUrl();

// Create participant token
const participantToken = await voiceServer.createParticipantToken(
  { identity: participantIdentity, name: participantName },
  roomName,
  agentName
);
```

### API Response

```typescript
{
  serverUrl: string;
  roomName: string;
  participantName: string;
  participantToken: string;
}
```

---

## 🛠️ Customizing Your Agent

### Adding New Tools

Edit [manager/main.py](manager/main.py) to add new functions:

```python
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # Your implementation here
    return f"The weather in {city} is sunny!"

def main():
    # ... existing code ...

    response = client.deploy(
        voice_agent_id=voice_agent_id,
        prompt="Updated prompt mentioning weather...",
        initial_greeting="Hello! I can help with age, discounts, and weather!",
        function_tools=[
            get_user_age,
            calculate_discount,
            get_weather  # Add your new tool
        ],
    )
```

**Requirements for tool functions:**
- Must have type hints for parameters
- Must have a docstring (used by LLM to understand the tool)
- Must return a string (the agent will speak this)

### Changing Agent Behavior

Modify the `prompt` parameter in [manager/main.py:69](manager/main.py#L69):

```python
response = client.deploy(
    voice_agent_id=voice_agent_id,
    prompt="""You are a professional financial advisor named Alex.
    You help users with calculations and provide detailed explanations.
    Always be formal and precise in your responses.""",
    initial_greeting="Good day! I'm Alex, your financial advisor. How may I assist you?",
    function_tools=[get_user_age, calculate_discount],
)
```

### Customizing the UI

The UI components are in [agent-ui/app](agent-ui/app) directory:
- Modify styling in Tailwind classes
- Customize components in `agent-ui/components/`
- Update layout and branding as needed

### Re-deploying Changes

After making changes:

```bash
# 1. Re-deploy the agent (if you changed tools/prompt)
cd manager
python main.py

# 2. Restart the UI (if you changed UI code)
cd ../agent-ui
# Stop the dev server (Ctrl+C) and restart
pnpm dev
```

---


### Project Structure Details

```
voice-manage-test/
├── manager/
│   ├── main.py              # Agent deployment script
│   ├── pyproject.toml       # Python dependencies & project config
│   ├── .env                 # Environment variables (gitignored)
│   ├── .venv/              # Python virtual environment
│   └── README.md           # (create for manager-specific docs)
│
└── agent-ui/
    ├── app/
    │   ├── api/
    │   │   └── connection-details/
    │   │       └── route.ts # API endpoint for voice connections
    │   └── page.tsx        # Main page component
    ├── components/         # React components
    ├── lib/               # Utility functions
    ├── public/            # Static assets
    ├── package.json       # Node dependencies
    ├── .env.local        # Environment variables (gitignored)
    └── README.md         # (create for UI-specific docs)
```

---

## 🤝 Support

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Review Moss Platform documentation** for credential setup
3. **Check browser console** for client-side errors
4. **Check terminal output** for server-side errors
5. **Verify environment variables** match between manager and agent-ui

---
