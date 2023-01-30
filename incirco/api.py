import frappe

def get_payment_order_table(doc):
    dict_ = {}
    for row in doc.references:
        bnk = frappe.get_doc("Bank Account",row.bank_account)
        if not dict_:
            str_ = row.supplier + bnk.bank + bnk.bank_account_no +bnk.branch_code
            dict_.update({str_:{"supplier":row.supplier,"bank":bnk.bank,"bank_account":bnk.bank_account_no,"branch":bnk.branch_code,"amount":row.amount}})

        else:
            str_ = row.supplier + bnk.bank + bnk.bank_account_no +bnk.branch_code
            if str_ in dict_:
                if dict_[str_]['amount']:
                    dict_[str_]['amount']+=row.amount
            else:
                dict_.update({str_:{"supplier":row.supplier,"bank":bnk.bank,"bank_account":bnk.bank_account_no,"branch":bnk.branch_code,"amount":row.amount}})
        print(dict_)
    print(dict_)
    return dict_







# <td class="Td">{{ row.supplier }}</td>
# <td class="Td">{{ bnk1.bank }}</td>
# <td class="Tr">{% if row.cheque_no %}{{ row.cheque_no }}{% endif %}</td>
# <td class="Td">{{ bnk1.bank_account_no }}</td>
# <td class="Td"> {{ bnk1.branch_code}}</td>
# <td class="Td"> {{ row.amount }}</td>