from transformers import AutoTokenizer, AutoModel
import torch

def get_embedding(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).cpu().numpy().flatten()


def model_select(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    global model, tokenizer
    if model_name == "sentence-transformers/all-MiniLM-L6-v2":
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)

    return model, tokenizer