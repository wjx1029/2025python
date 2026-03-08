# Author: Sean W
# 2026年03月07日15时40分21秒
# wanjx0701@gmail.com

import numpy as np
import torch
import torch.nn.functional as F
from torch.optim.lr_scheduler import LambdaLR
from torch.optim import Adam
from tqdm.auto import tqdm


class CrossEntropyWithpadding:
    def __init__(self, config):
        self.label_smoothing = config["label_smoothing"]

    def __call__(self, logits, labels, padding_mask):
        # logits: [batch_size, seq_len, vocab_size]
        # labels: [batch_size, seq_len]
        # padding_mask: [batch_size, seq_len]
        bs, seq_len, vocab_size = logits.shape
        logits = logits.view(bs * seq_len, vocab_size)
        labels = labels.view(bs * seq_len)
        loss = F.cross_entropy(logits, labels, reduction='none', label_smoothing=self.label_smoothing)
        # label_smoothing表示随机将一个类别的概率设置为0.1，使得模型更加关注其他类别

        if padding_mask is None:
            loss = loss.mean()
        else:
            # 将padding_mask reshape成一维张量，mask部分为0，非mask部分为1
            padding_mask = (~padding_mask).view(-1).float()
            loss = (loss * padding_mask).sum() / padding_mask.sum()

        return loss


class NoamDecayScheduler:
    def __init__(self, config):
        self.d_model = config['d_model']
        self.warmup_steps = config['warmup_steps']

    def __call__(self, step):
        step += 1
        arg1 = step ** -0.5
        arg2 = step * self.warmup_steps ** -1.5
        arg3 = self.d_model ** -0.5
        return arg3 * np.minimum(arg1, arg2)


def get_optimizer(model, config):
    base_lr = 0.1
    beta1 = config["beta1"]
    beta2 = config["beta2"]
    eps = config["eps"]

    optimizer = Adam(model.parameters(), lr=base_lr, betas=(beta1, beta2), eps=eps)

    lr_scheduler = NoamDecayScheduler(config)
    # 使用 LambdaLR 调度器，它可以根据给定的函数 lr_lambda 调整学习率。这里将 lr_scheduler 作为函数传递给 LambdaLR，它包含了特定于模型或任务的学习率调度规则
    scheduler = LambdaLR(optimizer, lr_lambda=lr_scheduler)

    return optimizer, scheduler


@torch.no_grad()
def evaluating(model, loss_func, data_loader):
    model.eval()
    loss_list = []
    for batch in data_loader:
        encoder_inputs = batch['encoder_inputs']
        encoder_inputs_mask = batch['encoder_inputs_mask']
        decoder_inputs = batch['decoder_inputs']
        decoder_labels = batch['decoder_labels']
        decoder_labels_mask = batch['decoder_labels_mask']

        output = model(encoder_inputs, decoder_inputs)

        logits = output
        loss = loss_func(logits, decoder_labels, padding_mask=decoder_labels_mask)
        loss_list.append(loss.cpu().item())

    return np.mean(loss_list)


def training(model, train_data, val_data, epochs, loss_func, optimizer,
             scheduler=None,
             save_ckpt_callback=None,
             early_stop_callback=None,
             eval_step=500):

    record_dict = {
        "train": [],
        "val": []
    }

    global_step = 1
    model.train()

    with tqdm(total=epochs * len(train_data)) as pbar:
        for epoch in range(epochs):
            for batch in train_data:
                encoder_inputs = batch['encoder_inputs']
                encoder_inputs_mask = batch['encoder_inputs_mask']
                decoder_inputs = batch['decoder_inputs']
                decoder_labels = batch['decoder_labels']
                decoder_labels_mask = batch['decoder_labels_mask']

                # 梯度清空
                optimizer.zero_grad()

                # 前向传播
                output = model(encoder_inputs, decoder_inputs)


                # 计算损失
                logits = output
                loss = loss_func(logits, decoder_labels, padding_mask=decoder_labels_mask)

                # 反向传播
                loss.backward()

                # 更新参数
                optimizer.step()

                # 更新学习率
                if scheduler is not None:
                    scheduler.step()

                # 记录损失
                loss = loss.cpu().item()
                record_dict["train"].append({"loss": loss, "step": global_step})

                # 评估模型
                if global_step % eval_step == 0:
                    val_loss = evaluating(model, loss_func, val_data)
                    record_dict["val"].append({"loss": val_loss, "step": global_step})
                    model.train()

                    if save_ckpt_callback is not None:
                        save_ckpt_callback(global_step, model.state_dict(), metric=-val_loss)

                    if early_stop_callback is not None:
                        early_stop_callback(-val_loss)
                        if early_stop_callback.early_stop:
                            print(f"Early Stop at epoch {epoch} / global_step {global_step}")
                            return record_dict

                global_step += 1
                pbar.update(1)
            pbar.set_postfix({"epoch": epoch, "loss": loss, "val_loss": val_loss})


    return record_dict




