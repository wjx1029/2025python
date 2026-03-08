# Author: Sean W
# 2026年03月06日22时14分49秒
# wanjx0701@gmail.com
import torch
import torch.nn as nn
import math


class PositionalEncoding(nn.Module):

    def __init__(self, d_model, max_len=5000):
        super().__init__()

        pe = torch.zeros(max_len, d_model)

        position = torch.arange(0, max_len).unsqueeze(1)

        div_term = torch.exp(
            torch.arange(0, d_model, 2) * -(math.log(10000.0) / d_model)
        )

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        pe = pe.unsqueeze(0)  # [1,max_len,d_model]

        self.register_buffer("pe", pe)

    def forward(self, x):

        # x [batch, seq_len, d_model]

        seq_len = x.size(1)

        return x + self.pe[:, :seq_len]


class TransformerEmbedding(nn.Module):

    def __init__(self, vocab_size, d_model, max_len, dropout, pad_idx):

        super().__init__()

        self.embedding = nn.Embedding(vocab_size, d_model, padding_idx=pad_idx)

        self.position = PositionalEncoding(d_model, max_len)

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):

        # x [batch, seq_len]

        x = self.embedding(x)

        x = self.position(x)

        return self.dropout(x)


def scaled_dot_product_attention(Q, K, V, mask=None):

    # Q,K,V
    # [batch, heads, seq, head_dim]

    d_k = Q.size(-1)

    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)

    # scores
    # [batch, heads, seq, seq]

    if mask is not None:
        scores = scores.masked_fill(mask, -1e9)

    attn = torch.softmax(scores, dim=-1)

    output = torch.matmul(attn, V)

    return output, attn


class MultiHeadAttention(nn.Module):

    def __init__(self, d_model, num_heads):

        super().__init__()

        assert d_model % num_heads == 0

        self.num_heads = num_heads
        self.head_dim = d_model // num_heads

        self.Wq = nn.Linear(d_model, d_model)
        self.Wk = nn.Linear(d_model, d_model)
        self.Wv = nn.Linear(d_model, d_model)

        self.Wo = nn.Linear(d_model, d_model)

    def forward(self, Q, K, V, mask=None):

        batch_size = Q.size(0)

        # linear

        Q = self.Wq(Q)
        K = self.Wk(K)
        V = self.Wv(V)

        # split heads
        # [batch, seq, d_model] -> [batch, heads, seq, head_dim]

        Q = Q.view(batch_size, -1, self.num_heads, self.head_dim).transpose(1,2)
        K = K.view(batch_size, -1, self.num_heads, self.head_dim).transpose(1,2)
        V = V.view(batch_size, -1, self.num_heads, self.head_dim).transpose(1,2)

        output, attn = scaled_dot_product_attention(Q,K,V,mask)

        # concat heads

        output = output.transpose(1, 2).contiguous()

        output = output.view(batch_size, -1, self.num_heads*self.head_dim)

        output = self.Wo(output)

        return output, attn


class FeedForward(nn.Module):

    def __init__(self, d_model, hidden, dropout):

        super().__init__()

        self.net = nn.Sequential(

            nn.Linear(d_model, hidden),

            nn.ReLU(),

            nn.Dropout(dropout),

            nn.Linear(hidden, d_model)
        )

    def forward(self, x):

        return self.net(x)


class EncoderLayer(nn.Module):

    def __init__(self, d_model, heads, ffn_hidden, dropout):

        super().__init__()

        self.attn = MultiHeadAttention(d_model, heads)

        self.norm1 = nn.LayerNorm(d_model)

        self.ffn = FeedForward(d_model, ffn_hidden, dropout)

        self.norm2 = nn.LayerNorm(d_model)

        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask):

        attn_out, _ = self.attn(x,x,x,mask)

        x = self.norm1(x + self.dropout(attn_out))

        ffn_out = self.ffn(x)

        x = self.norm2(x + self.dropout(ffn_out))

        return x


