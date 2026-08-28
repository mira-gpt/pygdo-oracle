from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.GDO_Module import GDO_Module
from gdo.date.GDT_Duration import GDT_Duration
from gdo.oracle.GDO_OracleAnswer import GDO_OracleAnswer
from gdo.oracle.GDO_OracleQuestion import GDO_OracleQuestion
from gdo.oracle.GDO_OracleSubscription import GDO_OracleSubscription
from gdo.ui.GDT_Link import GDT_Link
from gdo.ui.GDT_Page import GDT_Page


class module_oracle(GDO_Module):
    """Relay questions from a channel to subscribed oracle channels."""

    def gdo_classes(self) -> list[type[GDO]]:
        return [
            GDO_OracleSubscription,
            GDO_OracleQuestion,
            GDO_OracleAnswer,
        ]

    def gdo_module_config(self) -> list[GDT]:
        return [
            GDT_Duration('refresh_timeout').not_null().initial('7s'),
        ]

    def gdo_init_sidebar(self, page: GDT_Page):
        page._left_bar.add_field(
            GDT_Link().href(self.href('ask')).text('link_oracle_ask').icon('oracle'))

    def cfg_refresh_timeout(self) -> int:
        return self.get_config_value('refresh_timeout')
