from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.Render import Mode
from gdo.oracle.GDO_OracleQuestion import GDO_OracleQuestion
from gdo.oracle.OracleQuestionToken import OracleQuestionToken
from gdo.table.MethodQueryTable import MethodQueryTable
from gdo.ui.GDT_Link import GDT_Link


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
            GDT_Link('ocq_text').label('question'),
            table.column('ocq_created'),
        ]

    def gdo_order_default(self):
        return 'ocq_created DESC'

    def gdo_paginate_size(self) -> int:
        return 5

    def render_gdo(self, question: GDO_OracleQuestion, mode: Mode) -> str:
        return f'{question.get_id()}-{question.gdo_val("ocq_text")}'

    def render_ocq_text(self, gdt: GDT_Link, question: GDO_OracleQuestion):
        return gdt.href(self.gdo_module().href(
            'answers', positional=(question.get_id(), OracleQuestionToken.for_question(question)),
        )).text_raw(question.gdo_val('ocq_text')).render()
