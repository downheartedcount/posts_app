from abc import abstractmethod, ABC
from typing import List
from src.models.db_models import Post
from src.models.models import PostRequest


class BaseClient(ABC):

    @abstractmethod
    def fetch_posts(self) -> None:
        raise NotImplementedError

    def get_posts(self, post_request: PostRequest) -> List[Post]:
        raise NotImplementedError
