from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Channel import GDT_Channel
from gdo.core.GDT_Creator import GDT_Creator
from gdo.core.GDT_Unique import GDT_Unique
from gdo.date.GDT_Created import GDT_Created


class GDO_OracleSubscription(GDO):
    """One channel that receives Oracle questions."""

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('ocs_id'),
            GDT_Channel('ocs_channel').not_null().cascade_delete(),
            GDT_Creator('ocs_creator').not_null(),
            GDT_Created('ocs_created'),
            GDT_Unique('unique_oracle_channel').unique_columns('ocs_channel'),
        ]
