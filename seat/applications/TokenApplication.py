import logging
from seat.models.token import Token
logger = logging.getLogger(__name__)

class TokenApplication(object):

    """core functionality for interacting with exam entities, abstracts away our models"""

    def get_token_by_id(self, token_id):
        try:
            return Token.objects.get(id=token_id)
        except Exception, error:
            logger.info(str(error))
            raise error

    def is_valid(self, token):
        try:
            token_set = Token.objects.filter(token=token, open=True)
            if not token_set.exists():
                return False
            else:
                return token_set.all()[0]
        except Exception as error:
            logger.warn("conflict while validating token:"+str(error))
            raise error