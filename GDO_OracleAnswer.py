from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Index import GDT_Index
from gdo.core.GDT_Object import GDT_Object
from gdo.core.GDT_Text import GDT_Text
from gdo.core.GDT_User import GDT_User
from gdo.date.GDT_Created import GDT_Created
from gdo.oracle.GDO_OracleQuestion import GDO_OracleQuestion


class GDO_OracleAnswer(GDO):
    """A persisted answer authored by one user for an Oracle question."""

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('oanswer_id'),
            GDT_Object('oanswer_question').table(GDO_OracleQuestion.table()).not_null().cascade_delete(),
            GDT_User('oanswer_user').not_null(),
            GDT_Text('oanswer_text').not_null().max(4096),
            GDT_Created('oanswer_created'),
            GDT_Index('oracle_answer_question').index_fields('oanswer_question', 'oanswer_created'),
        ]
