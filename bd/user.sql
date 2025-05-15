CREATE USER 'pratcc'@'%' IDENTIFIED BY 'pratcc_app';

GRANT ALL PRIVILEGES ON pratcc.* TO 'pratcc'@'%';

FLUSH PRIVILEGES;