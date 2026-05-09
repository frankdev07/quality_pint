CREATE TABLE IF NOT EXISTS fact_supplier_payments (
    payment_id integer PRIMARY KEY auto_increment,
    invoice_id integer NOT NULL, -- FK: ¿Qué factura estamos pagando?
    payment_date date NOT NULL,
    amount_paid decimal(10,2) NOT NULL,
    payment_method varchar(50),
    reference_number varchar(100), -- Número de cheque o transferencia
    created_at timestamp default current_timestamp,
    
    FOREIGN KEY (invoice_id) REFERENCES fact_supplier_invoices(invoice_id)
);