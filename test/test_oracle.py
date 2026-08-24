import os
from unittest.mock import AsyncMock, patch

from gdo.base.Application import Application
from gdo.base.IPC import IPC
from gdo.base.ModuleLoader import ModuleLoader
from gdo.core.connector.Bash import Bash
from gdo.core.GDO_Channel import GDO_Channel
from gdo.oracle.GDO_OracleAnswer import GDO_OracleAnswer
from gdo.oracle.GDO_OracleQuestion import GDO_OracleQuestion
from gdo.oracle.GDO_OracleSubscription import GDO_OracleSubscription
from gdo.oracle.OracleQuestionToken import OracleQuestionToken
from gdo.oracle.method.answers import answers
from gdotest.TestUtil import GDOTestCase, cli_gizmore, cli_plug, cli_user, reinstall_module
from gdo.table.GDT_Table import GDT_Table
from gdo.ui.GDT_Error import GDT_Error


class OracleTestCase(GDOTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        Application.init(os.path.dirname(__file__ + '/../../../../'))
        Application.init_cli()
        loader = ModuleLoader.instance()
        loader.load_modules_db(True)
        reinstall_module('oracle')
        loader.init_modules(True, True)
        loader.init_cli()
        GDO_OracleAnswer.table().delete_where('1')
        GDO_OracleQuestion.table().delete_where('1')
        GDO_OracleSubscription.table().delete_where('1')
        self.gizmore = cli_gizmore()

    def channel(self):
        return Bash.get_server().get_or_create_channel('test_channel')

    def test_01_subscription_is_idempotent(self):
        first = cli_plug(self.gizmore, '$oracle.subscribe')
        second = cli_plug(self.gizmore, '$oracle.subscribe')
        self.assertIn('now receives Oracle questions', first)
        self.assertIn('now receives Oracle questions', second)
        subscriptions = GDO_OracleSubscription.table().select().exec().fetch_all()
        self.assertEqual(1, len(subscriptions))

    async def test_02_ask_persists_and_relays_question(self):
        cli_plug(self.gizmore, '$oracle.subscribe')
        with patch.object(IPC, 'send_to_dog') as enqueue:
            output = cli_plug(self.gizmore, '$oracle.ask Where is the truth?')
        questions = GDO_OracleQuestion.table().select().exec().fetch_all()
        self.assertEqual(1, len(questions))
        question = questions[0]
        self.assertEqual('Where is the truth?', question.gdo_val('ocq_text'))
        self.assertEqual('en', question.gdo_val('ocq_language'))
        self.assertEqual(self.channel().get_id(), question.gdo_val('ocq_channel'))
        self.assertEqual(64, len(OracleQuestionToken.for_question(question)))
        self.assertIn(f'Oracle question #{question.get_id()} has been sent', output)
        enqueue.assert_called_once_with('oracle.ipc_question', [question.get_id()])
        with patch.object(GDO_Channel, 'send', new_callable=AsyncMock) as send:
            await IPC.execute_dog_event('oracle.ipc_question', [question.get_id()])
        send.assert_awaited_once_with(
            f'Oracle question #{question.get_id()} from gizmore{{bash}}: Where is the truth?')

    async def test_03_answer_persists_and_relays_to_asking_channel(self):
        cli_plug(self.gizmore, '$oracle.subscribe')
        cli_plug(self.gizmore, '$oracle.ask What is the answer?')
        question = GDO_OracleQuestion.table().select().order('ocq_id DESC').exec().fetch_all()[0]
        answerer = cli_user('oracle_answerer')
        with patch.object(IPC, 'send_to_dog') as enqueue:
            output = cli_plug(answerer, f'$oracle.answer {question.get_id()} Forty two.')
        answers = GDO_OracleAnswer.table().select().exec().fetch_all()
        self.assertEqual(1, len(answers))
        self.assertEqual('Forty two.', answers[0].gdo_val('oca_text'))
        self.assertEqual(question.get_id(), answers[0].gdo_val('oca_question'))
        self.assertIn(f'Your answer to Oracle question #{question.get_id()} has been sent', output)
        enqueue.assert_called_once_with('oracle.ipc_answer', [answers[0].get_id()])
        with patch.object(GDO_Channel, 'send', new_callable=AsyncMock) as send:
            await IPC.execute_dog_event('oracle.ipc_answer', [answers[0].get_id()])
        send.assert_awaited_once_with(
            f'Oracle answer to question #{question.get_id()} from oracle_answerer{{bash}}: Forty two.')

    def test_04_answers_need_the_question_token(self):
        cli_plug(self.gizmore, '$oracle.ask Show this answer.')
        question = GDO_OracleQuestion.table().select().exec().fetch_all()[0]
        cli_plug(cli_user('oracle_answerer'), f'$oracle.answer {question.get_id()} Visible answer.')
        token = OracleQuestionToken.for_question(question)

        allowed = answers().input('question', question.get_id()).input('passcode_hash', token)
        allowed.env_user(self.gizmore).env_server(Bash.get_server()).env_channel(self.channel())
        self.assertIsInstance(Application.LOOP.run_until_complete(allowed.execute()), GDT_Table)

        denied = answers().input('question', question.get_id()).input('passcode_hash', '0' * 64)
        denied.env_user(self.gizmore).env_server(Bash.get_server()).env_channel(self.channel())
        self.assertIsInstance(Application.LOOP.run_until_complete(denied.execute()), GDT_Error)

    def test_05_questions_list_renders_id_and_text_in_chat(self):
        cli_plug(self.gizmore, '$oracle.ask Listed question.')
        output = cli_plug(self.gizmore, '$oracle.questions')
        self.assertIn('1-Listed question.', output)

    def test_06_unsubscribe_removes_current_channel(self):
        cli_plug(self.gizmore, '$oracle.subscribe')
        output = cli_plug(self.gizmore, '$oracle.unsubscribe')
        self.assertIn('no longer receives Oracle questions', output)
        self.assertEqual(0, len(GDO_OracleSubscription.table().select().exec().fetch_all()))
