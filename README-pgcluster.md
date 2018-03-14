- ```bash
  initdb -D ~/master -E UTF-8 --locale=C.UTF-8 -U postgres
  ```
- ```bash
  pg_basebackup -P -X stream -c fast -h 127.0.0.1 -p 5401 -U postgres -D ~/slave
  ```

- ```bash
  pg_ctl start -D ~/master/ -o '-c listen_addresses=* -c port=5401 -c hot_standby=on'\
  '-c wal_level=replica -c max_wal_senders=5 -c max_replication_slots=3 '\
  '-c synchronous_commit=remote_apply -c synchronous_standby_names=*'
  ```

- ```bash
  # cat slave/recovery.conf
  standby_mode = on
  primary_conninfo = 'host=127.0.0.1 port=5401'
  primary_slot_name = 'slot'
  trigger_file = '~/slave/promote_trigger'
  ```

- ```bash
  pg_ctl start -D ~/slave/ -o '-c listen_addresses=* -c port=5402 -c hot_standby=on'
  ```

- ```sql
  -- master
  CREATE ROLE replica WITH LOGIN REPLICATION PASSWORD '123' ;
  SELECT pg_create_physical_replication_slot('slot') ;
  SELECT * FROM pg_get_replication_slots() ;
  SELECT *, pg_wal_lsn_diff(s.sent_lsn, s.replay_lsn) AS byte_lag FROM pg_stat_replication s ;
  ```

- ```sql
  -- slave  
  SELECT now() - pg_last_xact_replay_timestamp() ;
  ```

- Q:
  - wal_level log format level is hot_standby (<9.6) or replica (>=9.6)
  - rw master, ro slave, app balance
  - wal_log_hints for pg_rewind
  - recovery_target_timeline

- uri: `postgresql://host1:port2,host2:port2/?target_session_attrs=read-write`
- temp slots
