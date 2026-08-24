from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Channel import GDT_Channel
from gdo.core.GDT_Index import GDT_Index
from gdo.core.GDT_Text import GDT_Text
from gdo.core.GDT_User import GDT_User
from gdo.date.GDT_Created import GDT_Created


class GDO_OracleQuestion(GDO):
    """A question and the channel to which its answers are relayed."""

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('oquestion_id'),
            GDT_User('oquestion_asker').not_null(),
            # Web questions have no chat channel. Their answers are persisted
            # and rendered by the web view instead.
            GDT_Channel('oquestion_channel').cascade_delete(),
            GDT_Text('oquestion_text').not_null().max(4096),
            GDT_Created('oquestion_created'),
            GDT_Index('oracle_question_channel').index_fields('oquestion_channel', 'oquestion_created'),
        ]
