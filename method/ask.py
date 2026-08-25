from gdo.base.GDT import GDT
from gdo.base.Application import Application
from gdo.core.GDT_RestOfText import GDT_RestOfText
from gdo.form.GDT_Form import GDT_Form
from gdo.form.MethodForm import MethodForm
from gdo.language.GDT_Language import GDT_Language
from gdo.oracle.GDO_OracleQuestion import GDO_OracleQuestion
from gdo.oracle.OracleQuestionToken import OracleQuestionToken
from gdo.base.IPC import IPC


class ask(MethodForm):
    @classmethod
    def gdo_trigger(cls) -> str:
        return 'oracle.ask'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'oc.ask'

    def gdo_method_hidden(self) -> bool:
        return True

    def gdo_create_form(self, form: GDT_Form) -> None:
        # In chat, preserve the concise `$oracle.ask <question>` syntax and
        # take the connector user's language. The web form can deliberately
        # select the language in which responders should read the question.
        if Application.IS_HTTP:
            form.add_field(
                GDT_Language('language').supported().not_null()
                .initial(self._env_user.get_lang_iso()))
        form.add_field(GDT_RestOfText('question').not_null().max(4096))
        super().gdo_create_form(form)

    async def form_submitted(self) -> GDT:
        language = self.param_val('language') if Application.IS_HTTP else self._env_user.get_lang_iso()
        question = GDO_OracleQuestion.blank({
            'ocq_asker': self._env_user.get_id(),
            'ocq_language': language,
            'ocq_channel': self._env_channel.get_id() if self._env_channel else None,
            'ocq_text': self.param_value('question'),
        }).insert()
        IPC.send_to_dog('oracle.ipc_question', [question.get_id()])
        if Application.IS_HTTP:
            return self.redirect(self.gdo_module().href(
                'answers', positional=(question.get_id(), OracleQuestionToken.for_question(question))))
        return self.reply('msg_oracle_asked', (question.get_id(),))
