def get_count_char(str_):
    letters = str_.lower() 
    dictionary = {} 
    for i in letters:  
        if i.isalpha():  
            if i in dictionary.keys():  
                count = dictionary[i]  
                count += 1  
                dictionary[i] = count  
            else:  
                dictionary[i] = 1  
    return dictionary 


def get_percent_correlation(str_):
    cor = get_count_char(str_) 
    summary = sum(cor.values()) 
    for key in cor: 
        cor[key] /= summary 
        cor[key] *= 100 
        cor[key] = round(cor[key]) 
    return cor 


main_str = """
        Данное предложение будет разбиваться на отдельные слова. 
        В качестве разделителя для встроенного метода split будет выбран символ пробела. На выходе мы получим список 
        отдельных слов. 
        Далее нужно отсортировать слова в алфавитном порядке, а после сортировки склеить их с помощью метода строк join.
        Приступим!!!!
    """

print(get_count_char(main_str))  # Вывод словаря "Буква" - "Количество"
# print(get_percent_correlation(main_str))  # Вывод словаря "Буква" - "Процентное соотношение (данная буква/все буквы)"
