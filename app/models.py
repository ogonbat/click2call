

"""Click To Call Database Models"""



import time
from core.db.base import ModelBase
from core.exceptions import RestMaxCallError

__author__ = 'cingusoft'

class User(ModelBase):
    """Store User-Agent informations.

     **Args:**

    * *username:* Username user <primary key>
    * *password:* Password user."""
    username = None
    password = None

    def authenticate(self,username,password):
        """authenticate method.

        if the authentication query fail raise a ObjectDoesNotExist."""
        return self.get(username=username,password=password)


class Client(ModelBase):
    """Client Table Model.

    **Args:**

    * *client_id:* The unique Client ID, is not the token <primary key>
    * *secret:* Password secret used during the Application Flow
    * *redirect_uri:* This is the uri checked during the Client Autorization process, in classic REST apps have more than one redirect uri."""

    client_id = None
    secret = None
    redirect_uri = None


    def authenticate(self,client_id,client_secret,code):
        """Check the correspondence between the clien_id, the secret password and the code.

        If the query return a empty value a ObjectDoesNotExist is raised."""
        sql = 'SELECT g.token FROM "client" AS c, "grant" AS g WHERE c.client_id=%s AND c.secret=%s and g.code=%s;'
        values = [client_id,client_secret,code]
        return self.sql(sql,values,"yes")


class Grant(ModelBase):
    """Grant Table Model.

     **Args:**

    * *token:* The unique Token obtained after the Grant process
    * *code:* Token used durign the Application Flow Authentication
    * *refresh:* Timestamp that indicate the token refresh time
    * *client_id:* Reference to Client Table <foreign key>
    * *user_id:* Reference to User-Agent Table <foreign key>."""

    token = None
    code = None
    id = None


    __user_id = None
    __client_id = None
    __refresh = None

    @property
    def expire(self):
        if self.__refresh is not None:
            return int(time.time()) - int(self.__refresh)
        else:
            return None



    @property
    def user_id(self):
        """Getter for the user id."""
        pass

    @user_id.setter
    def user_id(self,id):
        """Setter for the user id."""
        self.__user_id = id

    @property
    def client_id(self):
        """Getter for the client id."""
        pass

    @client_id.setter
    def client_id(self,id):
        """Setter for the client id."""
        self.__client_id = id

    def add(self,client_id, username):
        """Insert Query for grant table."""
        self.code = self._genHashString()
        self.token = self._genHashString()
        self.__user_id = username
        self.__client_id = client_id

        sql = 'INSERT INTO "grant" (code,token,user_id,client_id,refresh) VALUES (%s,%s,%s,%s,CURRENT_TIMESTAMP::abstime::int::bigint+3600);'
        values = [self.code,self.token,self.__user_id,self.__client_id]
        results = self.sql(sql,values)


    def update(self,client_id,username):
        """Update Query for the grant table."""
        self.code = self._genHashString()
        self.token = self._genHashString()

        sql = 'UPDATE "grant" SET refresh=CURRENT_TIMESTAMP::abstime::int::bigint+3600, code=%s, token=%s WHERE client_id=%s AND user_id=%s;'
        values = [self.code,self.token,client_id,username]
        self.sql(sql,values)

    def is_already_authorized(self,client_id,username):
        """Check if the client_id and the user-agent are linked.

        If result is 0 raise a ObjectDoesNotExist."""
        return self.get(client_id=client_id,user_id=username)

    def is_token_expired(self,token):
        """Check if the toke is expired.
        Is used the CURRENT_TIMESTAMP::abstime::int::bigint of PostgresSQL.
        This reduce the problem caused by Python to configure correct timezone."""
        sql = 'SELECT refresh-CURRENT_TIMESTAMP::abstime::int::bigint as expiration FROM "grant" WHERE token=%s'
        values = [token]
        return self.sql(sql,values,"yes")

class Call(ModelBase):
    """Call Table Model.
    **Args:**

    * *duration:* Call time duration, if not set return the ongoin call time
    * *number:* Number called from the User-Agent
    * *token:* Call token identifier for the Rest Server
    * *start:* Timestamp indicate the time start of the call
    * *endc:* Timestamp indicate the time end of the call
    * *grant_id:* Reference to Grant Table <foreign key>."""

    id = None
    duration = None
    number = None


    _start = None
    _endc = None
    _token = None
    _grant_id = None


    def start_call(self,client_id,number):
        """Query insert to add a new call.
        We use the timestamp of posgreSQL.
        Return the token call."""
        sql = 'INSERT INTO call (grant_id,token,start,number) VALUES (%s,%s,CURRENT_TIMESTAMP::abstime::int::bigint,%s);'
        token = self._genHashString()
        #start = self._genTimestamp()
        values = [client_id,token,number]
        self.sql(sql,values)
        return token

    def getCallInfo(self,token_call,token_user):
        """Return a Dictionary with a specific call."""

        sql = 'SELECT call.token as token, call.duration as duration, call.start as start, call.endc as stop, call.number as number, "user".username as username FROM call, "grant", "user" WHERE "grant".user_id = "user".username AND call.token=%s AND call.grant_id = "grant".id AND call.grant_id IN ( SELECT id FROM "grant" WHERE user_id IN (SELECT user_id FROM "grant" WHERE token=%s));'
        values=[token_call,token_user]
        return self.sql(sql,values,"yes")

    def check_allowed_calls(self,token,max_number):
        """Check if the User-Agent can start others calls."""
        sql = 'SELECT COUNT(*) as count FROM call, "grant" WHERE call.grant_id = "grant".id AND call.endc IS NULL AND call.grant_id IN ( SELECT id FROM "grant" WHERE user_id IN (SELECT user_id FROM "grant" WHERE token=%s));'
        values=[token]
        count = self.sql(sql,values,"yes")

        if int(count['count']) >= int(max_number):
            raise RestMaxCallError

    def getAllCalls(self,token_user):
        """Get a List with all the User-agent Ongoing Calls."""
        sql = 'SELECT  call.token as token, call.duration as duration, call.start as start, call.endc as stop, call.number as number FROM call, "grant" WHERE call.grant_id = "grant".id AND call.endc IS NULL AND call.grant_id IN ( SELECT id FROM "grant" WHERE user_id IN (SELECT user_id FROM "grant" WHERE token=%s));'
        values = [token_user]
        results = self.sql(sql,values,None,"yes")
        return results


    def getDuration(self,start):
        """Return the seconds difference between the start call and the actual time."""
        return int(time.time())-int(start)

    def update(self,token):
        """Update select, used to stop a call and add End Time Call and the Call Duration.
        Used CURRENT_TIMESTAMP."""
        sql = 'UPDATE call SET duration=CURRENT_TIMESTAMP::abstime::int::bigint-start, endc=CURRENT_TIMESTAMP::abstime::int::bigint WHERE token=%s;'
        values = [token]
        self.sql(sql,values)