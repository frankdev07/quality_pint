CREATE TABLE IF NOT EXISTS fact_invoices (
    invoice_id integer PRIMARY KEY auto_increment,
    customer_id integer NOT NULL, 
    invoice_number varchar(50) NOT NULL, 
    branch_id integer NOT NULL, -- Ahora es un ID numérico
    issue_date date NOT NULL, 
    due_date date NOT NULL, 
    total_amount decimal(10,2) NOT NULL, 
    balance_due decimal(10,2) NOT NULL, 
    status varchar(20) DEFAULT 'Pending', 
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    
    -- Definimos las dos relaciones (Foreign Keys)
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES dim_branches(branch_id)
);
