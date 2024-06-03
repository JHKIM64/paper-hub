from transformers import AutoTokenizer, AutoModel
import torch

# openai 사용시
    # openai.api_key = '~~~  sectret key ~~~'
    # def get_embedding_openai(text):
    #     response = openai.Embedding.create(
    #         input=text,
    #         model="text-embedding-ada-002"
    #     )
    #     return response['data'][0]['embedding']
def get_embedding(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).cpu().numpy().flatten()


def model_select(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    global model, tokenizer
    # mteb sota
    # https://huggingface.co/nvidia/NV-Embed-v1
    # model_name = "nvidia/NV-Embed-v1"

    if model_name == "sentence-transformers/all-MiniLM-L6-v2":
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)

    return model, tokenizer