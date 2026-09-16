import json
import logging

import torch
from pydantic import BaseModel, ValidationError
from transformers import AutoTokenizer, AutoModelForCausalLM

logger = logging.getLogger(__name__)

MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL)

model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    torch_dtype=torch.float32,
)


def call_llm_structured(
    prompt: str, schema: type[BaseModel], max_retries: int = 2
) -> BaseModel:
    """
    Calls the local Qwen model and parses its response into `schema`.
    Retries with a correction message if the output fails validation.
    """

    messages = [
        {
            "role": "system",
            "content": (
                "Respond ONLY with valid JSON matching the required schema. "
                "No preamble, no markdown fences."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    for attempt in range(max_retries + 1):

        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = tokenizer(
            text,
            return_tensors="pt",
        )

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=1024,
                do_sample=False,
            )

        generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

        raw_text = tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True,
        ).strip()

        raw_text = (
            raw_text
            .removeprefix("```json")
            .removesuffix("```")
            .strip()
        )

        try:
            parsed_json = json.loads(raw_text)
            return schema(**parsed_json)

        except (json.JSONDecodeError, ValidationError) as e:

            logger.warning(
                f"structured output parse failed "
                f"(attempt {attempt}): {e}"
            )

            messages.append(
                {
                    "role": "assistant",
                    "content": raw_text,
                }
            )

            messages.append(
                {
                    "role": "user",
                    "content": (
                        f"That output was invalid: {e}. "
                        "Return ONLY valid JSON matching the schema, "
                        "nothing else."
                    ),
                }
            )

    raise ValueError(
        f"Failed to get valid structured output "
        f"after {max_retries + 1} attempts"
    )