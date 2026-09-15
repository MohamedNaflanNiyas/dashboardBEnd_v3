from .model import load_model


def generate_dashboard(prompt):

    tokenizer, model, device = load_model()

    messages = [
        {
            "role": "system",
            "content": prompt
        }
    ]

    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    outputs = model.generate(
        **inputs,
        max_new_tokens=1500,
        do_sample=False
    )

    generated_tokens = outputs[
        0
    ][
        inputs["input_ids"].shape[-1]:
    ]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return answer