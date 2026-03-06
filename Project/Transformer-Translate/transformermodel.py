# Author: Sean W
# 2026年03月06日15时05分47秒
# wanjx0701@gmail.com
import math
from typing import List

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sklearn
import pandas as pd
import os
import sys
import time
from tqdm.auto import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F
from dataclasses import dataclass
from typing import Optional, Tuple

Tensor = torch.Tensor
# print(sys.version_info)
# for module in mpl, np, pd, sklearn, torch:
#     print(module.__name__, module.__version__)

device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
print(device)

seed = 42
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)
np.random.seed(seed)


class PositionalEmbedding(nn.Module):
    def __init__(self, d_model, max_len):
        super().__init__()
        pe = torch.zeros(max_len, d_model)

        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * -(torch.log(torch.Tensor([10000.0])) / d_model))

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        x = x + self.pe[:, :x.size(1)]
        return x


class TransformerEmbedding(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.vocab_size = config['vocab_size']
        self.d_model = config['d_model']
        self.pad_idx = config['pad_idx']
        dropout_rate = config['dropout']
        self.max_length = config['max_length']

        # 词嵌入层 (Word Embedding),将单词索引转换为稠密向量,设置padding_idx可以让pad的词向量全为0
        self.word_embedding = nn.Embedding(self.vocab_size, self.d_model, padding_idx=self.pad_idx)

        # 位置嵌入层 (Position Embedding)
        self.pos_embedding = PositionalEmbedding(self.d_model, self.max_length)

        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, input_ids):
        # input_ids.shape = [batch, seq_len]
        seq_len = input_ids.shape[1]
        assert (
                    seq_len <= self.max_length), f"input sequence length should no more than {self.max_length} but got {seq_len}"

        word_embeds = self.word_embedding(input_ids)  # word_embeds.shape = [batch, seq_len, d_model]
        word_embeds = self.pos_embedding(word_embeds)  # add positional embeds

        embeds = self.dropout(word_embeds)

        return embeds


@dataclass
class AttentionOutput:
    hidden_states: Tensor
    attn_scores: Tensor


class MultiHeadAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.head_nums = config['num_heads']
        self.d_model = config['d_model']
        assert(self.d_model % self.head_nums == 0), (
            "Hidden size must be divisible by num_heads but got {} and {}".format(self.d_model, self.head_nums))

        self.head_dim = self.d_model // self.head_nums

        self.Wq = nn.Linear(self.d_model, self.d_model, bias=False)     # 第二个self.d_model可以*系数
        self.Wk = nn.Linear(self.d_model, self.d_model, bias=False)
        self.Wv = nn.Linear(self.d_model, self.d_model, bias=False)
        self.Wo = nn.Linear(self.d_model, self.d_model, bias=False)     # 输出层

    def forward(self, Q, K, V, attn_mask=None) -> AttentionOutput:
        batch_size = Q.shape[0]
        Q = self.Wq(Q)      # Q.shape = [batch, seq_len, d_model] -> [batch, seq_len, d_model]
        K = self.Wk(K)
        V = self.Wv(V)

        # 分头    Q.shape = [batch, seq_len, d_model] -> [batch, seq_len, head_nums, head_dim]
        #                                            -> [batch, head_nums, seq_len, head_dim]
        Q = Q.view(batch_size, -1, self.head_nums, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, -1, self.head_nums, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, -1, self.head_nums, self.head_dim).transpose(1, 2)

        # 计算缩放点积注意力
        scores = torch.matmul(Q, K.transpose(-1, -2)) / math.sqrt(self.head_dim)
        # scores.shape = [batch, head_nums, seq_len, seq_len]

        if attn_mask is not None:
            # attn_mask = attn_mask[:, None, None, :]   # [batch, seq_len] 扩展到 [batch_size, 1, 1, seq_len]
            scores = scores.masked_fill(attn_mask, -1e9)

        attn_scores = torch.softmax(scores, dim=-1)     # attn_scores.shape = [batch, head_num, seq_lem, seq_len]
        output = torch.matmul(attn_scores, V)           # output.shape = [batch, head_num, seq_len, head_dim]

        output = output.transpose(1, 2).contiguous()    # output.shape = [batch, seq_len, num_heads, head_dim]
        output = output.view(batch_size, -1, self.d_model)         # output.shape = [batch, seq_len, d_model]
        output = self.Wo(output)

        return AttentionOutput(hidden_states=output, attn_scores=attn_scores)


