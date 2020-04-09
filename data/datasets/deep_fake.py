import os
import cv2
import json
from glob import glob
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

from data import transform


class DeepFakeDataset(Dataset):
    def __init__(self, folder, transform=None):
        self.folder = folder
        self.images_list = glob(os.path.join(self.folder, '*.jpg'))
        self.len = len(self.images_list)
        self.transform = transform
        self.annotation_path = os.path.join(self.folder, 'annotation.json')
        with open(self.annotation_path) as f:
            self.annotation = json.load(f)

    def __len__(self):
        return self.len

    def load_image(self, image_name):
        image = cv2.imread(image_name)
        return image

    def __getitem__(self, index):
        image_name = self.images_list[index]
        label = self.annotation[image_name]
        img = self.load_image(self.images_list[index])
        sample = {'images' : img,
                  'labels' : [0, label] if label else [1, 0]}
        if self.transform:
            sample = self.transform(sample)
        return sample


def get_deepfake_train(config):
    test_loader = DataLoader(DeepFakeDataset(folder=config['train']['folder'],
                                             transform=transform.Transforms(config['input_size'], train=True)),
                             batch_size=config['train']['batch_size'],
                             shuffle=False,
                             num_workers=config['num_workers'])


def get_deepfake_val(config):
    test_loader = DataLoader(DeepFakeDataset(folder=config['validation']['folder'],
                                             transform=transform.Transforms(config['input_size'], train=False)),
                             batch_size=config['validation']['batch_size'],
                             shuffle=False,
                             num_workers=config['num_workers'])