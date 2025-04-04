import sqlalchemy as sa


# Creates PostgreSQL function to update date in updated_on field of table
def postgresql_create_refresh_updated_on_func(schema):
    text = f"""
        CREATE FUNCTION {schema}.refresh_updated_on()
        RETURNS TRIGGER
        LANGUAGE plpgsql AS
        $func$
        BEGIN
           NEW.updated_on := now();
           RETURN NEW;
        END
        $func$;
    """
    return sa.text(text)


def postgresql_drop_refresh_updated_on_func(schema):
    text = f"DROP FUNCTION IF EXISTS {schema}.refresh_updated_on() CASCADE"
    return sa.text(text)


# Creates a PostgreSQL trigger on updated rows of table to update the date in the updated_on field
def postgresql_create_refresh_updated_on_trigger(schema, table):
    text = f"""
        CREATE TRIGGER trig_{table}_updated BEFORE UPDATE ON {schema}.{table}
        FOR EACH ROW EXECUTE PROCEDURE {schema}.refresh_updated_on();
    """
    return sa.text(text)


def postgresql_drop_refresh_updated_on_trigger(schema, table):
    text = f"DROP TRIGGER IF EXISTS trig_{table}_updated ON {schema}.{table} CASCADE"
    return sa.text(text)
