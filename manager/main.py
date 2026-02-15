#!/usr/bin/env python3
"""
Example: Deploy a customer care voice agent with support tools.

This demonstrates how to use the Moss Voice Agent Manager to deploy a
customer care agent with tools for order lookup, returns, and support tickets.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from moss_voice_agent_manager import MossVoiceClient

load_dotenv()  # Load .env from current directory if it exists


# Define customer care tools
def lookup_order_status(order_id: str) -> str:
    """Look up the current status of a customer order."""
    # In a real application, this would query your order management system
    # This is a mock implementation for demonstration
    order_statuses = {
        "ORD12345": "Your order is currently in transit and expected to arrive tomorrow.",
        "ORD67890": "Your order has been delivered on Feb 13, 2026.",
        "ORD11111": "Your order is being prepared for shipment."
    }

    order_id_upper = order_id.upper()
    if order_id_upper in order_statuses:
        return order_statuses[order_id_upper]
    else:
        return f"I couldn't find an order with ID {order_id}. Please verify the order number and try again."


def initiate_return(order_id: str, reason: str) -> str:
    """Initiate a return request for an order."""
    # In a real application, this would create a return in your system
    # This is a mock implementation for demonstration
    if not order_id or not reason:
        return "I need both the order ID and reason for the return to proceed."

    return_id = f"RET{order_id[-5:]}"
    return f"I've initiated return request {return_id} for order {order_id}. You'll receive a prepaid return label via email within 24 hours. Your refund will be processed once we receive the item."


def check_product_availability(product_name: str) -> str:
    """Check if a product is currently in stock."""
    # In a real application, this would query your inventory system
    # This is a mock implementation for demonstration
    product_name_lower = product_name.lower()

    if "laptop" in product_name_lower:
        return f"The {product_name} is currently in stock with 15 units available. Expected delivery in 2-3 business days."
    elif "headphones" in product_name_lower:
        return f"The {product_name} is temporarily out of stock. We expect to restock in 5-7 days."
    else:
        return f"I found the {product_name} in our catalog. It's currently in stock and ready to ship."


def create_support_ticket(issue_description: str, priority: str = "normal") -> str:
    """Create a support ticket for customer issues."""
    # In a real application, this would create a ticket in your support system
    # This is a mock implementation for demonstration
    import random
    ticket_id = f"TICKET-{random.randint(10000, 99999)}"

    priority_levels = {"low": "Low", "normal": "Normal", "high": "High", "urgent": "Urgent"}
    priority_display = priority_levels.get(priority.lower(), "Normal")

    return f"I've created support ticket {ticket_id} with {priority_display} priority for: '{issue_description}'. Our support team will contact you within 24 hours via email."


def main():
    """Deploy customer care voice agent with support tools."""

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
    print("🚀 Deploying customer care voice agent")
    print("="*60)

    try:
        # Deploy with customer care tools
        response = client.deploy(
            voice_agent_id=voice_agent_id,
            prompt="You are a friendly and professional customer care agent named Alex. Help customers with order inquiries, returns, product availability, and general support issues. Be empathetic, clear, and solution-oriented. Always confirm order details before processing requests.",
            initial_greeting="Hello! Thank you for calling customer support. I'm Alex, and I'm here to help you today. How can I assist you?",
            function_tools=[lookup_order_status, initiate_return, check_product_availability, create_support_ticket],
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
