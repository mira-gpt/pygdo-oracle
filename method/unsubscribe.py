from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDO_Permission import GDO_Permission
from gdo.oracle.GDO_OracleSubscription import GDO_OracleSubscription


class unsubscribe(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'oracle.unsubscribe'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'oc.unsub'

    def gdo_method_hidden(self) -> bool:
        return True

    def gdo_in_private(self) -> bool:
        return False

    def gdo_user_permission(self) -> str | None:
        return GDO_Permission.VOICE

    def gdo_execute(self) -> GDT:
        channel = self._env_channel
        if subscription := GDO_OracleSubscription.table().get_by_vals({
            'ocs_channel': channel.get_id(),
        }):
            subscription.delete()
            return self.reply('msg_oracle_unsubscribed', (channel.render_name(),))
        return self.reply('msg_oracle_not_subscribed', (channel.render_name(),))
