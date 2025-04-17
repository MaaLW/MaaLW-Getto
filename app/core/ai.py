from .corethread import CoreThread
from .define import Message, Source, Command, GamePage, NotifyInfo
from ..utils.datetime import datetime, timedelta
from ..utils.logger import logger

class AI(CoreThread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autopilot = False

    def _process(self, msg: Message, priority=100):
        logger.debug("%s Processing %s", self, msg)
        if msg.command == Command.NOTIFY:
            logger.info("AI received notification: %s", msg.content)
            # TODO: 实现AI决策逻辑
            strinfo = msg.content.get("info")
            assert isinstance(strinfo, str)
            info = NotifyInfo.from_str(strinfo)
            assert info is not None
            if info is NotifyInfo.SCRAPED:
                self._on_notify_scraped(msg)
            elif info is NotifyInfo.STARTED:
                pass
            elif info is NotifyInfo.FAILED:
                pass
            elif info is NotifyInfo.DONE:
                pass

    def _on_notify_scraped(self, msg: Message):
        gp = GamePage.from_str(msg.content.get("gamepage"))
        assert gp is not None
        scraped_result = msg.content.get("result")
        assert isinstance(scraped_result, dict)
        for name, value in scraped_result.items():
            vardict = dict(name=name, value=value)
            self._core.varspool.post_message(Message(source=Source.AI, command=Command.SET_VARIABLE, content=vardict))
        # TODO: Maybe should be configurable

    def need_scrape(self, gp: GamePage) -> bool:
        varname_last_scrape = "datetime_last_scrape_" + gp.value
        last_scrape = self._core.varspool.get_variable(varname_last_scrape)
        expire_time = timedelta(minutes=45) # TODO: Maybe should be configurable
        if last_scrape is None:
            return True
        if isinstance(last_scrape.value, datetime):
            return (datetime.now() - last_scrape.value) > expire_time
        else:
            logger.warning("Variable %s is not datetime type. Please Check.", varname_last_scrape)
            return True