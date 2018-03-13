- patroni+etcd stream async replication
- patroni, haproxy, keepalived
- repmgr(repmgr master register) + pgbouncer + haproxy + keepalived
- pgbouncer
- `initdb -D ~/master -E UTF-8 --locale=C.UTF-8 -U postgres`
- `#initdb -D ~/slave -E UTF-8 --locale=C.UTF-8 -U postgres`


- `wal_level = hot_standby|replica` log format level
- `pg_ctl start -D ~/master/ -o '-c port=5401 -c wal_level=replica -c max_wal_senders=5 -c max_replication_slots=3 -c listen_addresses=*'`
- `SELECT pg_create_physical_replication_slot('slot');`
  `SELECT * FROM pg_get_replication_slots() ;`
- ```# cat slave/recovery.conf 
  primary_conninfo = 'host=127.0.0.1 port=5401'
  standby_mode = on
  primary_slot_name = 'slot'```

- `CREATE ROLE replica WITH LOGIN REPLICATION PASSWORD '123' ;`
- `pg_basebackup -P -X stream -c fast -h 127.0.0.1 -p 5401 -U postgres -D ~/slave`
- `pg_ctl start -D ~/slave/ -o '-c port=5402 -c hot_standby=on'`


- `synchronous_commit = remote_apply`
- `synchronous_standby_names = '*'`
- rw master, ro slave, app balance

- `wal_log_hints = on` (pg_rewind)
- `recovery_target_timeline = 'latest'`

- uri: `postgresql://host1:port2,host2:port2/?target_session_attrs=read-write`
- temp slots
