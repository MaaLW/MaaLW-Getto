# app/player/player.py
from threading import Thread, Event
from queue import Queue
import json

from .define import NavigateResult
from ..core import Message, Source, Command, CoreInterface, GamePage, NotifyInfo
from ..utils.logger import logger
from ..utils.datetime import datetime
from ..utils.maafw.maafw import maafw, TaskDetail

class Player(Thread):
    def __init__(self, 
                 core: CoreInterface, 
                 **kwargs):
        super().__init__(**kwargs)
        self._core = core
        self._stop_event = Event()
        self._run_ppl = maafw.run_ppl
        self._dont_post_stop = Event()
        pass

    def run(self):
        '''DO NOT OVERRIDE.
        Override peri_run() instead'''
        try:
            self._pre_run()
            self.peri_run()
        finally:
            self._post_run()
        pass

    def stop(self, b_force:bool=False):
        if b_force: 
            self._force_stop_player()
        else: 
            self._stop_player()
        pass

    def force_stop(self):
        self._force_stop_player()
        pass

    def _stop_player(self):
        self.__set_stop()
        logger.info("%s Get Stop Signal, Will Stop Gracefully. Please Wait...", self)
        pass

    def _force_stop_player(self):
        '''
        Set stop event and replace any resources to dummy ones.
        
        If you have added any other resources, please replace them here.
        '''
        self.__set_stop()
        self._run_ppl = maafw.dummy_run_ppl
        if not self._dont_post_stop.is_set(): 
            self._dont_post_stop.set()
            maafw.post_stop()
        logger.info("%s Get Force Stop Signal, Will Do No More Actions and Stop Soon. Please Wait...", self)
        pass

    def _notify_core(self, **kwargs):
        msg = Message(source=Source.PLAYER, command=Command.NOTIFY, content={**kwargs, "instance": self})
        self._core.post_message(msg=msg)
    
    def _pre_run(self):
        self._notify_core(info=NotifyInfo.STARTED)
        pass

    def _post_run(self):
        self._notify_core(info=NotifyInfo.DONE)
        self._dont_post_stop.set()
        pass

    def peri_run(self):
        '''
        Override this method.
        Put anything here.
        '''
        pass

    def __set_stop(self):
        self._stop_event.set()

    def stopping(self):
        return self._stop_event.is_set()
    
    def _navigate(self, dest: GamePage) -> NavigateResult:
        if self.stopping(): return NavigateResult.STOPPED
        logger.debug("Navigating for %s, destination is %s", self, dest)
        if dest is GamePage.HOME:
            return self.__navigate_home()
        elif dest is GamePage.UNKNOWN:
            return NavigateResult.FAILED
        # TODO: Navigate to Exchange Shop
        else:
            logger.error("Not Implemented: %s", dest)
            return NavigateResult.FAILED
        pass

    def __navigate_home(self) -> NavigateResult:
        dest = GamePage.HOME
        b, td = self._run_ppl("Home_Go_Back_Home_Ruthlessly_v2", timeout=60)
        if not b or not td.status.succeeded:
            if self.stopping(): # error due to force stop
                return NavigateResult.STOPPED
            logger.error("%s Failed to navigate to home page", self)
            #self._notify_core(info="failed", action="navigate", dest=dest)
            return NavigateResult.FAILED
        if self._core.need_scrape(gp=dest):
            try:
                self.__scrape_home()
            except Exception as e:
                logger.error("%s Failed to scrape home page: %s", self, e)
            pass
        return NavigateResult.SUCCEEDED
    
    def __scrape_home(self) -> bool:
        datetime_last_scrape_home = datetime.now()
        b, td = self._run_ppl("Home_Scrape_Custom_Reco_Runner_v1", timeout=10)
        if b and isinstance(td, TaskDetail):
            str_result = td.nodes[-1].recognition.best_result.detail
            logger.debug("%s Home Page Scrape Result: %s", self, str_result)
            dict_result = json.loads(str_result)
            assert isinstance(dict_result, dict)
            dict_result["datetime_last_scrape_home"] = datetime_last_scrape_home
            self._notify_core(info=NotifyInfo.SCRAPED, gamepage=GamePage.HOME, result=dict_result)
            return True
        return False

    def _replay_daemon(self):
        if self.stopping(): return
        # create a replay daemon and join it
        pass