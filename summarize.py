import transformers
from summarizer import Summarizer

from transformers import AutoTokenizer, AutoModel, AutoConfig, pipeline
from vos_request import Playable

uds = Playable("00102200330")
text = uds.subtitles
print(text)


from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Danish-summarisation/dansum-mt5-base-v1")

model = AutoModelForSeq2SeqLM.from_pretrained("Danish-summarisation/dansum-mt5-base-v1")


# use bart in pytorch
sum = pipeline("summarization", model = model, tokenizer = tokenizer)


# config = AutoConfig.from_pretrained('allenai/scibert_scivocab_uncased')
# config.output_hidden_states=True
# tokenizer = AutoTokenizer.from_pretrained("Maltehb/danish-bert-botxo")
# model = AutoModel.from_pretrained("Maltehb/danish-bert-botxo", config=config, ignore_mismatched_sizes=True)

# sum = Summarizer(custom_model=model, custom_tokenizer=tokenizer)
# sum = Summarizer()
# print (sum(text))

print (sum(text, min_length=100))
