from django.contrib.auth.models import User


class QuestionFetcher():
    """

    """
    def __init__(
        self,
        user: User,
        data_provider_name: str
    ):
        self.user = user
        self.data_provider = get_data_provider_by_name(data_provider_name)
