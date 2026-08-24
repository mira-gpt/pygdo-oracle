"""Stable bearer token for the single-question Oracle web view."""

import hashlib
import hmac


class OracleQuestionToken:

    @staticmethod
    def for_question(question) -> str:
        from gdo.user.module_user import module_user
        pepper = module_user.instance().cfg_user_link_pepper().encode()
        payload = f'oracle.answers|{question.get_id()}'
        return hmac.new(pepper, payload.encode(), hashlib.sha256).hexdigest()
