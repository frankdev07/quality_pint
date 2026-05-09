CREATE DATABASE IF NOT EXISTS quality_pint;
USE quality_pint;


CREATE TABLE IF NOT EXISTS dim_branches (
    branch_id integer PRIMARY KEY auto_increment,
    branch_name varchar(100) NOT NULL unique,
    manager_name varchar(150),
    phone varchar(20),
    address text,
    is_active boolean NOT NULL DEFAULT TRUE,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp
);

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

CREATE TABLE IF NOT EXISTS dim_suppliers (
    supplier_id integer PRIMARY KEY auto_increment,
    supplier_name varchar(255) NOT NULL,
    contact_person varchar(150),
    phone varchar(20),
    email varchar(150),
    tax_id varchar(50), 
    address text,
    is_active boolean NOT NULL DEFAULT TRUE,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp
);


CREATE TABLE IF NOT EXISTS fact_invoices (
    invoice_id integer PRIMARY KEY auto_increment,
    customer_id integer NOT NULL, 
    invoice_number varchar(50) NOT NULL, 
    branch_id integer NOT NULL, 
    issue_date date NOT NULL, 
    due_date date NOT NULL, 
    total_amount decimal(10,2) NOT NULL, 
    balance_due decimal(10,2) NOT NULL, 
    status varchar(20) DEFAULT 'Pending', 
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES dim_branches(branch_id)
);

CREATE TABLE IF NOT EXISTS fact_payments (
    payment_id integer PRIMARY KEY auto_increment,
    invoice_id integer NOT NULL, 
    payment_date date NOT NULL, 
    amount_paid decimal(10,2) NOT NULL, 
    payment_method varchar(50), 
    reference_number varchar(100), 
    created_at timestamp default current_timestamp,
    
    CONSTRAINT fk_invoice_payment FOREIGN KEY (invoice_id) REFERENCES fact_invoices(invoice_id)
);

CREATE TABLE IF NOT EXISTS fact_supplier_invoices (
    invoice_id integer PRIMARY KEY auto_increment,
    supplier_id integer NOT NULL, 
    external_invoice_number varchar(50) NOT NULL, 
    branch_id integer NOT NULL, 
    issue_date date NOT NULL,
    due_date date NOT NULL, 
    total_amount decimal(10,2) NOT NULL,
    balance_due decimal(10,2) NOT NULL, 
    status varchar(20) DEFAULT 'Pending',
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    
    CONSTRAINT fk_supplier FOREIGN KEY (supplier_id) REFERENCES dim_suppliers(supplier_id),
    CONSTRAINT fk_supplier_branch FOREIGN KEY (branch_id) REFERENCES dim_branches(branch_id)
);

CREATE TABLE IF NOT EXISTS fact_supplier_payments (
    payment_id integer PRIMARY KEY auto_increment,
    invoice_id integer NOT NULL, 
    payment_date date NOT NULL,
    amount_paid decimal(10,2) NOT NULL,
    payment_method varchar(50),
    reference_number varchar(100), 
    created_at timestamp default current_timestamp,
    
    CONSTRAINT fk_supplier_invoice_payment FOREIGN KEY (invoice_id) REFERENCES fact_supplier_invoices(invoice_id)
);