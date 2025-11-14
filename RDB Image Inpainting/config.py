default_config = {
    'image_size': (256, 256),
    'batch_size': 8,
    'epochs': 50,
    'learning_rate': 1e-4,
    'early_stopping_patience': 10,
    'lr_reduce_factor': 0.5,
    'lr_reduce_patience': 5,
    'loss_function': 'mse',
    'num_channels': 3,
    'num_rdbs': 3,
    'layers_per_rdb': 3
}