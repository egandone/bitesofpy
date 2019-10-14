import decimal
import math

# Need to "quantize" our currency amounts
# to 1 cent so they render consistently
one_cent = decimal.Decimal('0.01')


def _calc_grand_total(item_total, tax_rate, tip):
    # Start wit the item amount
    total = decimal.Decimal(item_total[1:])

    # Compute and add the tax - round total to the cent
    tax_rate = decimal.Decimal(tax_rate[:-1]) / 100
    tax = round(total * tax_rate, 2)
    total += tax

    # Compute and add the tip on top of the subtotal
    tip_rate = decimal.Decimal(tip[:-1]) / 100
    tip = round(total * tip_rate, 2)
    total += tip

    return total.quantize(one_cent)


def check_split(item_total, tax_rate, tip, people):
    """Calculate check value and evenly split.

       :param item_total: str (e.g. '$8.68')
       :param tax_rate: str (e.g. '4.75%)
       :param tip: str (e.g. '10%')
       :param people: int (e.g. 3)

       :return: tuple of (grand_total: str, splits: list)
                e.g. ('$10.00', [3.34, 3.33, 3.33])
    """
    grand_total = _calc_grand_total(item_total, tax_rate, tip)

    # To compute the split we first divide the total evenly
    # amoungst the people - we round down so only have to
    # adjust amounts upwards below
    with decimal.localcontext() as decimal_ctx:
        decimal_ctx.rounding = decimal.ROUND_DOWN
        starting_split = round(grand_total / people, 2)

    # Create initial list of equal amounts
    splits = [starting_split.quantize(one_cent)] * people

    # Then while the current total is less then the target
    # just keep adding a cent evenly
    i = 0
    while sum(splits) < grand_total:
        splits[i] += one_cent
        i += 1
        i = i % people  # this ensures i wraps properly which should probably never happen

    return (f'${grand_total}', splits)
