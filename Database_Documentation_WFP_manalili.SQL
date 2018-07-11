--Compiled Database Triggers/Functions/SQL scripts/Notification alerts for Database

##---------------------------------NOTIFY/LISTEN/SEND_EMAIL------------------------------------------------##
--PYTHON SCRIPT TO LISTEN TO DATABASE TABLE AND SEND EMAIL FOR DML
import select
import datetime
import psycopg2
import psycopg2.extensions
import smtplib
from email.mime.text import MIMEText

myhost = '127.0.0.0'
dbase = 'db'
user = 'user'
pword = ''
conn = psycopg2.connect(host=myhost, database=dbase, user=user, password=pword, async=0)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

curs = conn.cursor()
curs.execute("LISTEN my_table;")
#DBase to UNLISTEN
#curs.execute("UNLISTEN postgres;")

#Database listening loop
seconds_passed = 0
print "Waiting for notifications on channel %s@" %myhost
while 1:
    conn.commit()
    if select.select([conn],[],[],5) == ([],[],[]):
        seconds_passed += 5
        print "{} seconds passed without a notification...".format(seconds_passed)
    else:
        seconds_passed = 0
        conn.poll()
        conn.commit()
        while conn.notifies:
            message = conn.notifies.pop()
            print "There was an edit on database %s:" %dbase, message.pid, message.channel, message.payload,datetime.datetime.now()
            
            s = smtplib.SMTP('smtp.gmail.com', 587)
            # start TLS for security
            s.starttls()
            # Authentication
            s.login("wfp.hq.dbtrack@gmail.com", "password")
            sender = 'wfp.hq.dbtrack@gmail.com'
            recipients = ['michaelandrew.manalili@gmail.com','otheremail@test.com']
            # sending the mail
            s.sendmail(sender, recipients, str(message))
            # terminating the session
            s.quit()
#https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/

##---------------------------------DML TRIGGERS / UUID / OTHERS-----------------------------------------------##
#COMPARE UUID master-slave
SELECT *
FROM   master_uuid
WHERE  NOT EXISTS (SELECT * FROM _slave_uuid
				WHERE slave_uuid.uuid_str = master_uuid.uuid_str);
SELECT *
FROM   slave_uuid
WHERE  NOT EXISTS (SELECT * FROM master_uuid
				WHERE master_uuid.uuid_str = slave_uuid.uuid_str);

SELECT * from slave_uuid
EXCEPT
SELECT * from master_uuid

#UUID LOOP
CREATE FUNCTION uuid_loop() RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
  FOR Loopid  IN 0..1000000 LOOP
     PERFORM uuid_generate_v4();
  END LOOP;
RETURN;
END;
$$;

#ADD UUID
ALTER TABLE my_table ADD COLUMN UUID varchar(256);

#UUID POPULATE
ALTER TABLE my_table ALTER COLUMN UUID SET DATA TYPE UUID USING (uuid_generate_v4());

#DML TRIGGER
CREATE OR REPLACE FUNCTION notify_id_trigger() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('feature', 'message'); #feature in database, message to sent to email OR EXECUTE
  RETURN new;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER data_modified AFTER insert or update or delete on bldg for each row execute procedure notify_id_trigger();

#DML TRIGGER FOR SDE
CREATE OR REPLACE FUNCTION sde_trigger() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('sde_tables_modified', 'SDE table has been modified');
  RETURN new;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER sde_data_modify AFTER update on sde_tables_modified for each row execute procedure sde_trigger();

#QUERY DELTA TABLES FROM SDE
SELECT * FROM wfp.a43 WHERE last_edited_date <= now()

#QUERY SDE DELTA TABLES 2
SELECT SUM(num_rows) AS TOTAL_A_TABLE_ROWS from database
WHERE table_name in (SELECT 'a'||registration_id from sde.table_registry);

#QUERY DELTA TABLES I,U,D SDE
SELECT * FROM information_schema.tables 
WHERE table_schema = 'wfp' AND table_name LIKE 'd%'
order by table_name DESC

#QUERY SDE LAYER EXTENTs
SELECT layer_id, database_name, owner, schema, table_name,
spatial_column, minx, minx, maxx, maxy, layer_config
FROM sde.sde_layers

#CYANAUDIT LOGS
SELECT *
FROM cyanaudit.vw_audit_log

#CYANAUDIT GET LATEST RECORD
SELECT recorded,table_name, column_name, pk_val, new_value
FROM cyanaudit.vw_audit_log
WHERE column_name = 'geom'
AND recorded < now()

SELECT COUNT(query) FROM cyanaudit.vw_audit_transaction_statement
WHERE query LIKE '%ADD%';

#AUDIT TRIGGER
CREATE FUNCTION audit_trigger()
  RETURNS trigger
  LANGUAGE plpgsql
  AS $$
  BEGIN
    IF TG_OP = 'INSERT' THEN
      INSERT INTO audit_foreign(relid, op_type, new_data)
           SELECT TG_RELID, TG_OP, row_to_json(NEW);
      RETURN new;
    ELSIF TG_OP = 'UPDATE' THEN
      INSERT INTO audit_foreign(relid, op_type, old_data, new_data)
           SELECT TG_RELID, TG_OP, row_to_json(OLD), row_to_json(NEW);
      RETURN new;
    ELSE
      -- DELETE case
      INSERT INTO audit_foreign(relid, op_type, old_data)
           SELECT TG_RELID, TG_OP, row_to_json(OLD);
      RETURN old;
    END IF;
  END;
  $$;
##---------------------------------FOREIGN DATA WRAPPER SETUP------------------------------------------------##
CREATE EXTENSION postgres_fdw
CREATE EXTENSION ogr_fdw

CREATE SERVER myforeignserver
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host '127.0.0.0', dbname 'mydb', port '5432')

CREATE FOREIGN TABLE __alias(  
  objectid integer,
  nameshort character varying(100),
  icao character varying(5),
  shape st_points)
SERVER myforeignserver  
OPTIONS (schema_name 'myschema', table_name 'mytable_alias');

--creates user mapping for schema

CREATE USER MAPPING FOR postgres
SERVER myserver
OPTIONS (user 'michael', password 'abc123');

GRANT USAGE ON FOREIGN SERVER myforeignserver TO user;

GRANT SELECT ON TABLE schema.table TO user;

CREATE FOREIGN TABLE __myforeigntable(  
  uuid_str varchar(256),
  shape geometry,
  namelong varchar)
SERVER myforeignserver
OPTIONS (schema_name 'myschema', table_name 'my_table');

GRANT ALL PRIVILEGES ON FOREIGN SERVER myserver TO postgres

GRANT USAGE ON FOREIGN SERVER myserver TO postgres

GRANT SELECT ON FOREIGN SERVER myserver TO postgres

IMPORT FOREIGN SCHEMA ogr_all
FROM SERVER myserver INTO my_table 

SELECT * FROM pg_foreign_table;
SELECT * FROM pg_foreign_server;


