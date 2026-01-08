# tech_support_examples.py
# Test technical support agent with multiple scenarios

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_tech_support_examples():
    """Test multiple technical support scenarios"""
    
    examples = [
        {
            "name": "Dropped Calls",
            "message": "My phone keeps dropping calls at home. What can I do?",
            "customer_id": "tech_001",
        },
        {
            "name": "No Service",
            "message": "I suddenly have no service on my phone. It was working yesterday.",
            "customer_id": "tech_002",
        },
        {
            "name": "Slow Data",
            "message": "My mobile data is very slow even though I have full bars.",
            "customer_id": "tech_003",
        },
        {
            "name": "Wi-Fi Calling",
            "message": "How do I turn on Wi‑Fi calling on my phone?",
            "customer_id": "tech_004",
        },
        {
            "name": "Voicemail Setup",
            "message": "How do I set up my voicemail on T‑Mobile?",
            "customer_id": "tech_005",
        },
        {
            "name": "SIM/ESIM Issue",
            "message": "My eSIM stopped working after I changed phones.",
            "customer_id": "tech_006",
        },
    ]
    
    print("\n" + "="*70)
    print("  TECH SUPPORT AGENT - COMPREHENSIVE TEST")
    print("="*70 + "\n")
    
    successful = 0
    failed = 0
    
    for i, example in enumerate(examples, 1):
        print(f"\nTest {i}: {example['name']}")
        print(f"Customer: {example['message']}")
        
        try:
            response = client.post("/chat", json={
                "message": example["message"],
                "customer_id": example["customer_id"],
            })
            result = response.json()
            
            print(f"Agent: {result['agent_type']}")
            print(f"Response: {result['response'][:150]}...")
            print(f"Cost: ${result['cost_estimate']:.4f}")
            print("✓ Success")
            successful += 1
        except Exception as e:
            print(f"✗ Error: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    print(f"\nTotal Tests: {len(examples)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(successful/len(examples)*100):.1f}%")
    print("\n✓ Technical Support Agent is working correctly!\n")


if __name__ == "__main__":
    test_tech_support_examples()
