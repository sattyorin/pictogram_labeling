import pathlib
from typing import Any

import keras.models
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import resnet
from tensorflow.keras.preprocessing.image import img_to_array, load_img

from i_searcher import ISearcher

TARGET_SIZE = (64, 64)
INPUT_SHAPE = (*TARGET_SIZE, 3)
COLOR_MODE = "grayscale"
SUFFIX = ".png"
DIR_PATH = "converted_images"

QUERY_PATH = "~/Downloads/lighting.png"


def cos_sim(v1: Any, v2: Any) -> Any:
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


class SimilaritySearch(ISearcher):
    def __init__(
        self,
        dir_path: str,
        model: keras.models,
        target_size: tuple,
        color_mode: str,
    ) -> None:
        self.dir_path = dir_path
        self.model = model
        self.target_size = target_size
        self.color_mode = color_mode

        self.image_path_list = self.get_image_path_list(self.dir_path, SUFFIX)

    def get_image_path_list(self, dir_path: str, suffix: str) -> np.ndarray:
        return np.array(sorted(pathlib.Path(dir_path).glob(f"*{suffix}")))

    def get_keywords(self, query_image_path: str) -> np.ndarray:
        pass

    def train(self):
        pass

    def load_image(self, image_path: str) -> np.ndarray:
        image = load_img(
            image_path, target_size=self.target_size, color_mode=self.color_mode
        )
        image = img_to_array(image)
        if image.shape[-1] == 1:
            image = np.repeat(
                image, 3, axis=-1
            )  # repeat grayscale channel 3 times

        return image

    def load_images_from_image_path_list(
        self, target_size: tuple, color_mode: str
    ) -> np.ndarray:
        images = []
        for img_path in self.image_path_list:
            img = self.load_image(img_path, target_size, color_mode)
            images.append(img)

        return np.array(images)

    def get_features(self, images: np.ndarray) -> np.ndarray:
        preprocessed = resnet.preprocess_input(images)
        return self.model.predict(preprocessed)

    def get_top_n_indexes(array: np.ndarray, num: int) -> np.ndarray:
        idx = np.argpartition(array, -num)[-num:]
        return idx[np.argsort(array[idx])][::-1]

    def show_results(self, indexes: np.ndarray, sims: np.ndarray) -> None:
        rank = 0
        plt.figure(figsize=(20, 20))

        for idx, sim in zip(indexes, sims):
            plt.subplot(3, 3, rank + 1)
            title = f"rank: {rank}, index: {idx}, sim: {sim:.3f}\n"
            title += f"path: {self.image_path_list[idx]}"
            plt.title(title)
            img = load_img(
                self.image_path_list[idx], target_size=self.target_size
            )
            plt.imshow(img)
            rank += 1

        plt.show()


def main():
    model = tf.keras.applications.ResNet152(
        include_top=False,
        # weights="imagenet",
        weights=None,
        input_shape=INPUT_SHAPE,
        pooling="avg",
    )
    searcher = SimilaritySearch(DIR_PATH, model, TARGET_SIZE, COLOR_MODE)
    images = searcher.load_images_from_image_path_list()
    features = searcher.get_features(images)

    query_image = searcher.load_image(QUERY_PATH)
    query_image = np.expand_dims(query_image, axis=0)
    query_feature = searcher.get_features(query_image)[0]

    # query_id = 1
    # query_feature = features[query_id]

    sims = np.array([cos_sim(query_feature, vector) for vector in features])

    indexes = searcher.get_top_n_indexes(sims, 9)

    searcher.show_results(indexes, sims[indexes], TARGET_SIZE)


if __name__ == "__main__":
    main()
