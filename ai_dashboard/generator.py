from .model import load_model


_MODEL = None
_TOKENIZER = None
_DEVICE = None


def get_model():

    global _MODEL
    global _TOKENIZER
    global _DEVICE

    if (
        _MODEL is None
        or _TOKENIZER is None
        or _DEVICE is None
    ):
        (
            _TOKENIZER,
            _MODEL,
            _DEVICE
        ) = load_model()

    return (
        _TOKENIZER,
        _MODEL,
        _DEVICE
    )


def generate_text(prompt):

    tokenizer, model, device = get_model()

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
        do_sample=False,
    )

    generated_tokens = outputs[
        0
    ][
        inputs["input_ids"].shape[-1]:
    ]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return response.strip()


def generate_dashboard(prompt):
    return generate_text(prompt)


# from .model import load_model


# def generate_dashboard(prompt):

#     tokenizer, model, device = load_model()

#     messages = [
#         {
#             "role": "system",
#             "content": prompt
#         }
#     ]

#     inputs = tokenizer.apply_chat_template(
#         messages,
#         add_generation_prompt=True,
#         tokenize=True,
#         return_dict=True,
#         return_tensors="pt"
#     )

#     inputs = {
#         key: value.to(device)
#         for key, value in inputs.items()
#     }

#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=1500,
#         do_sample=False
#     )

#     generated_tokens = outputs[
#         0
#     ][
#         inputs["input_ids"].shape[-1]:
#     ]

#     answer = tokenizer.decode(
#         generated_tokens,
#         skip_special_tokens=True
#     )

#     return answer