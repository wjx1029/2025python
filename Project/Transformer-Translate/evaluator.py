# Author: Sean W
# 2026年03月07日19时03分01秒
# wanjx0701@gmail.com

from tokenizer import *
from dataloader import *
from transformermodel import TransformerModel
from trainfunc import *
from callback import *
from torch.utils.data import DataLoader
from functools import partial

from nltk.translate.bleu_score import sentence_bleu
import torch


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

state_dict = torch.load(f"best.ckpt", map_location="cpu")

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

model.load_state_dict(state_dict)

loss_func = CrossEntropyWithpadding(config)

tokenizer = Tokenizer(word2idx, idx2word, max_length=config['max_length'])

test_ds = LangPairDataset('test', max_length=config['max_length'], data_dir='wmt16')
test_dl = DataLoader(test_ds, batch_size=1, collate_fn=partial(collate_fct, tokenizer=tokenizer))

model = model.to(device)
model.eval()
collect = {}
loss_collect = []
bleu_scores = []

for idx, batch in tqdm(enumerate(test_dl)):

    encoder_inputs = batch['encoder_inputs'].to(device)
    decoder_inputs = batch['decoder_inputs'].to(device)
    encoder_inputs_mask = batch['encoder_inputs_mask'].to(device)
    decoder_labels = batch['decoder_labels'].to(device)

    with torch.no_grad():

        # 用 teacher forcing 算 loss
        outputs = model(encoder_inputs, decoder_inputs)

        logits = outputs

        decoder_padding_mask = decoder_labels.eq(config["pad_idx"])
        loss = loss_func(logits, decoder_labels, decoder_padding_mask)

        # 用 autoregressive 算 BLEU
        infer_outputs = model.infer(encoder_inputs, config['bos_idx'], config['eos_idx'], max_len=config['max_length'])
        preds = infer_outputs

    loss_collect.append(loss.item())

    preds_text = tokenizer.decode(preds.cpu().numpy())[0]
    labels_text = tokenizer.decode(decoder_labels.cpu().numpy())[0]

    bleu_score = sentence_bleu(
        [labels_text.split()],
        preds_text.split(),
        weights=(0.25, 0.25, 0.25, 0.25)
    )

    bleu_scores.append(bleu_score)

    collect[idx] = {'loss': loss.cpu().item(),
                    'src_inputs': encoder_inputs,
                    'trg_inputs': decoder_inputs,
                    'mask': encoder_inputs_mask,
                    'trg_labels': decoder_labels,
                    'preds': preds
                    }

collect = sorted(collect.items(), key=lambda x: x[1]['loss'])
print(f'testing loss: {np.array(loss_collect).mean()}')
print(f'bleu_score: {np.array(bleu_scores).mean()}')