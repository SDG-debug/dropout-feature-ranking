import numpy as np
import pandas as pd
import torch.nn as nn

from .MLPLoaderBase import MLPLoaderBase


class MiniBooNE(MLPLoaderBase):
    '''
    Data specific loader to define nn_test and nn_rank.
    ::: test func: return {name, val}
    ::: rank func: return {rank}
    '''
    def __init__(self, mode='classification', **kwargs):
        kwargs['mode'] = mode
        super(MiniBooNE, self).__init__(**kwargs)

    def init_hyperamaters(self):
        return {
            'dimensions': [50, 150, 100, 50, 25, 2],
            'epochs': 100,
            'epoch_print': 1,
            'weight_lr': 1e-3,
            'lookahead': 6,
            'lr_patience': 2,
            'verbose': 1,
            'weight_decay': 1e-4,
            'loss_criteria': nn.CrossEntropyLoss(),
        }

    def init_bdnet_hyperparams(self):
        return {
            'reg_coef': 0.01,
            'ard_init': 0.,
            'lr': 0.002,
            'verbose': 1,
            'epochs': 150,
            'epoch_print': 10,
            'rw_max': 30,
            'loss_criteria': nn.CrossEntropyLoss(),
        }

    def _load_data(self, testfold=4):
        x = pd.read_csv('data/MiniBooNE/x.csv').values
        y = pd.read_csv('data/MiniBooNE/y.csv').values.ravel()
        x = x.astype(np.float32)
        y = y.astype(np.int64)

        alltrainset, testset = self.split_train_and_test((x, y), testfold=testfold)

        # Cut 10% as validation set for NN
        trainset, valset = self.split_valset(alltrainset, ratio=0.1)

        return alltrainset, trainset, valset, testset

    def get_top_indices(self):
        return [1, 2, 5, 10, 20, 30, 50]

    def _get_random_sample_hyperparams(self):
        return {'dimensions': self.hyper_params['dimensions']}
        # n_hidden = np.random.randint(50, 200)
        # n_layers = np.random.randint(0, 5)
        #
        # dimensions = [50, 2]
        # for i in range(n_layers):
        #     dimensions.insert(1, n_hidden)
        #
        # return {'dimensions': dimensions}