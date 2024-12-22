#import torch
from transformers import BertTokenizer, BertForSequenceClassification

LABEL_COLUMNS = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']


#
# class BertModerator:
#     def __init__(self, weights_path, name, num_labels=6, max_length=128, device='cpu'):
#         self.base_name = name
#         self.device = device
#         self.model = BertForSequenceClassification.from_pretrained(weights_path, num_labels=len(self.num_labels))
#         self.tokenizer = BertTokenizer.from_pretrained(name)
#         self.max_length = max_length
#         self.num_labels = num_labels
#         self.model.to(self.device)
#
#     def predict(self, text: str) -> int:
#         self.model.to(self.device)
#         LABEL_COLUMNS = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
#         tokens = self.tokenizer(
#             text,
#             max_length=self.max_length,
#             padding="max_length",
#             truncation=True,
#             return_tensors="pt"
#         )
#         tokens = {key: val.to(self.device) for key, val in tokens.items()}
#
#         with torch.no_grad():
#             outputs = self.model(**tokens)
#             logits = outputs.logits
#             probabilities = torch.sigmoid(logits).cpu().numpy()[0]
#
#         print(probabilities)
#         result = {label: prob for label, prob in zip(LABEL_COLUMNS, probabilities)}
#         return result
