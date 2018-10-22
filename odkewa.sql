drop table xdatamedia;
drop table xdata;
drop table xmetamedia;
drop table xmeta;

create table xmeta(
 fid text not null, -- form id
 vid text not null, -- version id (commit)
 giturl text not null,
 path text not null,
 ts timestamptz default now(),
 xlsform bytea not null,
 xform json not null,
 primary key (fid, vid)
);

create table xmetamedia(
 fid text not null,
 vid text not null,
 filename text not null,
 mimetype text not null, -- image/png, etc.
 language text null,
 content bytea not null,
 primary key (fid, vid, filename),
 foreign key (fid, vid) references xmeta (fid, vid)
);

create table xdata(
 sid text not null,
 fid text not null,
 vid text not null,
 device_id text not null,
 device_ip text not null,
 device_type text not null,
 ts timestamptz default now(),
 xdata json not null,
 primary key (sid),
 foreign key (fid, vid) references xmeta (fid, vid)
 -- hidden foreign key (xdata->...mediafields...) references xdatamedia(msid)
);

create table xdatamedia(
 msid text not null,
 filename text not null,
 mimetype text not null, -- image/png, etc.
 content bytea not null,
 ts timestamptz default now(),
 primary key (msid)
);
