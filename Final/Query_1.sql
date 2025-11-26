CREATE USER 'clinica_user'@'localhost'
IDENTIFIED WITH mysql_native_password BY 'clinica123';

GRANT ALL PRIVILEGES ON clinica.* TO 'clinica_user'@'localhost';

FLUSH PRIVILEGES;clinica_parceira

ALTER USER 'root'@'localhost'
IDENTIFIED WITH mysql_native_password BY 'B@lduin1998';

FLUSH PRIVILEGES;
paciente