@dataclass
class TransformerBlockOutput:
        hidden_states: Tensor
        self_attn_scores: Tensor
        cross_attn_scores: Optional[Tensor] = None


class TransformerBlock(nn.Module):
    def __init__(self, config, add_cross_attention=False):
        super().__init__()

        self.d_model = config['d_model']
        self.num_heads = config['num_heads']
        dropout_rate = config['dropout']
        ffn_dim = config['dim_feedforward']
        eps = config['layer_norm_eps']      # 层归一化的epsilon值

        self.self_attn = MultiHeadAttention(config)
        self.self_layer_norm = nn.LayerNorm(self.d_model, eps=eps)
        self.self_dropout = nn.Dropout(dropout_rate)

        if add_cross_attention:
            self.cross_attn = MultiHeadAttention(config)
            self.cross_layer_norm = nn.LayerNorm(self.d_model, eps=eps)
            self.cross_dropout = nn.Dropout(dropout_rate)
        else:
            self.cross_attn = None

        self.ffn = nn.Sequential(
            nn.Linear(self.d_model, ffn_dim),
            nn.ReLU(),
            nn.Linear(ffn_dim, self.d_model),
        )
        self.ffn_layer_norm = nn.LayerNorm(self.d_model, eps=eps)
        self.ffn_dropout = nn.Dropout(dropout_rate)

    def forward(self, embeds, self_attn_mask=None, encoder_outputs=None, cross_attn_mask=None) -> TransformerBlockOutput:

        self_attn_output = self.self_attn(embeds, embeds, embeds, attn_mask=self_attn_mask)
        embeds = embeds + self.self_dropout(self_attn_output.hidden_states)
        embeds = self.self_layer_norm(embeds)

        if self.cross_attn is not None:
            assert encoder_outputs is not None
            cross_attn_output = self.cross_attn(embeds, encoder_outputs, encoder_outputs, cross_attn_mask)
            embeds = embeds + self.cross_dropout(cross_attn_output.hidden_states)
            embeds = self.cross_layer_norm(embeds)

        ffn_output = self.ffn(embeds)
        embeds = self.ffn_layer_norm(embeds + self.ffn_dropout(ffn_output))

        return TransformerBlockOutput(
            hidden_states=embeds,
            self_attn_scores=self_attn_output.attn_scores,
            cross_attn_scores=cross_attn_output.attn_scores if self.cross_attn is not None else None
        )


@dataclass
class TransformerEncoderOutput:
    last_hidden_states: Tensor
    attn_scores: List[Tensor]


class TransformerEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()

        self.num_layers = config['num_encoder_layers']
        self.layers = nn.ModuleList(
            [TransformerBlock(config) for _ in range(self.num_layers)]
        )

    def forward(self, encoder_input_embeds, attn_mask=None) -> TransformerEncoderOutput:
        attn_scores = []
        embeds = encoder_input_embeds
        for layer in self.layers:
            block_output = layer(embeds, self_attn_mask=attn_mask)
            embeds = block_output.hidden_states         # 在每个层的输出中，提取了隐藏状态 block_outputs.hidden_states
            attn_scores.append(block_output.self_attn_scores)   # 将对应的注意力分数 block_outputs.self_attn_scores 添加到列表 attn_scores 中

        return TransformerEncoderOutput(
            last_hidden_states=embeds, attn_scores=attn_scores
        )


@dataclass
class TransformerDecoderOutput:
    last_hidden_states: Tensor
    self_attn_scores: List[Tensor]
    cross_attn_scores: List[Tensor]


