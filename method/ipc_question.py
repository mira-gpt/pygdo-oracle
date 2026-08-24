from gdo.base.Application import Application
from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.Trans import tiso
from gdo.core.GDT_Object import GDT_Object
from gdo.oracle.GDO_OracleQuestion import GDO_OracleQuestion
from gdo.oracle.GDO_OracleSubscription import GDO_OracleSubscription


class ipc_question(Method):
    """Dog-only fan-out for a persisted Oracle question."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return ''

    def gdo_parameters(self) -> list[GDT]:
        return [GDT_Object('question').table(GDO_OracleQuestion.table()).not_null().positional()]

    async def gdo_execute(self) -> GDT:
        if not (Application.IS_DOG or Application.is_unit_test()):
            return self.empty()
        question = self.param_value('question')
        text = tiso(question.gdo_val('ocq_language'), 'msg_oracle_question', (
            question.get_id(), question.gdo_value('ocq_asker').render_name(),
            question.gdo_val('ocq_text'),
        ))
        for subscription in GDO_OracleSubscription.table().select().exec():
            await subscription.gdo_value('ocs_channel').send(text)
        return self.empty()
