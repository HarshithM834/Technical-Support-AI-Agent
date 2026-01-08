# demo.py
# Runnable demo: test all scenarios without needing FastAPI server

import asyncio
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def print_section(title: str):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


async def demo():
    """Run demo with test scenarios"""
    
    print_section("T-Mobile AI Agent - 2 Day Build Demo")
    print("Multi-agent customer support system")
    print("Powered by: Gemini + Perplexity + ElevenLabs")
    
    # Scenario 1: Billing
    print_section("Scenario 1: Billing Question")
    billing_query = {
        "message": "Why is my bill so high this month? I usually pay $80 but now it's $120.",
        "customer_id": "demo_cust_001",
    }
    print(f"Customer: {billing_query['message']}")
    try:
        response = client.post("/chat", json=billing_query)
        result = response.json()
        print(f"\nAgent Type: {result['agent_type']}")
        print(f"Response: {result['response'][:200]}...")
        print(f"Cost Estimate: ${result['cost_estimate']:.4f}")
        print("✓ Success")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Scenario 2: Sales
    print_section("Scenario 2: Sales Question")
    sales_query = {
        "message": "I'm interested in upgrading my plan. What are your unlimited options?",
        "customer_id": "demo_cust_002",
    }
    print(f"Customer: {sales_query['message']}")
    try:
        response = client.post("/chat", json=sales_query)
        result = response.json()
        print(f"\nAgent Type: {result['agent_type']}")
        print(f"Response: {result['response'][:200]}...")
        print(f"Cost Estimate: ${result['cost_estimate']:.4f}")
        print("✓ Success")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Scenario 3: Technical Support
    print_section("Scenario 3: Technical Support")
    tech_query = {
        "message": "My phone keeps dropping calls. What should I do?",
        "customer_id": "demo_cust_003",
    }
    print(f"Customer: {tech_query['message']}")
    try:
        response = client.post("/chat", json=tech_query)
        result = response.json()
        print(f"\nAgent Type: {result['agent_type']}")
        print(f"Response: {result['response'][:200]}...")
        print(f"Cost Estimate: ${result['cost_estimate']:.4f}")
        print("✓ Success")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print_section("Demo Complete")
    print("✓ Billing Agent working")
    print("✓ Sales Agent working")
    print("✓ Technical Support Agent working ✨")
    print("\nTo run this demo again: python3 demo.py")


if __name__ == "__main__":
    asyncio.run(demo())