class TransformerDecoder(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.num_layers = config['num_decoder_layers']
        self.layers = nn.ModuleList(
            [TransformerBlock(config, add_cross_attention=True) for _ in range(self.num_layers)]
        )

    def forward(self, decoder_input_embeds, encoder_output, self_attn_mask=None, cross_attn_mask=None) -> TransformerDecoderOutput:
        self_attn_scores = []
        cross_attn_scores = []
        embeds = decoder_input_embeds
        for layer in self.layers:
            block_output = layer(embeds, self_attn_mask=self_attn_mask, encoder_outputs=encoder_output, cross_attn_mask=cross_attn_mask)
            embeds = block_output.hidden_states
            self_attn_scores.append(block_output.self_attn_scores)
            cross_attn_scores.append(block_output.cross_attn_scores)

        return TransformerDecoderOutput(
            last_hidden_states=embeds,
            self_attn_scores=self_attn_scores,
            cross_attn_scores=cross_attn_scores
        )


@dataclass
class TransformerOutput:
    logits: Tensor
    encoder_last_hidden_states: Tensor
    decoder_last_hidden_states: Tensor
    encoder_attn_scores: List[Tensor]
    decoder_self_attn_scores: List[Tensor]
    decoder_cross_attn_scores: List[Tensor]
    preds: Optional[Tensor] = None


class TransformerModel(nn.Module):
    def __init__(self, config):
        super().__init__()

        self.d_model = config['d_model']
        self.num_encoder_layers = config['num_encoder_layers']
        self.num_decoder_layers = config['num_decoder_layers']
        self.pad_idx = config['pad_idx']
        self.bos_idx = config['bos_idx']
        self.eos_idx = config['eos_idx']
        self.vocab_size = config['vocab_size']
        self.dropout_rate = config['dropout']
        self.max_length = config['max_length']
        self.share = config['shar_embedding']

        self.src_embedding = TransformerEmbedding(config)
        if self.share:              # 源和目标的嵌入层相同，共享参数，节省内存
            self.trg_embedding = self.src_embedding     # 源和目标的嵌入层相同，共享参数，节省内存
            # 输出层，共享参数，直接拿原有embedding矩阵的转置，节省内存
            self.linear = lambda x : torch.matmul(x, self.trg_embedding.word_embedding.weight.t())
        else:
            self.trg_embedding = TransformerEmbedding(config)
            self.linear = nn.Linear(self.d_model, self.vocab_size)

        self.encoder = TransformerEncoder(config)
        self.decoder = TransformerDecoder(config)

        self._init_weights()

    def _init_weights(self):
        """
        使用 xavier 均匀分布来初始化权重
        """
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)

    def generate_square_subsequent_mask(self, sz: int) -> Tensor:
        """
        这个掩码用于自回归解码，确保：
        每个位置只能看到它之前（包括自己）的位置，不能看到未来的位置
        """
        mask = torch.triu(torch.ones(sz, sz), diagonal=1).bool()
        return mask

    def forward(self, encoder_inputs, decoder_inputs, encoder_inputs_mask=None) -> TransformerOutput:
        # encoder_inputs: [batch_size, src_len]
        # decoder_inputs: [batch_size, trg_len]
        # encoder_inputs_mask: [batch_size, src_len]
        if encoder_inputs_mask is None:
            encoder_inputs_mask = encoder_inputs.eq(self.pad_idx)       # [batch_size, src_len]
        encoder_inputs_mask = encoder_inputs_mask.unsqueeze(1).unsqueeze(2)     # [batch_size, 1, 1, src_len],用于encoder的自注意力,用于encoder的自注意力

        decoder_inputs_mask = decoder_inputs.eq(self.pad_idx)  # [batch_size, trg_len]
        decoder_inputs_mask = decoder_inputs_mask.unsqueeze(1).unsqueeze(2)  # [batch_size, 1, 1, trg_len]

        look_ahead_mask = self.generate_square_subsequent_mask(decoder_inputs.shape[1])     # trg_len, trg_len]
        look_ahead_mask = look_ahead_mask.unsqueeze(0).unsqueeze(0).to(decoder_inputs.device)     # [1, 1, trg_len, trg_len],用于decoder的自注意力

        # [batch_size, 1, 1, trg_len]与[1, 1, trg_len, trg_len]相加，得到decoder的自注意力mask
        decoder_inputs_mask = decoder_inputs_mask | look_ahead_mask     # [batch_size, 1, trg_len, trg_len]

        # encoding
        encoder_inputs_embeds = self.src_embedding(encoder_inputs)
        encoder_outputs = self.encoder(encoder_inputs_embeds, encoder_inputs_mask)

        # decoding
        decoder_inputs_embeds = self.trg_embedding(decoder_inputs)
        decoder_outputs = self.decoder(decoder_inputs_embeds, encoder_outputs.last_hidden_states,
                                       self_attn_mask=decoder_inputs_mask, cross_attn_mask=encoder_inputs_mask)

        logits = self.linear(decoder_outputs.last_hidden_states)    # [batch_size, trg_len, vocab_size]

        return TransformerOutput(
            logits=logits,
            encoder_last_hidden_states=encoder_outputs.last_hidden_states,
            decoder_last_hidden_states=decoder_outputs.last_hidden_states,
            encoder_attn_scores=encoder_outputs.attn_scores,
            decoder_self_attn_scores=decoder_outputs.self_attn_scores,
            decoder_cross_attn_scores=decoder_outputs.cross_attn_scores
        )

    @torch.no_grad()
    def infer(self, encoder_inputs, encoder_inputs_mask=None) -> TransformerOutput:
        # encoder_inputs [batch_size, src_len]
        # assert len(encoder_inputs_mask.shape) == 2 and encoder_inputs.shape[0] == 1,只对单样本推理
        if encoder_inputs_mask is None:
            encoder_inputs_mask = encoder_inputs.eq(self.pad_idx)

        # [batch_size, 1, 1, src_len],[batch_size,src_len]相加时，会自动广播到[batch_size,1,src_len,src_len]
        encoder_inputs_mask = encoder_inputs_mask.unsqueeze(1).unsqueeze(2)

        look_ahead_mask = self.generate_square_subsequent_mask(self.max_length)
        look_ahead_mask = look_ahead_mask.unsqueeze(0).unsqueeze(0).to(encoder_inputs.device)    # [1, 1, trg_len, trg_len]

        # encoding
        encoder_inputs_embeds = self.src_embedding(encoder_inputs)
        encoder_outputs = self.encoder(encoder_inputs_embeds, encoder_inputs_mask)

        # decoding
        decoder_inputs = Tensor([self.bos_idx] * encoder_inputs.shape[0]).reshape(-1, 1).long().to(device=encoder_inputs.device)
        for cur_len in tqdm(range(1, self.max_length + 1)):
            decoder_inputs_embeds = self.trg_embedding(decoder_inputs)
            decoder_outputs = self.decoder(decoder_inputs_embeds, encoder_outputs.last_hidden_states,
                                           self_attn_mask=look_ahead_mask[:, :, :cur_len, :cur_len],
                                           cross_attn_mask=encoder_inputs_mask)
            logits = self.linear(decoder_outputs.last_hidden_states)
            next_token = logits.argmax(dim=-1)[:, -1:]
            decoder_inputs = torch.cat([decoder_inputs, next_token], dim=-1)    # 预测输出拼接到输入中
            if all((decoder_inputs == self.eos_idx).sum(dim=-1) > 0):
                break

        return TransformerOutput(
            preds=decoder_inputs[:, 1:],
            logits=logits,
            encoder_last_hidden_states=encoder_outputs.last_hidden_states,
            decoder_last_hidden_states=decoder_outputs.last_hidden_states,
            encoder_attn_scores=encoder_outputs.attn_scores,
            decoder_self_attn_scores=decoder_outputs.self_attn_scores,
            decoder_cross_attn_scores=decoder_outputs.cross_attn_scores
        )




