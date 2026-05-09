CREATE TABLE IF NOT EXISTS dim_branches (
    branch_id integer PRIMARY KEY auto_increment,
    branch_name varchar(100) NOT NULL unique,
    manager_name varchar(150),
    phone varchar(20),
    address text,
    is_active boolean NOT NULL DEFAULT TRUE,
    -- Agregamos los metadatos para consistencia
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp
);