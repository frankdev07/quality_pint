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