import torch
from transformers import BertTokenizer, BertForSequenceClassification

LABEL_COLUMNS = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']

path = "./app/model_weights/local_model"
class BertModerator:
    def __init__(self, weights_path, name, num_labels=6, max_length=128, device='cpu'):
        self.base_name = name
        self.device = device
        self.model = BertForSequenceClassification.from_pretrained(path)
        self.tokenizer = BertTokenizer.from_pretrained(path)
        #self.model.load_state_dict(torch.load(weights_path))
        self.model.to(device)
        self.max_length = max_length
        self.num_labels = num_labels

    def predict(self, text: str):
        self.model.to(self.device)
        LABEL_COLUMNS = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
        tokens = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        tokens = {key: val.to(self.device) for key, val in tokens.items()}

        with torch.no_grad():
            outputs = self.model(**tokens)
            logits = outputs.logits
            probabilities = torch.sigmoid(logits).cpu().numpy()[0]

        print(probabilities)
        return probabilities
