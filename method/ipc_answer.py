from gdo.base.Application import Application
from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.Trans import tiso
from gdo.core.GDT_Object import GDT_Object
from gdo.oracle.GDO_OracleAnswer import GDO_OracleAnswer


class ipc_answer(Method):
    """Dog-only routing for a persisted Oracle answer."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return ''

    def gdo_parameters(self) -> list[GDT]:
        return [GDT_Object('answer').table(GDO_OracleAnswer.table()).not_null().positional()]

    async def gdo_execute(self) -> GDT:
        if not (Application.IS_DOG or Application.is_unit_test()):
            return self.empty()
        answer = self.param_value('answer')
        question = answer.gdo_value('oca_question')
        if channel := question.gdo_value('ocq_channel'):
            text = tiso(question.gdo_val('ocq_language'), 'msg_oracle_answer', (
                question.get_id(), answer.gdo_value('oca_user').render_name(), answer.gdo_val('oca_text'),
            ))
            await channel.send(text)
        return self.empty()
