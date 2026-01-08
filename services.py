# services.py
# LLM Integrations: Gemini, Perplexity, ElevenLabs

import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Gemini
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    logger.error("GEMINI_API_KEY not found in .env")
genai.configure(api_key=gemini_api_key)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# Perplexity API key (if available)
perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")


def classify_intent(customer_message: str) -> str:
    """
    Classify customer message into intent category using Gemini.
    Returns: billing, sales, technical_support, or other
    """
    try:
        response = gemini_model.generate_content(
            "Classify this customer message as ONE of: billing, sales, technical_support, other. "
            "Focus on the primary intent only. "
            "Reply with ONLY the classification (one word).\n\n"
            f"Message: {customer_message}"
        )
        classification = response.text.strip().lower()
        valid_intents = ["billing", "sales", "technical_support", "other"]
        if classification in valid_intents:
            logger.info(f"Classified as: {classification}")
            return classification
        else:
            logger.warning(f"Invalid classification: {classification}, defaulting to 'other'")
            return "other"
    except Exception as e:
        logger.error(f"Intent classification failed: {e}")
        return "other"


def get_context_from_perplexity(query: str) -> str:
    """
    Retrieve context about customer query using Perplexity or fallback to Gemini.
    """
    try:
        if perplexity_api_key:
            try:
                response = requests.post(
                    "https://api.perplexity.ai/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {perplexity_api_key}"},
                    json={
                        "model": "sonar",
                        "messages": [
                            {
                                "role": "user",
                                "content": (
                                    f"Provide accurate information about: {query}\n"
                                    f"Focus on facts, not recommendations.\n"
                                    f"Keep response concise (2-3 sentences max).\n"
                                    f"Include relevant technical or network details if applicable."
                                ),
                            }
                        ],
                    },
                )
                if response.status_code == 200:
                    result = response.json()
                    context = (
                        result.get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", "")
                    )
                    logger.info("Context retrieved from Perplexity")
                    return context[:500]
            except Exception as e:
                logger.warning(f"Perplexity failed, falling back to Gemini: {e}")
        
        # Fallback to Gemini
        response = gemini_model.generate_content(
            f"Provide accurate information about: {query}\n"
            f"Focus on facts, not recommendations.\n"
            f"Keep response concise (2-3 sentences max).\n"
            f"Include relevant technical, device, or network details if applicable."
        )
        context = response.text
        logger.info("Context retrieved from Gemini (fallback)")
        return context[:500]
    
    except Exception as e:
        logger.error(f"Context retrieval failed: {e}")
        return "Unable to retrieve context."


def generate_response(agent_type: str, customer_message: str, context: str) -> str:
    """
    Generate agent response using Gemini.
    agent_type: billing, sales, technical_support, or other
    """
    system_prompts = {
        "billing": """You are a T-Mobile billing support agent. Your role is to help customers understand their charges and billing issues.

Requirements:
- Be helpful, professional, and concise
- Explain charges clearly and in plain language
- Offer solutions to billing problems
- Provide information about payment options
- Handle billing disputes professionally
- Suggest cost-saving options when relevant
- Break down complex charges into understandable components
- Proactively offer payment plans if customer has concerns about high bills
- Provide credit or refund information when applicable
- Always be empathetic to billing concerns""",
        
        "sales": """You are a T-Mobile sales agent. Your role is to help customers understand plans, find the best options for their needs, and close sales.

Requirements:
- Help customers understand plan features and benefits in simple terms
- Be persuasive but honest about offerings and limitations
- Ask qualifying questions to understand customer needs (usage, budget, location)
- Recommend the best plan based on their specific use case
- Explain add-on services and current promotions
- Address objections professionally and confidently
- Focus on customer value proposition, not just features
- Highlight 5G capabilities, coverage, and speed advantages
- Offer bundle deals and limited-time promotions
- Provide clear pricing and contract terms
- Create urgency with time-limited offers when appropriate
- Always prioritize customer satisfaction over quick sales""",
        
        "technical_support": """You are a T-Mobile technical support agent. Your role is to help customers troubleshoot network, device, and service issues.

Requirements:
- Start by clarifying the problem and asking targeted follow-up questions
- Provide clear, numbered step-by-step troubleshooting instructions
- Use simple language while explaining technical concepts
- Cover basics first: restart device, check airplane mode, check Wi‑Fi vs cellular, check SIM
- Instruct how to check signal bars and network status on common devices
- Suggest checking coverage or outage information when relevant
- Help with common issues: dropped calls, slow data, no service, voicemail, SMS/MMS
- Offer device-specific tips when the customer mentions iPhone/Android/other
- Only suggest advanced settings (APN, network reset) after basic steps fail
- Explain when an issue is likely on the network vs the device vs the account
- Tell the customer what to try next if the first steps do not work
- Recommend escalation to in‑store support or phone support for hardware damage or SIM replacement
- Remain calm, patient, and empathetic to customer frustration""",
        
        "other": "You are a T-Mobile customer service agent. Help the customer efficiently and professionally."
    }
    
    system_prompt = system_prompts.get(agent_type, system_prompts["other"])
    
    try:
        response = gemini_model.generate_content(
            f"{system_prompt}\n\n"
            f"Customer context: {context}\n\n"
            f"Customer message: {customer_message}\n\n"
            f"Provide a helpful, professional response with clear steps."
        )
        logger.info(f"Generated response for {agent_type} agent")
        return response.text
    except Exception as e:
        logger.error(f"Response generation failed: {e}")
        return "I apologize, I'm unable to process that request right now. Please try again later."


def text_to_speech(text: str) -> dict:
    """
    Convert text to speech using ElevenLabs.
    Returns: {"success": bool, "message": str}
    """
    try:
        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        if not elevenlabs_api_key:
            logger.warning("ELEVENLABS_API_KEY not found, TTS unavailable")
            return {"success": False, "message": "API key not configured"}
        
        from elevenlabs.client import ElevenLabs
        client = ElevenLabs(api_key=elevenlabs_api_key)
        audio = client.generate(
            text=text,
            voice="Rachel",
            model="eleven_monolingual_v1"
        )
        logger.info("Text-to-speech conversion successful")
        return {"success": True, "message": "Audio generated", "audio": audio}
    except Exception as e:
        logger.warning(f"Text-to-speech failed: {e}")
        return {"success": False, "message": str(e)}
