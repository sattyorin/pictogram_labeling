import abc

import numpy as np


class ISearcher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_keywords(self, query_image_path: str) -> np.ndarray:
        raise NotImplementedError()
