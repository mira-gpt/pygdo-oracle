from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_Object import GDT_Object
from gdo.core.GDT_RestOfText import GDT_RestOfText
from gdo.oracle.GDO_OracleAnswer import GDO_OracleAnswer
from gdo.oracle.GDO_OracleQuestion import GDO_OracleQuestion


class answer(Method):
    @classmethod
    def gdo_trigger(cls) -> str:
        return 'oracle.answer'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'oc.answer'

    def gdo_method_hidden(self) -> bool:
        return True

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_Object('q_id').table(GDO_OracleQuestion.table()).not_null(),
            GDT_RestOfText('answer').not_null().max(4096),
        ]

    def get_question(self) -> GDO_OracleQuestion:
        return self.param_value('q_id')

    async def gdo_execute(self) -> GDT:
        question = self.get_question()
        answer = self.param_value('answer')
        GDO_OracleAnswer.blank({
            'oanswer_question': question.get_id(),
            'oanswer_user': self._env_user.get_id(),
            'oanswer_text': answer,
        }).insert()
        # Chat questions receive the answer immediately. For web questions the
        # persisted answer is rendered when the asker opens the Oracle view.
        if channel := question.gdo_value('oquestion_channel'):
            await channel.send(self.t('msg_oracle_answer', (
                question.get_id(), self._env_user.render_name(), answer,
            )))
        return self.reply('msg_oracle_answered', (question.get_id(),))
