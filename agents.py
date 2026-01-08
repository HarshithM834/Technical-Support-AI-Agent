# agents.py
# Multi-agent system: Agent classes and routing

from services import generate_response, get_context_from_perplexity
import logging

logger = logging.getLogger(__name__)


class Agent:
    """Base agent class"""
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
    
    def process(self, customer_message: str, context: str) -> str:
        """Process customer message and return response"""
        response = generate_response(self.role, customer_message, context)
        logger.info(f"{self.name} processed message")
        return response


class BillingAgent(Agent):
    """
    Handles billing-related queries
    Responsibilities:
    - Explain charges and fees
    - Handle billing disputes
    - Provide refund information
    - Explain payment options
    - Track account credits
    - Suggest cost-saving options
    """
    def __init__(self):
        super().__init__("BillingAgent", "billing")
    
    def process(self, customer_message: str, context: str) -> str:
        """Process billing inquiries"""
        response = super().process(customer_message, context)
        logger.info("BillingAgent: Processed billing inquiry")
        return response


class SalesAgent(Agent):
    """
    Handles sales and upsell queries
    Responsibilities:
    - Explain plans and benefits
    - Recommend plan upgrades
    - Promote add-on services
    - Handle new customer inquiries
    - Provide promotional offers
    - Compare plan options
    """
    def __init__(self):
        super().__init__("SalesAgent", "sales")
    
    def process(self, customer_message: str, context: str) -> str:
        """Process sales inquiries"""
        response = super().process(customer_message, context)
        logger.info("SalesAgent: Processed sales inquiry")
        return response


class TechSupportAgent(Agent):
    """
    Handles technical support queries
    Responsibilities:
    - Troubleshoot network issues
    - Provide device support
    - Explain technical features
    - Guide through setup processes
    - Check basic coverage / signal questions
    - Suggest next steps or escalation
    """
    def __init__(self):
        super().__init__("TechSupportAgent", "technical_support")
    
    def process(self, customer_message: str, context: str) -> str:
        """Process technical support inquiries"""
        response = super().process(customer_message, context)
        logger.info("TechSupportAgent: Processed technical support inquiry")
        return response


class GeneralAgent(Agent):
    """Handles miscellaneous queries"""
    def __init__(self):
        super().__init__("GeneralAgent", "other")


class AgentRouter:
    """Routes customer messages to appropriate agent"""
    def __init__(self):
        self.agents = {
            "billing": BillingAgent(),
            "sales": SalesAgent(),
            "technical_support": TechSupportAgent(),
            "other": GeneralAgent(),
        }
        logger.info("AgentRouter initialized with all agents")
    
    def route(self, intent: str, customer_message: str) -> tuple:
        """
        Route customer message to appropriate agent.
        Returns: (agent_name, response)
        """
        # Get the agent
        agent = self.agents.get(intent, self.agents["other"])
        
        # Get context
        context = get_context_from_perplexity(customer_message)
        
        # Get response from agent
        response = agent.process(customer_message, context)
        
        logger.info(f"Routed to {agent.name}")
        return agent.name, response
