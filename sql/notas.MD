CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id integer PRIMARY KEY auto_increment,
    customer_code varchar(50) NOT NULL unique,
    customer_segment varchar(10), 
    full_name varchar(255) NOT NULL,
    phone varchar(20),
    email varchar(150),
    address text,
    allows_credit boolean NOT NULL DEFAULT FALSE,
    credit_limit decimal(10,2) DEFAULT 0.00,
    max_credit_days integer DEFAULT 0,
    payment_frequency_days integer DEFAULT 0,
    is_active boolean NOT NULL DEFAULT TRUE,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp
);

CREATE TABLE IF NOT EXISTS fact_invoices (
    invoice_id integer PRIMARY KEY auto_increment,
    customer_id integer NOT NULL, -- FK: ¿Quién debe?
    invoice_number varchar(50) NOT NULL, -- El número de factura física o DTE
    branch_name varchar(50) NOT NULL, -- "Santa Elena" o "Soyapango"
    issue_date date NOT NULL, -- Fecha en que se llevó la pintura
    due_date date NOT NULL, -- Fecha límite para pagar (Calculada con los días calendario)
    total_amount decimal(10,2) NOT NULL, -- Deuda original (Ej. $100.00)
    balance_due decimal(10,2) NOT NULL, -- Saldo pendiente (Lo que falta por pagar)
    status varchar(20) DEFAULT 'Pending', -- 'Pending' (Pendiente), 'Paid' (Pagada), 'Overdue' (En mora)
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    
    -- Relación con la tabla de clientes que creamos antes
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id)
);

CREATE TABLE IF NOT EXISTS fact_payments (
    payment_id integer PRIMARY KEY auto_increment,
    invoice_id integer NOT NULL, -- FK: ¿A qué factura le está abonando?
    payment_date date NOT NULL, -- Fecha en que entregó el dinero
    amount_paid decimal(10,2) NOT NULL, -- Cuánto abonó (Ej. $25.00)
    payment_method varchar(50), -- "Efectivo", "Transferencia", "Cheque"
    reference_number varchar(100), -- Número de transferencia bancaria (si aplica)
    created_at timestamp default current_timestamp,
    
    -- Relación con la tabla de facturas
    FOREIGN KEY (invoice_id) REFERENCES fact_invoices(invoice_id)
);

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