if __name__ == '__main__':
    import torch
    import torch.nn as nn

    # ===== 1 配置 =====
    config = {
        "vocab_size": 20,
        "d_model": 32,
        "num_heads": 4,
        "dim_feedforward": 64,
        "num_encoder_layers": 2,
        "num_decoder_layers": 2,
        "dropout": 0.1,
        "max_length": 10,
        "pad_idx": 0,
        "bos_idx": 1,
        "eos_idx": 2,
        "layer_norm_eps": 1e-5,
        "shar_embedding": True
    }

    model = TransformerModel(config)

    # ===== 2 单条训练数据 =====
    src = torch.tensor([[5, 6, 7, 8, 2]])  # 输入
    tgt = torch.tensor([[1, 8, 7, 6, 5, 2]])  # 目标 (BOS + reversed + EOS)

    criterion = nn.CrossEntropyLoss(ignore_index=0)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    # ===== 3 训练 =====
    for step in range(300):

        out = model(src, tgt[:, :-1])

        logits = out.logits.reshape(-1, config["vocab_size"])
        labels = tgt[:, 1:].reshape(-1)

        loss = criterion(logits, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if step % 50 == 0:
            print("step:", step, "loss:", loss.item())

    # ===== 4 推理测试 =====
    pred = model.infer(src).preds
    print("prediction:", pred)

    attn = out.decoder_self_attn_scores[0]

    print(attn.shape)
    print(attn[0, 0])

    print(out.logits.shape)
    print(out.decoder_self_attn_scores[0].shape)
    print(out.decoder_self_attn_scores[0][0, 0])

