from abc import abstractmethod, ABC
from src.models.db_models import Post, User
from src.models.models import PostRequest


class BaseRepo(ABC):

    @abstractmethod
    def save_users(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def save_posts(self, post: Post) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_posts(self, post_request: PostRequest) -> list[Post]:
        raise NotImplementedError
