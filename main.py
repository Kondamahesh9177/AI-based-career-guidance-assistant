import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset
import os

 
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


df = pd.read_csv(r"C:\Users\konda\Downloads\career_guidance_dataset (1).csv")


df["Interest_Label"] = df["Interest Area"].astype("category").cat.codes


train_texts, val_texts, train_labels, val_labels = train_test_split(
    df["Interest Area"], df["Interest_Label"], test_size=0.2, random_state=42
)


tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

train_encodings = tokenizer(list(train_texts), truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(list(val_texts), truncation=True, padding=True, max_length=128)


class CareerDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])  
        return item


train_dataset = CareerDataset(train_encodings, train_labels.tolist())
val_dataset = CareerDataset(val_encodings, val_labels.tolist())


model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased", num_labels=len(df["Interest_Label"].unique())
)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=True,
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

trainer.train()


model.save_pretrained("career_bert_model")
tokenizer.save_pretrained("career_bert_model")
print(" Model trained and saved successfully!")
