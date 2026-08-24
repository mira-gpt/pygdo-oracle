from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.Render import Mode
from gdo.oracle.GDO_OracleQuestion import GDO_OracleQuestion
from gdo.table.MethodQueryTable import MethodQueryTable


class questions(MethodQueryTable):
    """Public web overview of persisted Oracle questions."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'oracle.questions'

    def gdo_table(self) -> GDO:
        return GDO_OracleQuestion.table()

    def gdo_table_headers(self) -> list[GDT]:
        table = self.gdo_table()
        return [
            table.column('ocq_id'),
            table.column('ocq_text'),
        ]

    def gdo_order_default(self):
        return 'ocq_created DESC'

    def gdo_paginate_size(self) -> int:
        return 5

    def render_gdo(self, question: GDO_OracleQuestion, mode: Mode) -> str:
        return f'{question.get_id()}-{question.gdo_val("ocq_text")}'
