- ```bash
  initdb -D ~/master -E UTF-8 --locale=C.UTF-8 -U postgres
  ```
- ```bash
  pg_basebackup -P -X stream -c fast -h 127.0.0.1 -p 5401 -U postgres -D ~/slave
  ```

- ```bash
  pg_ctl start -D ~/master/ -o '-c listen_addresses=* -c port=5401 '\
  '-c wal_level=hot_standby -c max_wal_senders=5 -c max_replication_slots=3 '\
  '-c synchronous_commit=remote_apply -c synchronous_standby_names=*'

- ```sql
  CREATE ROLE replica WITH LOGIN REPLICATION PASSWORD '123' ;
  SELECT pg_create_physical_replication_slot('slot') ;
  SELECT * FROM pg_get_replication_slots() ;
  ```

- ```bash
  # cat slave/recovery.conf
  standby_mode = on
  primary_conninfo = 'host=127.0.0.1 port=5401'
  primary_slot_name = 'slot'
  ```

- ```bash
  pg_ctl start -D ~/slave/ -o '-c port=5402 -c hot_standby=on'
  ```

- Q:
  - wal_level log format level is hot_standby or replica
  - rw master, ro slave, app balance
  - wal_log_hints for pg_rewind
  - recovery_target_timeline
