# FreshBasket Reliable Pipeline Check

This project demonstrates two workflow reliability layers:

## Session 1 checks
- file exists
- file is not empty

## Session 2 checks
- required columns exist

Required columns:
- order_id
- customer_id
- order_total
- order_date

## Run valid file
```bash
python reliable_pipeline.py