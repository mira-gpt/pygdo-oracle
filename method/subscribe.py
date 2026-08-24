from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDO_Permission import GDO_Permission
from gdo.oracle.GDO_OracleSubscription import GDO_OracleSubscription


class subscribe(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'oracle.subscribe'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'oc.sub'

    def gdo_method_hidden(self) -> bool:
        return True

    def gdo_in_private(self) -> bool:
        return False

    def gdo_user_permission(self) -> str | None:
        return GDO_Permission.VOICE

    def gdo_execute(self) -> GDT:
        if not GDO_OracleSubscription.table().get_by_vals({
            'ocs_channel': self._env_channel.get_id(),
        }):
            GDO_OracleSubscription.blank({
                'ocs_channel': self._env_channel.get_id(),
                'ocs_creator': self._env_user.get_id(),
            }).insert()
        return self.reply('msg_oracle_subscribed', (self._env_channel.render_name(),))
