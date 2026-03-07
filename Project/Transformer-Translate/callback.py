# Author: Sean W
# 2026年03月07日16时05分33秒
# wanjx0701@gmail.com

import os
import numpy as np
import torch


class SaveCheckpointCallback:
    def __init__(self, save_dir, save_step=500, save_best_only=True):
        self.save_step = save_step
        self.save_dir = save_dir
        self.save_best_only = save_best_only
        self.best_metric = -np.inf

        # mkdir
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)

    def __call__(self, step, state_dict, metric=None):
        if step % self.save_step == 0:
            if self.save_best_only:
                assert metric is not None
                if metric >= self.best_metric:
                    torch.save(state_dict, os.path.join(self.save_dir, 'best.ckpt'))
                    self.best_metric = metric
            else:
                torch.save(state_dict, os.path.join(self.save_dir, 'step_{}.ckpt'.format(step)))


class EarlyStopCallback:
    def __init__(self, patience=5, min_delta=0.01):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_metric = - np.inf

    def __call__(self, metric):
        if metric > self.best_metric + self.min_delta:
            self.counter = 0
            self.best_metric = metric
        else:
            self.counter += 1

    @ property
    def early_stop(self):
        return self.counter >= self.patience