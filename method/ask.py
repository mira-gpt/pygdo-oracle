from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_RestOfText import GDT_RestOfText
from gdo.oracle.GDO_OracleQuestion import GDO_OracleQuestion
from gdo.oracle.GDO_OracleSubscription import GDO_OracleSubscription


class ask(Method):
    @classmethod
    def gdo_trigger(cls) -> str:
        return 'oracle.ask'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'oc.ask'

    def gdo_method_hidden(self) -> bool:
        return True

    def gdo_parameters(self) -> list[GDT]:
        return [GDT_RestOfText('question').not_null().max(4096)]

    async def gdo_execute(self) -> GDT:
        question = GDO_OracleQuestion.blank({
            'oquestion_asker': self._env_user.get_id(),
            'oquestion_channel': self._env_channel.get_id() if self._env_channel else None,
            'oquestion_text': self.param_value('question'),
        }).insert()
        text = self.t('msg_oracle_question', (
            question.get_id(), self._env_user.render_name(), self.param_value('question'),
        ))
        for subscription in GDO_OracleSubscription.table().select().exec().fetch_all():
            await subscription.gdo_value('osub_channel').send(text)
        return self.reply('msg_oracle_asked', (question.get_id(),))
