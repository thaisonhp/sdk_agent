from agents import function_tool

@function_tool
def calculate_pit_in_vn(income: float, dependents: int):
    """
    Tính thuế thu nhập cá nhân ở Việt Nam.

    Args:
        income (float): Tổng thu nhập hàng tháng (triệu VND).
        dependents (int): Số người phụ thuộc (mỗi người phụ thuộc giảm trừ 4.4 triệu).

    Returns:
        float: Số tiền thuế phải đóng.
    """
    personal_deduction = 11  # triệu VND
    dependent_deduction = 4.4 * dependents  # triệu VND

    taxable_income = income - personal_deduction - dependent_deduction
    if taxable_income <= 0:
        return 0  # Không phải đóng thuế nếu thu nhập chịu thuế ≤ 0

    # Các bậc thuế
    tax_brackets = [5, 10, 18, 32, 52, 80]
    tax_rates = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35]

    tax_amount = 0
    remaining_income = taxable_income
    previous_limit = 0

    # Tính thuế theo bậc
    for i, limit in enumerate(tax_brackets):
        if remaining_income > 0:
            taxable_amount = min(remaining_income, limit - previous_limit)
            tax_amount += taxable_amount * tax_rates[i]
            remaining_income -= taxable_amount
            previous_limit = limit
        else:
            break

    if remaining_income > 0:
        tax_amount += remaining_income * tax_rates[-1]

    return round(tax_amount, 2)
