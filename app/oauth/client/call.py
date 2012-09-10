
"""Call Module, this is the REST Handler."""


import time
from app.models import Call, Grant
from core.exceptions import RestMaxCallError, ObjectDoesNotExist
from core.http.handler import RestHandler
from app.settings import DOMAIN_REST, MAXIMUM_ONGOING_CALL
import tornado.web
import datetime
__author__ = 'cingusoft'


class CallHandler(RestHandler):
    """Call Handler.
    All the methos in this class permit to add, modify and check the calls."""
    def get(self):
        """This method is called with a GET.
        Without parameter return a list of ongoin call of the User-Agent.
        With the token_call parameter set, this method return the specific call information.
        """
        duration = 0
        token_call = self.get_argument("token_call",None)
        call_info = Call()
        if token_call is not None:
            try:
                infos = call_info.getCallInfo(token_call,self._grant_token)
                if infos['stop'] is not None:
                    stop = datetime.datetime.fromtimestamp(int(infos['stop'])).strftime('%d/%m/%Y %H:%M:%S')
                else:
                    stop = "Call Ongoing"
                if infos['duration'] is None:
                    #we need to calculate the duration netween the satrt to now
                    duration = call_info.getDuration(infos['start'])
                else:
                    duration = infos['duration']
                user_info = dict(
                    info= dict(duration=str(datetime.timedelta(seconds=duration)),
                                number=infos['number'],
                                token=infos['token'],
                                start=datetime.datetime.fromtimestamp(int(infos['start'])).strftime('%d/%m/%Y %H:%M:%S'),
                                end=stop),
                    user = dict(username=infos['username'])
                )
                self.set_status(200)
                self.write_result(user_info,"call")
            except ObjectDoesNotExist, e:
                raise tornado.web.HTTPError(409,"the token send is not correct")
        else:
            #return all the ongoing calls
            try:
                final = []
                results = call_info.getAllCalls(self._grant_token)
                for infos in results:
                    if infos['stop'] is not None:
                        stop = datetime.datetime.fromtimestamp(int(infos['stop'])).strftime('%d/%m/%Y %H:%M:%S')
                    else:
                        stop = "Call Ongoing"
                    if infos['duration'] is None:
                        #we need to calculate the duration netween the satrt to now
                        duration = call_info.getDuration(infos['start'])
                    else:
                        duration = infos['duration']
                    user_info = dict(
                        info= dict(duration=str(datetime.timedelta(seconds=duration)),
                            number=infos['number'],
                            token=infos['token'],
                            start=datetime.datetime.fromtimestamp(int(infos['start'])).strftime('%d/%m/%Y %H:%M:%S'),
                            end=stop)
                    )
                    final.append(user_info)
                self.set_status(200)
                print final
                self.write_result(final,"call")
            except ObjectDoesNotExist, e:
                self.set_status(204)
                self.write_result({},"call")


    def post(self):
        """Method POST to add a new call on ongoing status."""

        try:
            call_app = Call()
            call_app.check_allowed_calls(self._grant_token,MAXIMUM_ONGOING_CALL)
        except RestMaxCallError, e:
            raise tornado.web.HTTPError(409,"maximum ongoin calls reached")

        number = self.get_argument("number")
        grant_app = Grant()
        grant_id = grant_app.get(token=self._grant_token)
        call_start = Call()
        token_call = call_start.start_call(grant_id['id'],number)
        self.set_status(201)
        self.set_header("Location",DOMAIN_REST+"/call?token_call="+token_call)
        self.write("")

    def put(self):
        """PUT method to udpate the status of the call, in this case is stop the call and actualize the end time and the duration"""
        token_call = self.get_argument("token_call")
        call_stop = Call()
        returned_call = call_stop.get(token=token_call)
        if returned_call['duration'] is None:
            call_stop.update(token_call)
        self.set_status(200)
        self.set_header("Location",DOMAIN_REST+"/call?token_call="+token_call)
        self.write("")