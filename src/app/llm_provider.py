"""LLM provider module for configurable language model support."""

import os
from typing import Optional
from langchain.llms.base import LLM
from langchain.llms.fake import FakeListLLM


def get_llm() -> LLM:
    """Get the configured LLM instance based on environment settings."""
    provider = os.getenv("LLM_PROVIDER", "fake").lower()

    if provider == "openai":
        try:
            from langchain.llms import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                print("WARNING: OPENAI_API_KEY not set, falling back to fake LLM")
                return FakeListLLM(responses=["Evidence not configured. Please set OPENAI_API_KEY."])
            model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            return OpenAI(api_key=api_key, model=model)
        except ImportError:
            print("WARNING: OpenAI not installed, falling back to fake LLM")
            return FakeListLLM(responses=["OpenAI not installed. Install with: pip install openai"])

    elif provider == "ollama":
        try:
            from langchain_community.llms import Ollama
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model = os.getenv("OLLAMA_MODEL", "llama2")
            return Ollama(base_url=base_url, model=model)
        except ImportError:
            print("WARNING: Ollama not installed, falling back to fake LLM")
            return FakeListLLM(responses=["Ollama not installed. Install with: pip install langchain-community"])

    elif provider == "huggingface":
        try:
            from langchain.llms import HuggingFacePipeline
            from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

            token = os.getenv("HUGGINGFACE_TOKEN")
            model_name = os.getenv("HUGGINGFACE_MODEL", "gpt2")

            tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
            model = AutoModelForCausalLM.from_pretrained(model_name, token=token)

            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=512,
                temperature=0.7
            )

            return HuggingFacePipeline(pipeline=pipe)
        except ImportError:
            print("WARNING: HuggingFace not installed, falling back to fake LLM")
            return FakeListLLM(responses=["HuggingFace not installed. Install with: pip install transformers"])

    else:
        # Default to fake LLM for development/testing
        return FakeListLLM(responses=[
            "This is a test response from the fake LLM.",
            "Evidence generation is working with fake LLM.",
            "Configure LLM_PROVIDER in .env for real responses."
        ])