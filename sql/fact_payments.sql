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
