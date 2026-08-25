import hmac

from gdo.base.Application import Application
from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_Object import GDT_Object
from gdo.core.GDT_String import GDT_String
from gdo.oracle.GDO_OracleAnswer import GDO_OracleAnswer
from gdo.oracle.GDO_OracleQuestion import GDO_OracleQuestion
from gdo.oracle.OracleQuestionToken import OracleQuestionToken
from gdo.table.MethodQueryTable import MethodQueryTable
from gdo.ui.GDT_Error import GDT_Error


class answers(MethodQueryTable):
    """View the answers to one question through its opaque access token."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return ''

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_Object('question').table(GDO_OracleQuestion.table()).not_null().positional(),
            GDT_String('passcode_hash').ascii().case_s().minlen(64).maxlen(64).not_null().positional(),
        ]

    def get_question(self) -> GDO_OracleQuestion:
        return self.param_value('question')

    def has_valid_passcode(self) -> bool:
        return hmac.compare_digest(OracleQuestionToken.for_question(self.get_question()), self.param_val('passcode_hash'))

    def gdo_table(self) -> GDO:
        return GDO_OracleAnswer.table()

    def gdo_table_headers(self) -> list[GDT]:
        table = self.gdo_table()
        return [
            table.column('oca_user'),
            table.column('oca_text'),
            table.column('oca_created'),
        ]

    def gdo_table_query(self):
        return self.gdo_table().select().where(f'oca_question={self.get_question().get_id()}')

    def gdo_order_default(self):
        return 'oca_created ASC'

    def gdo_paginated(self) -> bool:
        return False

    def gdo_execute(self) -> GDT:
        if not self.has_valid_passcode():
            return GDT_Error().text('err_oracle_answers_access')
        if Application.is_html():
            self.gdo_module().add_meta(
                f'<meta http-equiv="refresh" content="{self.gdo_module().cfg_refresh_timeout()}">')
        return super().gdo_execute()
