#!/usr/bin/env python3
"""
Example: Deploy a voice agent with custom tools.

This demonstrates how to use the Moss Voice Agent Manager to deploy an agent
with custom Python functions as tools.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from moss_voice_agent_manager import MossVoiceClient

load_dotenv()  # Load .env from current directory if it exists


# Define custom tools
def get_user_age(birth_year: int) -> str:
    """Calculate user's age from birth year."""
    from datetime import datetime
    current_year = datetime.now().year
    age = current_year - birth_year
    return f"You are approximately {age} years old."


def calculate_discount(original_price: float, discount_percent: float) -> str:
    """Calculate the final price after applying a discount."""
    if discount_percent < 0 or discount_percent > 100:
        return "Discount percent must be between 0 and 100."

    discount_amount = original_price * (discount_percent / 100)
    final_price = original_price - discount_amount

    return f"Original price: ${original_price:.2f}, Discount: {discount_percent}%, Final price: ${final_price:.2f}"


def main():
    """Deploy voice agent with custom tools."""

    # Configuration from environment
    # Required: Your Moss project credentials
    project_id = os.getenv("MOSS_PROJECT_ID")
    project_key = os.getenv("MOSS_PROJECT_KEY")
    voice_agent_id = os.getenv("MOSS_VOICE_AGENT_ID")

    if not project_id or not project_key or not voice_agent_id:
        print("❌ Error: Required environment variables missing")
        print("\nRequired:")
        print("  export MOSS_PROJECT_ID='your-project-uuid'")
        print("  export MOSS_PROJECT_KEY='your-project-read-key'")
        print("  export MOSS_VOICE_AGENT_ID='your-voice-agent-uuid'")
        return

    # Create client
    client = MossVoiceClient(
        project_id=project_id,
        project_key=project_key
    )

    # Deploy agent
    print("\n" + "="*60)
    print("🚀 Deploying voice agent with custom tools")
    print("="*60)

    try:
        # Deploy with custom tools
        response = client.deploy(
            voice_agent_id=voice_agent_id,
            prompt="You are a helpful assistant named May, with custom calculation tools. Help users calculate their age and discounts.",
            initial_greeting="Hello! I can help you calculate your age and apply discounts. How can I assist you?",
            function_tools=[get_user_age, calculate_discount],
        )

        print("✅ Deployment successful!")
        print(f"🎯 Voice Agent ID: {voice_agent_id}")
        print("="*60)

    except Exception as exc:
        print("\n" + "="*60)
        print("❌ Deployment failed!")
        print("="*60)
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
