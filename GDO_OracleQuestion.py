from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Channel import GDT_Channel
from gdo.core.GDT_Index import GDT_Index
from gdo.core.GDT_Text import GDT_Text
from gdo.core.GDT_User import GDT_User
from gdo.date.GDT_Created import GDT_Created
from gdo.language.GDT_Language import GDT_Language


class GDO_OracleQuestion(GDO):
    """A question and the channel to which its answers are relayed."""

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('ocq_id'),
            GDT_User('ocq_asker').not_null().label('created'),
            GDT_Language('ocq_language').not_null().label('language'),
            GDT_Channel('ocq_channel').cascade_delete(),
            GDT_Text('ocq_text').not_null().maxlen(4096).label('question'),
            GDT_Created('ocq_created'),
            GDT_Index('oracle_question_channel').index_fields('ocq_channel', 'ocq_created'),
        ]