class DecoderLayer(nn.Module):

    def __init__(self, d_model, heads, ffn_hidden, dropout):

        super().__init__()

        self.self_attn = MultiHeadAttention(d_model, heads)

        self.norm1 = nn.LayerNorm(d_model)

        self.cross_attn = MultiHeadAttention(d_model, heads)

        self.norm2 = nn.LayerNorm(d_model)

        self.ffn = FeedForward(d_model, ffn_hidden, dropout)

        self.norm3 = nn.LayerNorm(d_model)

        self.dropout = nn.Dropout(dropout)

    def forward(self, x, enc_out, src_mask, tgt_mask):

        attn_out,_ = self.self_attn(x, x, x, tgt_mask)

        x = self.norm1(x + self.dropout(attn_out))

        attn_out,_ = self.cross_attn(x,enc_out,enc_out,src_mask)

        x = self.norm2(x + self.dropout(attn_out))

        ffn_out = self.ffn(x)

        x = self.norm3(x + self.dropout(ffn_out))

        return x


class Encoder(nn.Module):

    def __init__(self, vocab_size, d_model, layers, heads, ffn_hidden, dropout, max_len, pad_idx):

        super().__init__()

        self.embedding = TransformerEmbedding(
            vocab_size, d_model, max_len, dropout, pad_idx
        )

        self.layers = nn.ModuleList(
            [EncoderLayer(d_model,heads,ffn_hidden,dropout) for _ in range(layers)]
        )

    def forward(self, x, mask):

        x = self.embedding(x)

        for layer in self.layers:
            x = layer(x, mask)

        return x


class Decoder(nn.Module):

    def __init__(self, vocab_size, d_model, layers, heads, ffn_hidden, dropout, max_len, pad_idx):

        super().__init__()

        self.embedding = TransformerEmbedding(
            vocab_size,d_model,max_len,dropout,pad_idx
        )

        self.layers = nn.ModuleList(
            [DecoderLayer(d_model,heads,ffn_hidden,dropout) for _ in range(layers)]
        )

        self.fc = nn.Linear(d_model, vocab_size)

    def forward(self, x, enc_out, src_mask, tgt_mask):

        x = self.embedding(x)

        for layer in self.layers:
            x = layer(x, enc_out, src_mask, tgt_mask)

        return self.fc(x)


class TransformerModel(nn.Module):

    def __init__(
        self,
        src_vocab,
        tgt_vocab,
        d_model=512,
        layers=6,
        heads=8,
        ffn_hidden=2048,
        dropout=0.1,
        max_len=512,
        pad_idx=0
    ):

        super().__init__()

        self.encoder = Encoder(
            src_vocab,d_model,layers,heads,ffn_hidden,dropout,max_len,pad_idx
        )

        self.decoder = Decoder(
            tgt_vocab,d_model,layers,heads,ffn_hidden,dropout,max_len,pad_idx
        )

        self.pad_idx = pad_idx

    def make_src_mask(self, src):

        mask = (src == self.pad_idx)

        return mask.unsqueeze(1).unsqueeze(2)

    def make_tgt_mask(self, tgt):

        batch, seq = tgt.shape

        pad_mask = (tgt == self.pad_idx).unsqueeze(1).unsqueeze(2)

        look_ahead = torch.triu(torch.ones(seq,seq),1).bool().to(tgt.device)

        look_ahead = look_ahead.unsqueeze(0).unsqueeze(0)

        return pad_mask | look_ahead

    def forward(self, src, tgt):

        src_mask = self.make_src_mask(src)

        tgt_mask = self.make_tgt_mask(tgt)

        enc_out = self.encoder(src, src_mask)

        out = self.decoder(tgt, enc_out, src_mask, tgt_mask)

        return out

    @torch.no_grad()
    def infer(self, src, bos_idx, eos_idx, max_len=128):

        # src [batch, src_len]

        device = src.device
        batch_size = src.size(0)

        src_mask = self.make_src_mask(src)

        # encoder
        enc_out = self.encoder(src, src_mask)

        # decoder input <bos>
        tgt = torch.full((batch_size, 1), bos_idx, dtype=torch.long).to(device)

        for _ in range(max_len):

            tgt_mask = self.make_tgt_mask(tgt)

            out = self.decoder(tgt, enc_out, src_mask, tgt_mask)

            # logits of last token
            logits = out[:, -1, :]

            next_token = torch.argmax(logits, dim=-1, keepdim=True)

            tgt = torch.cat([tgt, next_token], dim=1)

            # stop if all finished
            if (next_token == eos_idx).all():
                break

        return tgt[:, 1:]



