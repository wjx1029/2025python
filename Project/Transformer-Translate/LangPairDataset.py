# Author: Sean W
# 2026年03月05日20时54分46秒
# wanjx0701@gmail.com

from pathlib import Path
from torch.utils.data import Dataset
import numpy as np


class LangPairDataset(Dataset):
    def __init__(self, mode='train', max_length=128, overwrite_cache=False, data_dir='wmt16'):
        self.data_dir = Path(data_dir)
        cache_path = self.data_dir / ".cache" / f"de2en_{mode}_{max_length}.npy"

        if overwrite_cache or not cache_path.exists():  # 重新覆盖缓存或缓存路径不存在
            cache_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.data_dir / f"{mode}_src.bpe", "r", encoding="utf-8") as file:
                self.src = file.readlines()     # 去掉句子前后的空格

            with open(self.data_dir / f"{mode}_trg.bpe", "r", encoding="utf-8") as file:
                self.trg = file.readlines()

            filtered_src = []
            filtered_trg = []
            for src, trg in zip(self.src, self.trg):
                if len(src) <= max_length and len(trg) <= max_length:   # 过滤长度超过最大长度的句子
                    filtered_src.append(src.strip())            # 去掉句子前后的空格
                    filtered_trg.append(trg.strip())

            filtered_src = np.array(filtered_src)
            filtered_trg = np.array(filtered_trg)
            self.src = filtered_src
            self.trg = filtered_trg
            print(f"Filtered data: {len(filtered_src)} pairs")

            # allow_pickle=True允许保存对象数组，将过滤后的数据保存为 NumPy 数组，存储在缓存文件中
            np.save(cache_path, {'src' : filtered_src, 'trg' : filtered_trg}, allow_pickle=True)
            print(f"Saved filtered data to {cache_path}")

        else:
            cache_dict = np.load(cache_path, allow_pickle=True).item()
            self.src = cache_dict['src']
            self.trg = cache_dict['trg']
            print(f"Load {mode} dataset from {cache_path},     length : {len(self.src)} pairs")

    def __getitem__(self, idx):
        return self.src[idx], self.trg[idx]

    def __len__(self):
        return len(self.src)


if __name__ == '__main__':
    train_ds = LangPairDataset('train',max_length=192)
    val_ds = LangPairDataset('val',max_length=192)
    test_ds = LangPairDataset('test',max_length=192)

    print('-' * 50)
    print("source: {}\ntarget: {}".format(*train_ds[0]))
    print(train_ds[0])