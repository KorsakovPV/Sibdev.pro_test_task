import heapq

from accounts.models import Account


def method_conformance(self, user_account):
    # Получаю все свои приоритеты
    my_priorities = user_account.precedents.all().values('importance', 'priorities_name_id')
    my_priorities_dict = dict()
    for my_priorit in my_priorities:
        my_priorities_dict[my_priorit.get('priorities_name_id')] = my_priorit.get('importance')
    # Получаю все accounts
    all_accounts = Account.objects.exclude(id=user_account.id)
    return_accounts_list = list()
    for account in all_accounts:
        conformance = 0
        # Фильтрую приоритеты акаунта из цикла по своим. Оставляю совпадения
        account_precedents = account.precedents.filter(
            priorities_name_id__in=my_priorities.values('priorities_name_id'))
        # Прохожу по приоритетам и вычисляю соответствие
        for account_precedent in account_precedents:
            pass
            conformance += abs(
                account_precedent.importance - my_priorities_dict[account_precedent.priorities_name_id])
        if len(return_accounts_list) < 21:
            heapq.heappush(return_accounts_list, (100 - conformance / (len(my_priorities) * 20), account.name))
        else:
            heapq.heapreplace(return_accounts_list, (100 - conformance / (len(my_priorities) * 20),
                                                     account.name))
    data = list()
    for _ in return_accounts_list:
        conformance, name = heapq.heappop(return_accounts_list)
        if conformance < 75:
            break
        data.append({'conformance': conformance, 'name': name})
    return data
