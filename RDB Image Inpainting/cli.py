# cli.py
import argparse
import logging
from preprocessing.preprocessor import ImagePreprocessor
from models.inpainting import InpaintingRDN
from data.dataset import load_and_preprocess_dataset
from training.trainer import ModelTrainer
from config import default_config

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def preprocess(args, logger):
    processor = ImagePreprocessor()
    try:
        total, rgb = processor.process_dataset(args.input_dir, args.output_dir)
        logger.info(f"\nDataset Processing Complete:")
        logger.info(f"Total images processed: {total}")
        logger.info(f"RGB images saved: {rgb}")
        logger.info(f"Images filtered out: {total - rgb}")
        logger.info(f"\nRGB images saved to: {args.output_dir}")
        return 0
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        return 1

def train(args, logger):
    config = default_config.copy()
    config.update({
        'epochs': args.epochs,
        'batch_size': args.batch_size,
        'save_path': args.output
    })

    try:
        dataset = load_and_preprocess_dataset(
            args.dataset_path,
            image_size=config['image_size'],
            batch_size=config['batch_size']
        )

        model = InpaintingRDN(
            num_channels=config['num_channels'],
            num_rdbs=config['num_rdbs'],
            layers_per_rdb=config['layers_per_rdb']
        )

        trainer = ModelTrainer(config)
        model = trainer.train(model, dataset)
        
        logger.info("Training completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        return 1

def main():
    parser = argparse.ArgumentParser(description='Image Inpainting Tools')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Preprocessing command
    preprocess_parser = subparsers.add_parser('preprocess', help='Preprocess image dataset')
    preprocess_parser.add_argument('input_dir', help='Input directory containing images')
    preprocess_parser.add_argument('output_dir', help='Output directory for processed images')

    # Training command
    train_parser = subparsers.add_parser('train', help='Train inpainting model')
    train_parser.add_argument('dataset_path', help='Path to training dataset')
    train_parser.add_argument('--output', default='image_inpainting_model.h5',
                            help='Path to save trained model')
    train_parser.add_argument('--epochs', type=int, default=50,
                            help='Number of training epochs')
    train_parser.add_argument('--batch-size', type=int, default=32,
                            help='Batch size for training')

    args = parser.parse_args()
    setup_logging()
    logger = logging.getLogger(__name__)

    if args.command == 'preprocess':
        return preprocess(args, logger)
    elif args.command == 'train':
        return train(args, logger)

if __name__ == '__main__':
    exit(main())


