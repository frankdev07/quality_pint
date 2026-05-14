CREATE OR REPLACE VIEW vw_cuentas_por_cobrar AS
SELECT 
    f.invoice_number AS 'Numero_Factura',
    c.customer_code AS 'Codigo_Cliente',
    c.full_name AS 'Cliente',
    b.branch_name AS 'Sucursal',
    f.issue_date AS 'Fecha_Emision',
    f.due_date AS 'Fecha_Vencimiento',
    f.balance_due AS 'Saldo_Pendiente',
    f.status AS 'Estado'
FROM fact_invoices f
JOIN dim_customers c ON f.customer_id = c.customer_id
JOIN dim_branches b ON f.branch_id = b.branch_id
WHERE f.balance_due > 0;