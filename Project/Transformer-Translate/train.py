# Author: Sean W
# 2026年03月07日17时07分41秒
# wanjx0701@gmail.com

from tokenizer import *
from dataloader import *
from transformermodel import TransformerModel
from trainfunc import *
from callback import *

import os
from torch.utils.data import DataLoader
from functools import partial  # 固定collate_fct的tokenizer参数

exp_name = 'en-de-translate'

# 构造词表
word2idx, idx2word = get_word_idx_vocab()
vocab_size = len(word2idx)

# HyperParameters for training
config = {
    'bos_idx': 1,
    'eos_idx': 2,
    'pad_idx': 0,
    'vocab_size': vocab_size,       # 词汇表大小,决定了词嵌入矩阵的大小，影响模型容量和内存使用
    'max_length': 128,              # 最大序列长度, 限制输入/输出序列长度，影响位置编码和计算复杂度
    'batch_size': 4096,             # 批量大小
    'd_model': 512,                 # 模型的维度，即词嵌入的维度 *
    'num_heads': 8,                # 多头注意力的头数  *
    'dropout': 0.1,                 # dropout 概率    *
    'dim_feedforward': 2048,        # FFN 的隐藏层大小    *
    'layer_norm_eps': 1e-6,         # 层归一化的 epsilon, 防止除零错误
    'num_encoder_layers': 6,        # 编码器层数 *
    'num_decoder_layers': 6,        # 解码器层数 *
    'label_smoothing': 0.1,         # 标签平滑的超参数  *
    'beta1': 0.9,                   # Adam的一阶矩估计衰减率
    'beta2': 0.98,                   # Adam的一阶矩估计衰减率
    'eps': 1e-9,                    # Adam 的 epsilon, 防止除零错误
    'warmup_steps': 4000,           # 学习率预热步数   *
    'share_embedding': False,       # 是否共享词向量   *
}

# dataset
train_ds = LangPairDataset('train', max_length=config['max_length'])
val_ds = LangPairDataset('val', max_length=config['max_length'])

# tokenizer
tokenizer = Tokenizer(word2idx, idx2word, max_length=config['max_length'])

# dataloader
sampler = TransformerBatchSampler(train_ds, batch_size=config['batch_size'], shuffle_batch=True, clip_last_batch=False)
train_dl = DataLoader(train_ds, batch_sampler=sampler, collate_fn=partial(collate_fct, tokenizer=tokenizer))

sampler = TransformerBatchSampler(val_ds, batch_size=config['batch_size'], shuffle_batch=False, clip_last_batch=False)
val_dl = DataLoader(val_ds, batch_sampler=sampler, collate_fn=partial(collate_fct, tokenizer=tokenizer))

# model
model = TransformerModel(src_vocab=config['vocab_size'],
                         tgt_vocab=config['vocab_size'],
                         d_model=config['d_model'],
                         layers=config['num_encoder_layers'],
                         heads=config['num_heads'],
                         dropout=config['dropout'],
                         ffn_hidden=config['dim_feedforward'],
                         max_len=config['max_length'],
                         pad_idx=config['pad_idx'],
                         )

# print(model)    # 打印模型结构
print(f'Total params: {sum(p.numel() for p in model.parameters() if p.requires_grad)}')  # 打印可训练参数数量

# epochs
epochs = 100

# 损失函数
loss_func = CrossEntropyWithpadding(config)

# 优化器
optimizer, scheduler = get_optimizer(model, config)

# callbacks
if not os.path.exists('checkpoints'):
    os.makedirs('checkpoints')
save_ckpt_callback = SaveCheckpointCallback(f'checkpoints/{exp_name}', save_step=500, save_best_only=True)
early_stop_callback = EarlyStopCallback(patience=10, min_delta=1e-3)


# ====================================== start train ==========================================
model = model.to(device)

record = training(model,
                  train_dl,
                  val_dl,
                  epochs,
                  loss_func,
                  optimizer,
                  scheduler=scheduler,
                  save_ckpt_callback=save_ckpt_callback,
                  early_stop_callback=early_stop_callback,
                  eval_step=500
                  )









