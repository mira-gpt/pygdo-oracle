from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_String import GDT_String


class oracle(Method):
    """
    Aux module that lists the hidden oracle commands.
    """

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'oracle'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'oc'

    def gdo_execute(self) -> GDT:
        return GDT_String('result').val(self.t('info_oracle_commands'))
