import json
import re


def parse_json_response(answer):

    if not answer:
        raise ValueError(
            "AI returned an empty response."
        )

    answer = answer.strip()

    answer = re.sub(
        r"```json",
        "",
        answer,
        flags=re.IGNORECASE
    )

    answer = answer.replace(
        "```",
        ""
    ).strip()

    start = answer.find("{")
    end = answer.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            "No JSON object found."
        )

    json_text = answer[
        start:end + 1
    ]

    try:
        return json.loads(json_text)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON: {error}"
        )