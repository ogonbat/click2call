CREATE DATABASE clickcall
  WITH OWNER = postgres
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'C'
       LC_CTYPE = 'C'
       CONNECTION LIMIT = -1;

CREATE TABLE call
(
  id serial NOT NULL,
  grant_id integer,
  duration integer,
  "number" character(20),
  token character(20),
  start integer,
  endc integer,
  CONSTRAINT pk_call PRIMARY KEY (id ),
  CONSTRAINT fk_call_grant FOREIGN KEY (grant_id)
      REFERENCES "grant" (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT unique_call_token UNIQUE (token )
)WITH (
  OIDS=FALSE
);
CREATE TABLE client
(
  client_id character(20) NOT NULL,
  secret character(20),
  redirect_uri character(125),
  CONSTRAINT pk_client PRIMARY KEY (client_id )
)WITH (
  OIDS=FALSE
);
CREATE TABLE "grant"
(
  id serial NOT NULL,
  user_id character(20),
  client_id character(20),
  token character(20),
  code character(20),
  refresh integer,
  CONSTRAINT pk_grant PRIMARY KEY (id ),
  CONSTRAINT fk_grant_client FOREIGN KEY (client_id)
      REFERENCES client (client_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_grant_user FOREIGN KEY (user_id)
      REFERENCES "user" (username) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT unique_code UNIQUE (code ),
  CONSTRAINT unique_token UNIQUE (token )
)WITH (
  OIDS=FALSE
);
CREATE TABLE "user"
(
  username character(20) NOT NULL,
  password character(20),
  CONSTRAINT pk_username PRIMARY KEY (username )
)WITH (
  OIDS=FALSE
);