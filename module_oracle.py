from gdo.base.GDO import GDO
from gdo.base.GDO_Module import GDO_Module
from gdo.oracle.GDO_OracleAnswer import GDO_OracleAnswer
from gdo.oracle.GDO_OracleQuestion import GDO_OracleQuestion
from gdo.oracle.GDO_OracleSubscription import GDO_OracleSubscription


class module_oracle(GDO_Module):
    """Relay questions from a channel to subscribed oracle channels."""

    def gdo_classes(self) -> list[type[GDO]]:
        return [
            GDO_OracleSubscription,
            GDO_OracleQuestion,
            GDO_OracleAnswer,
        ]
