# Technical Support AI Agent

A robust, multi-agent AI system designed to automate Tier 1 technical support. This intelligent agent is capable of diagnosing network issues, troubleshooting device problems, and guiding users through setup processes with step-by-step instructions.

## Capabilities

- **Intelligent Diagnostics**:
  - **Network Troubleshooting**: Diagnoses dropped calls, slow data, and signal issues.
  - **Device Support**: Assists with SIM/eSIM configuration, Wi-Fi calling setup, and voicemail issues.
  - **Step-by-Step Guidance**: Provides clear, numbered instructions for resolving common technical problems.

- **Multi-Modal Support**:
  - **Text Chat**: Real-time conversational interface.
  - **Voice Integration**: (Optional) Capable of text-to-speech responses for voice-enabled applications.

- **Context Awareness**:
  - Uses retrieval-augmented generation (RAG) to fetch up-to-date technical specifications and troubleshooting guides.
  - Maintains conversation context to ask relevant follow-up questions.

## Architecture

The system utilizes a specialized **TechSupportAgent** within a routing framework:
1.  **Intent Classification**: Identifies if a query is technical, billing-related, or sales-related.
2.  **Context Retrieval**: Fetches relevant technical knowledge bases (simulated via Perplexity API in this demo).
3.  **Response Generation**: Uses a Large Language Model (LLM) with a specialized system prompt to generate empathetic and accurate technical solutions.

## Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/HarshithM834/Technical-Support-AI-Agent.git
    cd Technical-Support-AI-Agent
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Variables**:
    Create a `.env` file with your API keys:
    ```
    GEMINI_API_KEY=your_gemini_key
    PERPLEXITY_API_KEY=your_perplexity_key (optional, for real-time context)
    ELEVENLABS_API_KEY=your_elevenlabs_key (optional, for voice)
    ```

4.  **Run the Server**:
    ```bash
    python main.py
    ```

## Usage

- **Chat Endpoint**: `POST /chat`
    ```json
    {
      "message": "My internet is not working on my phone",
      "customer_id": "test_user_1"
    }
    ```

- **Run Tests**:
    ```bash
    python tech_support_examples.py
    ```
