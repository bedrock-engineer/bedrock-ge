import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    from sqlalchemy import create_engine
    return create_engine, mo, pl


@app.cell
def _(pl):
    # Create DataFrames with one-to-many relationship
    customers = pl.DataFrame({
        "customer_id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "email": ["alice@email.com", "bob@email.com", "charlie@email.com"]
    })

    orders = pl.DataFrame({
        "order_id": [101, 102, 103, 104],
        "customer_id": [1, 1, 2, 3],  # Foreign key reference
        "amount": [100.50, 75.25, 200.00, 50.00],
        "order_date": ["2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18"]
    })
    return customers, orders


@app.cell
def _(create_engine, customers, mo, orders):
    # Create connection to new SQLite database (file will be created automatically)
    db_path = mo.notebook_location() / "database.db"
    engine = create_engine(f"sqlite:///{db_path}")

    # Write tables - schema will be created automatically
    customers.write_database("customers", engine, if_table_exists="replace")
    orders.write_database("orders", engine, if_table_exists="replace")
    return


@app.cell
def _():
    return


@app.cell
def _(create_engine, inspect, pl, text):
    class ConfigurableDatabaseManager:
        def __init__(self, db_path: str, fk_config: dict[str, list[tuple]]):
            self.engine = create_engine(f"sqlite:///{db_path}")
            self.fk_config = fk_config  # {"table_name": [("col", "ref_table", "ref_col"), ...]}
        
            with self.engine.begin() as conn:
                conn.execute(text("PRAGMA foreign_keys = ON"))
    
        def write_data_with_config(self, df: pl.DataFrame, table_name: str):
            """Write data using predefined foreign key configuration"""
            foreign_keys = self.fk_config.get(table_name, [])
        
            # Check if table exists and needs recreation for FK constraints
            inspector = inspect(self.engine)
            if table_name in inspector.get_table_names():
                # This class method is not defined
                self.recreate_table_with_fks(df, table_name, foreign_keys)
            else:
                # This class method is not defined
                self.create_table_with_fks(df, table_name, foreign_keys)
        
            df.write_database(table_name, self.engine, if_table_exists="append")

    # Usage with configuration
    # fk_relationships = {
    #     "orders": [("customer_id", "customers", "customer_id")],
    #     "order_items": [
    #         ("order_id", "orders", "order_id"),
    #         ("product_id", "products", "product_id")
    #     ],
    #     "reviews": [
    #         ("customer_id", "customers", "customer_id"),
    #         ("product_id", "products", "product_id")
    #     ]
    # }

    # db_manager = ConfigurableDatabaseManager("configured_db.db", fk_relationships)
    return


if __name__ == "__main__":
    app.run()
