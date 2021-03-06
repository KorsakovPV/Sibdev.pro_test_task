import operator

from accounts.models import Account


def method_conformance(user_account: Account) -> list:
    # Получаю все свои приоритеты и сохраняю их в словарь. Ключь id , значение
    my_priorities = user_account.precedents.all().values('importance', 'priorities_name_id')
    my_priorities_dict = dict()
    for my_priorit in my_priorities:
        my_priorities_dict[my_priorit.get('priorities_name_id')] = my_priorit.get('importance')

    # Получаю все accounts. В данной реализации prefetch_related утяжеляет запрос.
    all_accounts = Account.objects.exclude(id=user_account.id)  # .prefetch_related('precedents')
    return_accounts_list = list()
    for account in all_accounts:
        conformance = 0
        # Фильтрую приоритеты account. Оставляю совпадения.
        account_precedents = account.precedents.filter(
            priorities_name_id__in=my_priorities.values('priorities_name_id'))
        # Прохожу по приоритетам и вычисляю соответствие
        for account_precedent in account_precedents:
            # Посчитываю соответствие user_account(аутентифицированного) и account_precedent(из списка всех аккаунтов).
            # Максимальное соответствие 0, несоответствие 20 * на количество предпочтений у user_account.
            # Разность можно заменить на разность квадратов или кубов. Это позволит отбраковывать варианты с большими
            # различиями по одному приоритету. Сейчас такие результаты выравниваются и теряются в сумме.
            conformance += abs(
                account_precedent.importance - my_priorities_dict[account_precedent.priorities_name_id])
        try:
            ammount_conformance = 100 - conformance / (len(my_priorities) * 20) * 100
        except ZeroDivisionError:
            ammount_conformance = 0
        if ammount_conformance >= 75:
            return_accounts_list.append({'conformance': ammount_conformance, 'name': account.name})
        if len(return_accounts_list) >= 20:
            break

    return_accounts_list.sort(key=operator.itemgetter('conformance'), reverse=True)

    # Перебирать 20000 записей очень дорого. Поэтому я вывожу первые 20 подходящих записей. Это скорее всего не
    # совсем по ТЗ. Как все жадные алгоритмы он заметно быстрее. И возвращает результат приемлемый но не самый точный.
    # Релевантность результатов можно улучшить набирая не 20, а например 100 значений. А из них уже выдавать самые
    # подходящие или случайные (тоже интересное решение). Это не должно дать большую нагрузку на алгоритм.
    return return_accounts_list

    # Точное но очень долгое решение. Куча оставляет самые релевантные значения и поддерживает их в отсортированном
    # виде.

    #     if len(return_accounts_list) < 21:
    #         heapq.heappush(return_accounts_list, (ammount_conformance, account.name))
    #     else:
    #         heapq.heapreplace(return_accounts_list, (ammount_conformance, account.name))
    # data = list()
    #
    # # Достаем значения из кучи.
    # while len(return_accounts_list) > 0:
    #     conformance, name = heapq.heappop(return_accounts_list)
    #     if conformance >= 75:
    #         data.append({'conformance': conformance, 'name': name})
    #
    # # Разворачиваем массив что самое релевантное значение было первым.
    # data.reverse()
    #
    # return data
