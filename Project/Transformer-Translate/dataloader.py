# Author: Sean W
# 2026年03月05日23时07分32秒
# wanjx0701@gmail.com


from torch.utils.data import BatchSampler
import numpy as np
import torch

from langpairdataset import LangPairDataset
from tokenizer import Tokenizer


device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")

class SampleInfo:
    def __init__(self, i, lens):
        """
        记录文本对的序号和长度信息
        输入：
            - i (int): 文本对的序号。
            - lens (list): 文本对源语言和目标语言的长度
        """
        self.i = i
        self.max_len = max(lens) + 1
        self.src_len = lens[0] + 1
        self.trg_len = lens[1] + 1


class TokenBatchCreator:
    def __init__(self, batch_size):
        """
        参数:
        batch_size (int): 用于限制批量的大小。
        功能:
        初始化了一个空的批量列表 _batch。
        设定了初始的最大长度为 -1。
        存储了传入的 batch_size。
        """
        self._batch = []                # 这个就是之前的batch_size，就是第一个batch内有多少个样本
        self.max_len = -1
        self._batch_size = batch_size   # 限制批量的大小,假设是4096

    def append(self, info: SampleInfo):
        """
        参数:
        info (SampleInfo): 文本对的信息。
        功能:
        接收一个 SampleInfo 对象，并根据其最大长度信息更新当前批量的最大长度。
        如果将新的样本加入批量后超过了批量大小限制，它会返回已有的批量并将新的样本加入新的批量。
        否则，它会更新最大长度并将样本添加到当前批量中。
        """
        # 更新当前批量的最大长度
        cur_len = info.max_len      # 当前样本的长度
        max_len = max(self.max_len, info.max_len)   # 每来一个样本，更新当前批次的最大长度
        # 如果新的样本加入批量后超过大小限制，则将已有的批量返回，新的样本加入新的批量
        if max_len * (len(self._batch) + 1) > self._batch_size:
            result = self._batch
            self._batch = []
            self._batch.append(info)
            self.max_len = cur_len
            return result
        else:
            self._batch.append(info)
            self.max_len = max_len
            return None

    @property
    def batch(self):
        return self._batch


class TransformerBatchSampler(BatchSampler):
    def __init__(self, dataset, batch_size=4096, shuffle_batch=False, clip_last_batch=False, seed=0):
        """
        批量采样器
        输入:
            - dataset: 数据集
            - batch_size: 批量大小
            - shuffle_batch: 是否对生成的批量进行洗牌
            - clip_last_batch: 是否裁剪最后剩下的数据
            - seed: 随机数种子
        """
        self._dataset = dataset
        self._batch_size = batch_size
        self._shuffle_batch = shuffle_batch
        self._clip_last_batch = clip_last_batch
        self._seed = seed
        self._random = np.random
        self._random.seed(seed)

        self._sample_infos = []
        # 根据数据集中的每个样本，创建了对应的 SampleInfo 对象，包含了样本的索引和长度信息。
        for i, data in enumerate(self._dataset):
            lens = [len(data[0]), len(data[1])]
            self._sample_infos.append(SampleInfo(i, lens))

    def __iter__(self):
        """
        ### 迭代器 ###
        对数据集中的样本进行排序，排序规则是先按源语言长度排序，如果相同则按目标语言长度排序。
        使用 TokenBatchCreator 逐步组装批量数据，当满足批量大小时返回一个批量的样本信息。
        如果不裁剪最后一个批次的数据且存在剩余样本，则将这些样本组成最后一个批次。
        如果需要对批量进行洗牌，则对批次进行洗牌操作。
        通过迭代器，抛出每个批量的样本在数据集中的索引。
        """

        # 排序，如果源语言长度相同则按照目标语言的长度排列
        infos = sorted(self._sample_infos, key=lambda info: (info.src_len, info.trg_len))

        batch_infos = []
        batch_creator = TokenBatchCreator(self._batch_size)

        for info in infos:
            batch = batch_creator.append(info)
            if batch is not None:
                batch_infos.append(batch)

        # 是否抛弃最后批量的文本对
        if not self._clip_last_batch and len(batch_creator.batch) != 0:
            batch_infos.append(batch_creator.batch) # 最后一个batch

        # 是否打乱batch
        if self._shuffle_batch:
            self._random.shuffle(batch_infos)

        self.batch_number = len(batch_infos)
        # print("batch_number: {}".format(self.batch_number))

        # 抛出一个批量的文本对在数据集中的序号
        for batch in batch_infos:
            batch_indices = [info.i for info in batch]  # 批量的样本在数据集中的索引，第一个batch[0,1,.....82]，第二个batch[83,84,85,86,87]
            yield batch_indices

    def __len__(self):
        if hasattr(self, "batch_number"):
            return self.batch_number
        batch_number = (len(self._dataset) + self._batch_size) // self._batch_size
        return batch_number


def collate_fct(batch, tokenizer:Tokenizer):
    src_words = [pair[0].split() for pair in batch]
    trg_words = [pair[1].split() for pair in batch]

    # [BOS] src [EOS] [PAD]
    encoder_inputs, encoder_inputs_mask = tokenizer.encode(
        src_words, padding_first=False, add_bos=True, add_eos=True, return_mask=True)

    # [BOS] trg [PAD]
    decoder_inputs = tokenizer.encode(
        trg_words, padding_first=False, add_bos=True, add_eos=False, return_mask=False)

    # trg [EOS] [PAD]
    decoder_labels, decoder_labels_mask = tokenizer.encode(
        trg_words, padding_first=False, add_bos=False, add_eos=True, return_mask=True
    )

    return {
        "encoder_inputs": encoder_inputs.to(device=device),
        "encoder_inputs_mask": encoder_inputs_mask.to(device=device),
        "decoder_inputs": decoder_inputs.to(device=device),
        "decoder_labels": decoder_labels.to(device=device),
        "decoder_labels_mask": decoder_labels_mask.to(device=device),
    }


if __name__ == '__main__':
    print(device)

    train_ds = LangPairDataset("train")
    sampler = TransformerBatchSampler(train_ds, batch_size=4096, shuffle_batch=True)
    print('batch sample done')
    for idx, batch in enumerate(sampler):
        print("第{}批量的数据中含有文本对是：{}，数量为：{}".format(idx, batch, len(batch)))
        print("第{}批量的数据长度是：{}".format(idx, [len(train_ds[idx][0]) for idx in batch]))
        print("第{}批量的数据长度是：{}".format(idx, [len(train_ds[idx][1]) for idx in batch]))
        if idx >= 2:
            break

    print("-" * 150)
    from functools import partial  # 固定collate_fct的tokenizer参数
    from torch.utils.data import BatchSampler, DataLoader
    from tokenizer import get_word_idx_vocab

    word2idx, idx2word = get_word_idx_vocab()
    tokenizer = Tokenizer(word2idx=word2idx, idx2word=idx2word)
    sampler = TransformerBatchSampler(train_ds, batch_size=256, shuffle_batch=True)
    sample_dl = DataLoader(train_ds, batch_sampler=sampler, collate_fn=partial(collate_fct, tokenizer=tokenizer))


    for batch in sample_dl:
        for key, value in batch.items():
            print(key)
            print(value)
        break