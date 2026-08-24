from gdo.base.GDT import GDT
from gdo.base.Application import Application
from gdo.base.Method import Method
from gdo.core.GDT_RestOfText import GDT_RestOfText
from gdo.oracle.GDO_OracleQuestion import GDO_OracleQuestion
from gdo.oracle.OracleQuestionToken import OracleQuestionToken
from gdo.base.IPC import IPC


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
            'ocq_asker': self._env_user.get_id(),
            'ocq_language': self._env_user.get_lang_iso(),
            'ocq_channel': self._env_channel.get_id() if self._env_channel else None,
            'ocq_text': self.param_value('question'),
        }).insert()
        IPC.send_to_dog('oracle.ipc_question', [question.get_id()])
        if Application.IS_HTTP:
            return self.redirect(self.gdo_module().href(
                'answers', positional=(question.get_id(), OracleQuestionToken.for_question(question))))
        return self.reply('msg_oracle_asked', (question.get_id(),))
