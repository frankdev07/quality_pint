CREATE TABLE IF NOT EXISTS fact_supplier_invoices (
    invoice_id integer PRIMARY KEY auto_increment,
    supplier_id integer NOT NULL, -- FK: ¿A quién le debemos?
    external_invoice_number varchar(50) NOT NULL, -- El número de factura del proveedor
    branch_name varchar(50) NOT NULL, -- Para saber qué tienda hizo la compra
    issue_date date NOT NULL,
    due_date date NOT NULL, -- Fecha en que Juan debe pagarle al proveedor
    total_amount decimal(10,2) NOT NULL,
    balance_due decimal(10,2) NOT NULL, -- Saldo que Juan aún no ha pagado
    status varchar(20) DEFAULT 'Pending',
    created_at timestamp default current_timestamp,
    
    FOREIGN KEY (supplier_id) REFERENCES dim_suppliers(supplier_id)
);