import os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import csv


ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'artifacts')
CSV_FILE = os.path.join(ARTIFACTS_DIR, 'dataset.csv')

SHORT_MODEL_NAME = "flan-t5-small"  # flan-t5-small, flan-t5-base, flan-t5-large, flan-t5-xl, flan-t5-xxl
MODEL_NAME = "google/" + SHORT_MODEL_NAME
MAX_LEN = 50


class ModelRunner(object):
    def __init__(self, model_name, temperature):
        self.model_name = model_name
        self.temperature = temperature
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def run_model(self, prompt, num_return_sequences):
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        gen_tokens = self.model.generate(
            input_ids,
            do_sample=True,
            temperature=self.temperature,
            max_length=MAX_LEN,
            num_return_sequences=num_return_sequences)
        return [self.tokenizer.decode(gen_token, skip_special_tokens=True) for gen_token in gen_tokens]


def set_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    # When running on the CuDNN backend, two further options must be set
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def get_tests(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def main():
    set_seed(42)
    tests = get_tests(CSV_FILE)

    temperature = 0.00001
    runner = ModelRunner(MODEL_NAME, temperature)
    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0
    for test in tests:
        if int(test['move_count']) != 2:
            continue
        print(test)
        model_result = runner.run_model(test['prompt'], 1)[0]
        if model_result.startswith('no'):
            if test['expected'] == 'Yes':
                false_negative += 1
            if test['expected'] == 'No':
                true_negative += 1
        elif model_result.startswith('yes'):
            if test['expected'] == 'Yes':
                true_positive += 1
            if test['expected'] == 'No':
                false_positive += 1
        else:
            print(f'Unrecognized answer: {model_result}')
    print(f'True positive: {true_positive}, False positive: {false_positive}')
    print(f'True negative: {true_negative}, False negative: {false_negative}')


if __name__ == '__main__':
    main()
