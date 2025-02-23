from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
)

from typing import Any, Iterable

MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT"

class BioClinicalBert:

    def __init__(self, model_name: str = MODEL_NAME, num_labels: int = 2, max_length: int = 128) -> None:
        self.model_name = model_name
        self.num_labels = num_labels
        self.max_length = max_length
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertForSequenceClassification.from_pretrained(self.model_name, num_labels=self.num_labels)
    
    def tokenize(self, examples: Iterable[str], text_column_name: str = "sentence") -> Any:
        return self.tokenizer(
            examples[text_column_name],
            padding="max_length",
            truncation=True, 
            max_length=self.max_length
        )
