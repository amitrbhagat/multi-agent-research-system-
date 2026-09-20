import json
import logging

import ollama
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "llama3.2:1b"


class StructuredOutputError(Exception):
    """Raised when the LLM fails to return data matching the schema."""
    pass


def call_llm_structured(
    prompt: str,
    schema: type[BaseModel],
    model: str = DEFAULT_MODEL,
    max_retries: int = 2,
) -> BaseModel:
    """
    Calls an LLM through Ollama using native JSON schema enforcement
    and validates the response against the provided Pydantic schema.

    Retries automatically if parsing or validation fails.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a precise research writing assistant. "
                "Always respond with data that strictly conforms "
                "to the requested format."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    json_schema = schema.model_json_schema()

    for attempt in range(max_retries + 1):
        raw_text = ""

        try:
            response = ollama.chat(
                model=model,
                messages=messages,
                format=json_schema,
                options={
                    "temperature": 0,
                    "num_predict": 512,
                },
            )

            raw_text = response["message"]["content"].strip()
            parsed_json = json.loads(raw_text)
            return schema(**parsed_json)

        except (json.JSONDecodeError, ValidationError) as e:
            logger.warning(
                f"Validation failed (attempt {attempt + 1}/{max_retries + 1}): {e}"
            )

            if attempt == max_retries:
                break

            # Append context for self-correction on retry
            messages.extend([
                {"role": "assistant", "content": raw_text},
                {
                    "role": "user",
                    "content": (
                        f"Your previous output was invalid: {e}. "
                        "Please fix the errors and return output "
                        "that strictly follows the required schema."
                    ),
                },
            ])

        except Exception as e:
            logger.error(f"LLM call failed on attempt {attempt + 1}: {e}")
            raise

    raise StructuredOutputError(
        f"Failed to generate valid structured output "
        f"after {max_retries + 1} attempts."
    )
