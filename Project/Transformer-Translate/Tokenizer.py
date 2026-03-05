# Author: Sean W
# 2026年03月05日21时35分31秒
# wanjx0701@gmail.com

from tqdm.auto import tqdm
import torch

# Tokenizer
# 这里有两种处理方式，分别对应着 encoder 和 decoder 的 word embedding 是否共享，这里实现共享的方案


def get_word_idx_vocab(threshold=1):  # 出现次数低于threshold的token舍弃
    word2idx = {
        "[PAD]": 0,
        "[BOS]": 1,
        "[EOS]": 2,
        "[UNK]": 3
    }

    idx2word = {idx: word for word, idx in word2idx.items()}

    index = len(idx2word)

    # vocab是token出现的次数，共有18000多个词
    with open("wmt16/vocab", "r", encoding="utf-8") as file:
        for line in tqdm(file.readlines()):
            token, count = line.strip().split()
            if int(count) > threshold:
                word2idx[token] = index
                idx2word[index] = token
                index += 1

    return word2idx, idx2word


class Tokenizer:
    def __init__(self, word2idx, idx2word, max_length=128, pad_idx=0, bos_idx=1, eos_idx=2, unk_idx=3):
        self.word2idx = word2idx
        self.idx2word = idx2word
        self.max_length = max_length
        self.pad_idx = pad_idx
        self.bos_idx = bos_idx
        self.eos_idx = eos_idx
        self.unk_idx = unk_idx

    def encode(self, text_list, padding_first=False, add_bos=True, add_eos=True, return_mask=False):
        max_length = min(self.max_length, add_bos + add_eos + max([len(text) for text in text_list]))
        idx_list = []
        for text in text_list:
            idx = [self.word2idx.get(word, self.unk_idx) for word in text[:max_length - add_bos - add_eos]]
            if add_bos:
                idx = [self.bos_idx] + idx
            if add_eos:
                idx = idx + [self.eos_idx]
            if padding_first:
                idx = [self.pad_idx] * (max_length - len(idx)) + idx
            else:
                idx = idx + [self.pad_idx] * (max_length - len(idx))

            idx_list.append(idx)

        input_ids = torch.tensor(idx_list)
        mask = (input_ids == self.pad_idx).to(dtype=torch.int64)

        return input_ids if not return_mask else (input_ids, mask)

    def decode(self, idx_list, remove_bos=True, remove_eos=True, remove_pad=True, split=False):
        text_list = []
        for indices in idx_list:
            text = []
            for idx in indices:
                if remove_bos and idx == self.bos_idx:
                    continue
                if remove_eos and idx == self.eos_idx:
                    break
                if remove_pad and idx == self.pad_idx:
                    continue
                text.append(self.idx2word.get(idx, "[UNK]"))
            if not split:
                text = " ".join(text)
            text_list.append(text)

        return text_list


if __name__ == '__main__':
    word2idx, idx2word = get_word_idx_vocab()
    vocab_size = len(word2idx)
    print("vocab_size : {}".format(vocab_size))

    print('-' * 100)

    tokenizer = Tokenizer(word2idx=word2idx, idx2word=idx2word)

    raw_text = ["hello world".split(), "tokenize text datas with batch".split(), "this is a test".split()]
    indices, masks = tokenizer.encode(raw_text, padding_first=True, add_bos=True, add_eos=True, return_mask=True)
    decode_text = tokenizer.decode(indices.tolist(), remove_bos=True, remove_eos=True, remove_pad=True, split=False)

    print("raw text")
    for raw in raw_text:
        print(raw)
    print("indices")
    for index in indices:
        print(index)
    print("masks")
    for mask in masks:
        print(mask)
    print("decode text")
    for decode in decode_text:
        print(decode)
