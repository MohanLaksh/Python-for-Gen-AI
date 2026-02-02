# Smart Study Assistant

A multi-role AI chatbot built with Python that automatically routes queries to ChatGPT, Gemini, or Claude based on task complexity and type.

## Features

- **Three Study Roles**
  - **Tutor**: Q&A, concept explanations, and step-by-step guidance
  - **Quiz Creator**: Generate practice questions (MCQs, True/False, Fill-in-the-blank)
  - **Summarizer**: Condense notes into key points and study guides

- **Automatic Model Routing**
  - Intelligently selects the best AI model for each task
  - Routes based on task complexity (simple, moderate, complex)
  - Supports OpenAI (GPT-4o), Google (Gemini), and Anthropic (Claude)

- **Role-Based Prompting**
  - Specialized prompt templates for each role
  - Context-aware responses
  - Consistent persona-based interactions

- **Interactive CLI**
  - Beautiful command-line interface with Rich
  - Conversation history management
  - Role and model override options

## Installation

1. Clone or download the project:
```bash
cd smart-study-assistant
Create a virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt
Configuration

Copy the example environment file:
cp .env.example .env
Edit .env and add your API keys:
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
ANTHROPIC_API_KEY=sk-ant-...
Note: At least one API key is required. All three can be configured for optimal routing.

Usage

Start Assistant

python main.py chat
Start with Specific Role or Model

# Force tutor role
python main.py chat --role tutor

# Force specific model
python main.py chat --model openai

# Add context
python main.py chat --context "subject=Computer Science, difficulty=advanced"

# Direct query
python main.py chat "What is machine learning?"
Interactive Commands

Once in the chat interface, you can use these commands:

/help - Show help message
/clear - Clear conversation context
/role <name> - Set role (tutor, quiz, summary)
/model <name> - Set model (openai, gemini, claude)
/context <kv> - Set context (format: key=value, topic=value)
/quit - Exit assistant
Execution Flows

This section provides visual diagrams showing how Smart Study Assistant processes requests through its components.

Overall Request Processing Flow

graph TD
    subgraph CLI
        A[[User Input]] --> B[/chat command]
        B --> C[StudyAssistant.init]
    end
    
    subgraph Router["Router Component"]
        C --> D[TaskClassifier.classify]
        D --> E[(TaskType, ComplexityLevel)]
        E --> F[ModelRouter.route]
    end
    
    subgraph Roles
        F --> G[role.prepare_prompt]
    end
    
    subgraph Models["Models Component"]
        G --> H[BaseLLMClient.generate_response]
        H --> I[(AI API Call)]
        I --> J[Response]
    end
    
    subgraph Session["Session Component"]
        J --> K[SessionManager.add_message]
        K --> L[(Conversation History)]
    end
    
    L --> M[Display Response]
    M --> A
Task Classification Logic

graph TD
    A[TaskClassifier.classify] --> B[Input: Lowercase]
    
    B --> C[TaskClassifier._classify_task_type]
    C --> D[TaskClassifier._classify_complexity]
    
    subgraph Data["Keyword Dictionaries"]
        E[(tutor_keywords)]
        F[(quiz_keywords)]
        G[(summary_keywords)]
    end
    
    C --> E
    C --> F
    C --> G
    
    E --> H[Score Quiz Keywords]
    F --> H
    G --> H
    
    H --> I{Score Comparison}
    I -->|Quiz Score Highest| J[TaskType.QUIZ]
    I -->|Summary Score >= Tutor| K[TaskType.SUMMARY]
    I -->|Tutor Score Highest| L[TaskType.TUTOR]
    
    subgraph Complexity
        M[(complexity_keywords)]
        N[Score Keywords]
    end
    
    D --> M
    N --> O{Complex Score > 0?}
    O -->|Yes| P[ComplexityLevel.COMPLEX]
    O -->|No| Q{Moderate Score > 0?}
    Q -->|Yes| R[ComplexityLevel.MODERATE]
    Q -->|No| S[ComplexityLevel.SIMPLE]
    
    J --> T[(TaskType, ComplexityLevel)]
    K --> T
    L --> T
    P --> T
    R --> T
    S --> T
Model Routing Decision

graph TD
    A[ModelRouter.route] --> B{Override Model?}
    
    B -->|Yes| C[ModelRouter._get_client_by_name]
    B -->|No| D[Lookup routing_rules]
    
    subgraph Configuration["Routing Data"]
        E[(routing_rules)]
        F[(client_map)]
    end
    
    D --> E
    E --> F
    
    F --> G{(TaskType, Complexity)<br/>in client_map?}
    G -->|Yes| H[Return Matched Client]
    G -->|No| I[ModelRouter._get_default_client]
    
    subgraph Clients["Available AI Models"]
        J[(clients dict)]
        K{OpenAI Key?}
        L{Gemini Key?}
        M{Claude Key?}
    end
    
    C --> N{Name in clients?}
    N -->|Yes| J
    N -->|No| I
    
    I --> K
    I --> L
    I --> M
    
    K -->|Yes| O[OpenAIClient]
    L -->|Yes| P[GeminiClient]
    M -->|Yes| Q[ClaudeClient]
    
    O --> R[Return Client]
    P --> R
    Q --> R
    H --> R
Routing Rules Matrix

graph LR
    subgraph Router["Routing Rules Matrix"]
        subgraph Tutor["TaskType.TUTOR"]
            A((Simple)) --> A1[GPT-4o-mini]
            B((Moderate)) --> B1[Claude 3.5 Sonnet]
            C((Complex)) --> C1[GPT-4o]
        end
        
        subgraph Quiz["TaskType.QUIZ"]
            D((Simple)) --> D1[Gemini Flash]
            E((Moderate)) --> E1[Gemini Flash]
            F((Complex)) --> F1[GPT-4o]
        end
        
        subgraph Summary["TaskType.SUMMARY"]
            G((Simple)) --> G1[GPT-4o-mini]
            H((Moderate)) --> H1[GPT-4o-mini]
            I((Complex)) --> I1[Claude 3.5 Sonnet]
        end
    end
    
    subgraph Providers["Model Providers"]
        subgraph OpenAI["OpenAI Models"]
            A1
            C1
            F1
            G1
            H1
        end
        
        subgraph Google["Google Models"]
            D1
            E1
        end
        
        subgraph Anthropic["Anthropic Models"]
            B1
            I1
        end
    end
Role-Based Prompting Examples

Tutor Role

> What is recursion?
> Explain the concept of inheritance in Python
> How does a neural network learn?
> Use an analogy to explain binary search
Quiz Creator Role

> Generate a quiz about Python data types
> Create 5 multiple-choice questions about SQL
> Test me on basic calculus concepts
> Make a true/false quiz about JavaScript
Summarizer Role

> Summarize these notes: [paste text]
> Create a study guide from this lecture: [paste text]
> Condense this article into bullet points: [paste text]
Model Routing Logic

The assistant automatically selects the best AI model for each task. See Routing Rules Matrix above for complete routing decisions.

Project Structure

smart-study-assistant/
├── main.py                 # CLI entry point
├── config.py               # Configuration & API keys
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
├── models/
│   ├── base_model.py      # Abstract model interface
│   ├── openai_client.py   # ChatGPT integration
│   ├── gemini_client.py   # Gemini integration
│   └── claude_client.py   # Claude integration
├── router/
│   ├── task_classifier.py # Analyze query type/complexity
│   └── model_router.py   # Select appropriate model
├── roles/
│   ├── base_role.py       # Abstract role interface
│   ├── tutor.py          # Q&A & explanations
│   ├── quiz_creator.py    # Generate practice questions
│   └── summarizer.py     # Note summarization
├── prompts/
│   ├── tutor_prompts.py   # Tutor role templates
│   ├── quiz_prompts.py    # Quiz generation templates
│   └── summary_prompts.py # Summarization templates
├── session/
│   └── session_manager.py # Conversation history
└── utils/
    └── helpers.py         # Utility functions
Dependencies

openai - OpenAI API client
google-generativeai - Google Gemini API client
anthropic - Anthropic Claude API client
click - CLI framework
python-dotenv - Environment variable management
pydantic - Data validation
pydantic-settings - Settings management
rich - Rich terminal output
Requirements

Python 3.10+
At least one AI API key (OpenAI, Gemini, or Claude)
Getting API Keys

OpenAI

Visit platform.openai.com
Sign in and create an account
Go to API Keys section
Create a new API key
Google Gemini

Visit aistudio.google.com
Sign in with Google account
Create a new API key
Copy the key
Anthropic Claude

Visit console.anthropic.com
Sign up for an account
Go to API Keys section
Generate a new API key
License

This project is for educational purposes.