import argparse
import sys
import json
from summariser.openai_client import OpenAIClient
from summariser.anthropic_client import AnthropicClient
from summariser.gemini_client import GeminiClient
from summariser.lmstudio_client import LMStudioClient
from schemas.summary_schema import SummaryOutput

def get_client(provider: str):
    if provider == "openai":
        return OpenAIClient()
    elif provider == "anthropic":
        return AnthropicClient()
    elif provider == "gemini":
        return GeminiClient()
    elif provider == "lmstudio":
        return LMStudioClient()
    else:
        raise ValueError(f"Unknown provider: {provider}")

def read_input(file_path: str = None, text: str = None) -> str:
    if file_path:
        with open(file_path, 'r') as f:
            return f.read()
    if text:
        return text
    # Read from stdin if no arguments provided
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""

def main():
    parser = argparse.ArgumentParser(description="Smart Text Summariser")
    parser.add_argument("--provider", type=str, choices=["openai", "anthropic", "gemini", "lmstudio"], default="openai", help="LLM Provider")
    parser.add_argument("--input-file", type=str, help="Path to input text file")
    parser.add_argument("--text", type=str, help="Raw input text")
    parser.add_argument("--tone", type=str, default="neutral", help="Tone of the summary")
    
    args = parser.parse_args()
    
    input_text = read_input(args.input_file, args.text)
    
    if not input_text:
        print("Error: No input text provided. Use --input-file, --text, or pipe input via stdin.")
        sys.exit(1)
        
    try:
        client = get_client(args.provider)
        summary: SummaryOutput = client.summarize(input_text, tone=args.tone)
        
        # Output result as JSON
        print(summary.model_dump_json(indent=2))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
