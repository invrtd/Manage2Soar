from django.db import migrations

JOURNAL_TABLES = ("billing_journalentry", "billing_journalline")

# A generic starting chart of accounts. Clubs rename, renumber, and add
# accounts (including their bank accounts) from the Club Finances pages.
SEED_ACCOUNTS = (
    ("1000", "Undeposited Funds", "asset", True, "undeposited_funds"),
    ("1200", "Member Receivables", "asset", False, "member_receivables"),
    ("2000", "Accounts Payable", "liability", False, None),
    ("3000", "General Fund", "equity", False, "general_fund"),
    ("3900", "Opening Balance Equity", "equity", False, "opening_balance_equity"),
    ("4000", "Membership Dues", "income", False, None),
    ("4100", "Tow Fees", "income", False, "tow_revenue"),
    ("4200", "Glider Rental", "income", False, "rental_revenue"),
    ("4300", "Instruction", "income", False, "instruction_revenue"),
    ("4400", "Guest Flights", "income", False, "guest_flight_revenue"),
    ("4500", "Miscellaneous Charges", "income", False, "default_charge_revenue"),
    ("4600", "Donations", "income", False, None),
    ("4900", "Other Income", "income", False, None),
    ("5000", "Field Rent", "expense", False, None),
    ("5100", "Aircraft Maintenance", "expense", False, None),
    ("5200", "Fuel and Oil", "expense", False, None),
    ("5300", "Insurance", "expense", False, None),
    ("5400", "Utilities", "expense", False, None),
    ("5500", "Bank Fees", "expense", False, None),
    ("5800", "Member Credits and Discounts", "expense", False, "member_credits"),
    ("5900", "Bad Debt and Write-offs", "expense", False, "bad_debt"),
)


def install_journal_triggers(apps, schema_editor):
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        if connection.vendor == "sqlite":
            for table in JOURNAL_TABLES:
                for action in ("UPDATE", "DELETE"):
                    cursor.execute(
                        f"""
                        CREATE TRIGGER {table}_no_{action.lower()}
                        BEFORE {action} ON {table}
                        BEGIN
                            SELECT RAISE(ABORT, 'posted journal records are immutable');
                        END;
                        """
                    )
        elif connection.vendor == "postgresql":
            cursor.execute(
                """
                CREATE FUNCTION billing_reject_journal_mutation() RETURNS trigger AS $$
                BEGIN
                    RAISE EXCEPTION 'posted journal records are immutable';
                END;
                $$ LANGUAGE plpgsql;
                """
            )
            for table in JOURNAL_TABLES:
                cursor.execute(
                    f"""
                    CREATE TRIGGER {table}_no_mutation
                    BEFORE UPDATE OR DELETE ON {table}
                    FOR EACH ROW EXECUTE FUNCTION billing_reject_journal_mutation();
                    """
                )


def remove_journal_triggers(apps, schema_editor):
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        if connection.vendor == "sqlite":
            for table in JOURNAL_TABLES:
                for action in ("update", "delete"):
                    cursor.execute(f"DROP TRIGGER IF EXISTS {table}_no_{action}")
        elif connection.vendor == "postgresql":
            for table in JOURNAL_TABLES:
                cursor.execute(
                    f"DROP TRIGGER IF EXISTS {table}_no_mutation ON {table}"
                )
            cursor.execute("DROP FUNCTION IF EXISTS billing_reject_journal_mutation()")


def seed_chart_of_accounts(apps, schema_editor):
    Account = apps.get_model("billing", "Account")
    if Account.objects.exists():
        return
    for code, name, account_type, is_cash, role in SEED_ACCOUNTS:
        Account.objects.create(
            code=code,
            name=name,
            type=account_type,
            is_cash=is_cash,
            system_role=role,
        )


def unseed_chart_of_accounts(apps, schema_editor):
    Account = apps.get_model("billing", "Account")
    Account.objects.filter(
        code__in=[row[0] for row in SEED_ACCOUNTS], lines__isnull=True
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("billing", "0011_club_accounting")]

    operations = [
        migrations.RunPython(install_journal_triggers, remove_journal_triggers),
        migrations.RunPython(seed_chart_of_accounts, unseed_chart_of_accounts),
    ]
