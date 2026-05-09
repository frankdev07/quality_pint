CREATE TABLE IF NOT EXISTS dim_suppliers (
    supplier_id integer PRIMARY KEY auto_increment,
    supplier_name varchar(255) NOT NULL,
    contact_person varchar(150),
    phone varchar(20),
    email varchar(150),
    tax_id varchar(50), -- NIT o NRC del proveedor para temas legales
    address text,
    is_active boolean NOT NULL DEFAULT TRUE,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp
);