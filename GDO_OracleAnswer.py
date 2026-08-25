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
            GDT_AutoInc('oca_id'),
            GDT_Object('oca_question').table(GDO_OracleQuestion.table()).not_null().cascade_delete(),
            GDT_User('oca_user').not_null().label('creator'),
            GDT_Text('oca_text').not_null().maxlen(4096).label('answer'),
            GDT_Created('oca_created'),
            GDT_Index('oracle_answer_question').index_fields('oca_question', 'oca_created'),
        ]
