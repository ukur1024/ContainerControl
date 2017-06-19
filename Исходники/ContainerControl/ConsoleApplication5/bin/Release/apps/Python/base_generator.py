#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from scipy import stats
from sklearn import linear_model

# Количество предлагаемых хэндлером рекомендаций
HANDLER_RECOMS = 5
# Количество выводимых рекомендаций из предложенных
HANDLER_SHOWN = 7
# Флаг для отключения записи данных в файл
DISABLE_DATAFILE_CHANGE = False

class Exercise:
    '''
    Класс, представляющий задание.
    
    Назначение полей (предполагаемый тип):
    ID (int) - идентификатор задания
    difficulty (int) - сложность задания
    text (str) - текст задания
    answer (str) - предполагаемый ответ
    tags (list of str) - теги (навыки), относящиеся к заданию
    theme (Theme) - тема, к которой относится данное задание
    reward (int) - баллы за задание
    '''
    def __init__(self, identifier):
        self.ID = identifier
        self.difficulty = 1
        self.text = ''
        self.answer = ''
        self.tags = []
        self.theme = None
        self.reward = 0
    #
    def __repr__(self):
        return 'Задание {0} ({1}, сложность {2})'.format( \
            self.ID, self.theme, self.difficulty)
#
class Theme:
    '''
    Класс, представляющий тему.
    
    Назначение полей (предполагаемый тип):
    ID (int) - идентификатор темы
    name (str) - название темы
    exercises (list of Exercise) - упражнения, относящиеся к теме
    minimal_tags (list of str) - минимальный набор навыков для освоения
    '''
    def __init__(self, identifier):
        self.ID = identifier
        self.name = ''
        self.exercises = []
        self.minimal_tags = []
    #
    def __repr__(self):
        return 'Тема {0}: {1}'.format(self.ID, self.name)
#
class Student:
    '''
    Класс, представляющий студента.
    
    ID (int) - идентификатор студента
    '''
    def __init__(self, identifier, system, answers):
        self._exercises = system.exercises
        self._themes = system.themes
        self.ID = identifier
        self._answers = answers
        #
        self.compl_exercises = []
        for a in self._answers:
            self.compl_exercises.append(self._exercises[str(a)])
    #
    def completed_exercises(self):
        "Возвращает завершённые студентом задания."
        return self.compl_exercises
    #
    def uncompleted_exercises(self):
        "Возвращает незавершённые студентом задания."
        result = []
        for ex in self._exercises.values():
            if not (ex in self.compl_exercises):
                result.append(ex)
        #
        return result
    #
    def exercises_by_theme(self, theme):
        "Возвращает завершённые по данной теме задания."
        result = []
        for ex in self.compl_exercises:
            if ex.theme == theme:
                result.append(ex)
        return result
    #
    def unexercises_by_theme(self, theme):
        "Возвращает незавершённые по данной теме задания."
        result = []
        compl = self.exercises_by_theme(theme)
        for ex in theme.exercises:
            if not (ex in compl):
                result.append(ex)
        #
        return result
    #
    def exercise_completeness(self, theme):
        "Возвращает освоенность темы по заданиям."
        # Обработка пустых тем
        if len(theme.exercises) == 0:
            return 1.0
        # Отношение пройденных заданий ко всем имеющимся
        return len(self.exercises_by_theme(theme)) / \
            float(len(theme.exercises))
    #
    def reward_completeness(self, theme):
        "Возвращает освоенность темы по баллам."
        # Максимум баллов за тему
        total = 0
        for ex in theme.exercises:
            total += ex.reward
        # Обработка пустых тем или заданий, не имеющих баллов
        if total == 0:
            return 1.0
        # Получено баллов за тему
        current = 0
        for ex in self.exercises_by_theme(theme):
            current += ex.reward
        # Отношение полученных баллов к максимуму
        return current / float(total)
    #
    def completed_tags(self, theme):
        "Возвращает освоенные по данной теме умения."
        tags = set()
        for ex in self.exercises_by_theme(theme):
            for tag in ex.tags:
                tags.add(tag)
        #
        return tags
    #
    def uncompleted_tags(self, theme):
        "Возвращает неосвоенные по данной теме умения."
        return set.difference( \
            set(theme.minimal_tags), self.completed_tags(theme))
    #
    def is_theme_completed(self, theme):
        "Определяет, освоена ли тема в полном объёме."
        return len(self.uncompleted_tags(theme)) == 0
    #
    def __repr__(self):
        return 'Студент ' + str(self.ID)
#

class TestSystem:
    "Класс, представляющий систему тестирования."
    def __init__(self):
        self.themes = {}
        self.exercises = {}
        self._load_themes()
        #
        self.students = {}
        self._load_students()
        #
        self.weights = []
        self._load_handler_weights()
        #
        self.last_recommendation = []
        self.last_choice = []
        self.recommendation_dict = {}
        #
        self.handlers = (self.max_difficulty_handler, \
                         self.tags_handler, \
                         self.completeness_handler, \
                         self.collaboration_handler, \
                         self.interest_handler)
        #
        self.total_recommendations = []
        self.total_choises = [0, 0, 0, 0, 0]
        self._norm_counter = 0
        # нормализируемая гребневая регрессия
        self._ridge = linear_model.Ridge(alpha = 0.05, normalize = True)
    #
    def _load_handler_weights(self):
        "Загружает веса хэндлеров из файла."
        weights_file = open('weights.dat', 'r')
        for line in weights_file.readlines():
            try:
                self.weights.append(float(line))
            except ValueError:
                pass
    #
    def _load_themes(self):
        "Загружает темы из XML-файла в объектное представление."
        import xml.etree.ElementTree as ET
        #
        for t_node in ET.parse('themes.xml').getroot():
            theme = Theme(0)
            theme.name = '<empty>'
            if 'name' in t_node.attrib:
                theme.name = t_node.attrib['name']
            if 'id' in t_node.attrib:
                theme.ID = t_node.attrib['id']
            # минимальный набор навыков
            min_tags_node = t_node.find('minimal_tags')
            if min_tags_node != None:
                theme.minimal_tags = min_tags_node.text.split(',')
            # задания
            for ex_node in t_node.findall('exercise'):
                exercise = Exercise(0)
                exercise.theme = theme
                if 'id' in ex_node.attrib:
                    exercise.ID = ex_node.attrib['id']
                if 'difficulty' in ex_node.attrib:
                    exercise.difficulty = int(ex_node.attrib['difficulty'])
                if 'reward' in ex_node.attrib:
                    exercise.reward = int(ex_node.attrib['reward'])
                # текст задания
                ex_text_node = ex_node.find('text')
                if ex_text_node != None:
                    exercise.text = ex_text_node.text
                # ответ на задание
                ex_ans_node = ex_node.find('answer')
                if ex_ans_node != None:
                    exercise.answer = ex_ans_node.text
                # навыки к заданию
                ex_tags_node = ex_node.find('tags')
                if ex_tags_node != None:
                    exercise.tags = ex_tags_node.text.split(',')
                # добавление результатов в словарь
                theme.exercises.append(exercise)
                self.exercises[exercise.ID] = exercise
            #
            self.themes[theme.ID] = theme
    #
    @staticmethod
    def generate_students_file(count, answers):
        "Генерирует файл с ответами студентов."
        studfile = open('students.dat', 'w')
        for i in range(count):
            ans_count = random.randint(1, answers)
            # генерация случайного набора ответов
            numbers = set()
            for a in range(ans_count):
                numbers.add(random.randint(1, answers))
            # вывод в файл
            studfile.write(str(i) + ':' + ','.join(map(str, numbers)) + '\n')
        # 
        studfile.flush()
        studfile.close()
    #
    def refresh_students_file(self):
        "Сохраняет данные о студентах, полученные в текущий запуск."
        studfile = open('students.dat', 'w')
        vals = sorted(self.students.keys(), key=int)
        for v in vals:
            studfile.write(v + ':' + ','.join(map(lambda x: x.ID, \
                self.students[v].completed_exercises())) + '\n')
        # 
        studfile.flush()
        studfile.close()
    #
    def refresh_weights_file(self):
        "Сохраняет веса хэндлеров, полученные в текущий запуск."
        w_file = open('weights.dat', 'w')
        for w in self.weights:
            w_file.write(str(w) + '\n')
        w_file.flush()
        w_file.close()
    #
    def _load_students(self):
        "Загружает информацию о студентах из файла."
        studfile = open('students.dat', 'r')
        for line in studfile.readlines():
            if len(line) > 2:
                # часть до двоеточия - ID студента
                first = line.split(':')
                ID = first[0]
                # часть после - решённые задания
                answers = map(int, first[1].split(','))
                self.students[ID] = Student(ID, self, answers)
    #
    def max_difficulty_handler(self, student):
        '''
        Хэндлер наивысшей сложности.
        Приоритет в выборе отдаётся самым сложным заданиям.
        '''
        result = []
        for ex in student.uncompleted_exercises():
            # Вес самых сложных заданий - 1
            if ex.difficulty == 3:
                result.append((ex, 1.0))
            # Вес заданий повышенной сложности - 0.75
            elif ex.difficulty == 2:
                result.append((ex, 0.75))
            # Вес собычных заданий - 0.5
            else:
                result.append((ex, 0.5))
        #
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    #
    def tags_handler(self, student):
        '''
        Хэндлер освоения умений.
        Приоритет в выборе отдаётся заданиям, покрывающим наибольшее
        число неосвоенных тегов в теме.
        '''
        result = []
        for ex in student.uncompleted_exercises():
            untags = student.uncompleted_tags(ex.theme)
            coverity = untags.intersection(set(ex.tags))
            cov_koeff = 0.01
            if len(untags) != 0:
                cov_koeff = len(coverity) / float(len(untags))
            result.append((ex, cov_koeff))
        #
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    #
    def completeness_handler(self, student):
        '''
        Хэндлер полноты прохождения тем по заданиям и баллам.
        Приоритет в выборе отдаётся заданиям из тем, в которых
        решено меньше всего заданий.
        '''
        result = []
        for th in self.themes.values():
            compl = (student.exercise_completeness(th) + \
                     student.reward_completeness(th)) / 2.0
            for ex in student.unexercises_by_theme(th):
                result.append((ex, 1 - compl))
        #
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    #
    def collaboration_handler(self, student):
        '''
        Хэндлер коллаборации.
        Приоритет в выборе отдаётся заданиям, которые решали студенты,
        находившиеся в похожей ситуации.
        '''
        def inter_len(s):
            return len(set.intersection(set(student.completed_exercises()), \
                set(s.completed_exercises())))
        #
        stud_sim = []
        for s in self.students.values():
            # Студенты с большим числом решённых заданий будут полностью
            # занимать рекомендацию. Поэтому разница в решённых темах ограничена
            if abs(len(s.completed_exercises()) - \
                   len(student.completed_exercises())) < 10:
                stud_sim.append(s)
        #
        stud_sim = sorted(stud_sim, key=inter_len, reverse=True)
        result = set()
        sync_result = set()
        for stud in stud_sim:
            for ex in stud.completed_exercises():
                if not ex in sync_result:
                    result.add((ex, 1.0 - (1.0 / (inter_len(stud) + 1))))
                    sync_result.add(ex)
        #
        result = sorted(result, key=lambda x: x[1], reverse=True)
        return result
    #
    def interest_handler(self, student):
        '''
        Хэндлер по интересам.
        Приоритет в выборе отдаётся заданиям из тем, в которых
        пользователь прошёл больше всего заданий.
        '''
        result = []
        for th in self.themes.values():
            count = len(student.exercises_by_theme(th))
            for ex in student.unexercises_by_theme(th):
                koeff = 1 - (1.0 / (count + 1))
                if koeff < 0.01:
                    koeff = 0.01
                result.append((ex, koeff))
        #
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    #
    def generate_recommendation(self, student):
        "Составляет рекомендацию для пользователя."
        self.last_recommendation = []
        self.recommendation_dict = {}
        result = []
        res_len = 0
        index = 0
        #
        for hnd in self.handlers:
            res_len += HANDLER_RECOMS
            recom = hnd(student)
            iterator = iter(recom)
            weights = []
            while len(result) < res_len:
                pair = next(iterator)
                pair = (pair[0], pair[1] * self.weights[index])
                if not (pair[0] in map(lambda x: x[0], result)):
                    result.append(pair)
                    weights.append(pair[1])
                    self.recommendation_dict[pair[0].ID] = index
                #
            index += 1
            self.last_recommendation.append(weights)
        #
        result = sorted(result, key=lambda x: x[1], reverse=True)
        return result
    #
    def calculate_weights(self):
        if (len(self.last_recommendation) == 0) or (len(self.last_choice) == 0):
            return
        for i in range(HANDLER_RECOMS):
            column = []
            for j in range(len(self.last_recommendation)):
                column.append(self.last_recommendation[j][i])
            self.weights[i] += stats.linregress(column, self.last_choice).slope
    #
    def _is_arg(self, arg):
        if arg == '':
            print('Укажите аргумент.')
            return False
        return True
    #
    def start_REPL(self):
        print('Добро пожаловать в систему тестирования.')
        print('Для входа введите login <ID студента>')
        print('Для выхода из программы введите exit')
        print('Для показа справки по командам введите help')
        #
        student_id = ''
        while True:
            str_cmd = input('> ').split(' ')
            cmd = str_cmd[0]
            arg = ''
            if len(str_cmd) > 1:
                arg = str_cmd[1]
            #
            if cmd == 'exit':
                if not DISABLE_DATAFILE_CHANGE:
                    self.refresh_students_file()
                    self.refresh_weights_file()
                return
            elif cmd == 'help':
                print('Справка по командам системы')
                print('help - вывод справки')
                print('exit - выход из системы')
                print('login <ID> - вход за студента по ID')
                print('compl - завершённые задания')
                print('uncompl - незавершённые задания')
                print('compl_t <ID> - освоенные задания в теме по ID')
                print('tags <ID> - освоенные умения в теме по ID')
                print('untags <ID> - неосвоенные умения в теме по ID')
                print('a <ID> - выбрать вопрос для ответа по ID')
            #
            elif cmd == 'login':
                if not self._is_arg(arg):
                    continue
                else:
                    student_id = arg
                #
                if not (student_id in self.students):
                    print('Такого студента нет в базе.')
                    student_id = ''
                    continue
                else:
                    rec = self.generate_recommendation(\
                        self.students[student_id])
                    print('Рекомендуемые задания')
                    for pair in rec[:HANDLER_SHOWN]:
                        print(pair[0])
            #
            elif cmd == 'compl':
                print('Завершённые задания')
                result = ', '.join(map(lambda ex: ex.ID, \
                    self.students[student_id].completed_exercises()))
                print(result)
            elif cmd == 'uncompl':
                print('Незавершённые задания')
                result = ', '.join(map(lambda ex: ex.ID, \
                    self.students[student_id].uncompleted_exercises()))
                print(result)
            elif cmd == 'compl_t':
                if not self._is_arg(arg):
                    continue
                else:
                    if not (arg in self.themes.keys()):
                        print('Такой темы нет в базе.')
                        continue
                    print('Завершённые задания в теме {0}'.format(arg))
                    result = ', '.join(map(lambda ex: ex.ID, \
                        self.students[student_id].\
                            exercises_by_theme(self.themes[arg])))
                    print(result)
            #
            elif cmd == 'tags':
                if not self._is_arg(arg):
                    continue
                else:
                    if not (arg in self.themes.keys()):
                        print('Такой темы нет в базе.')
                        continue
                    print('Полученные умения в теме {0}'.format(arg))
                    result = ', '.join(self.students[student_id].\
                        completed_tags(self.themes[arg]))
                    print(result)
            #
            elif cmd == 'untags':
                if not self._is_arg(arg):
                    continue
                else:
                    if not (arg in self.themes.keys()):
                        print('Такой темы нет в базе.')
                        continue
                    print('Неполученные умения в теме {0}'.format(arg))
                    result = ', '.join(self.students[student_id].\
                        uncompleted_tags(self.themes[arg]))
                    print(result)
            #
            elif cmd == 'a':
                if not self._is_arg(arg):
                    continue
                else:
                    if not (arg in self.exercises.keys()):
                        print('Такого задания нет в базе.')
                        continue
                    ex = self.exercises[arg]
                    print(ex)
                    print('Текст задания:', ex.text)
                    print('Умения:', ex.tags)
                    print('\nВыберите действие:')
                    print('3 - решить задание')
                    print('2 - посмотреть задание')
                    print('1 - пропустить')
                    answer = -1
                    while answer == -1:
                        try:
                            answer = int(input('> '))
                        except ValueError:
                            print('Введите 3, 2 или 1')
                    #
                    if answer == 2 or answer == 3:
                        self.students[student_id].compl_exercises.append(ex)
                    self.last_choice = []
                    for i in range(5):
                        if not (arg in self.recommendation_dict.keys()):
                            break
                        if self.recommendation_dict[arg] == i:
                            self.last_choice.append(answer)
                        else:
                            self.last_choice.append(0)
                    # Аккумуляция значений для осуществления регуляризуются
                    top_rec = []
                    for i in range(HANDLER_RECOMS):
                        top_rec.append(self.last_recommendation[i][0])
                        self.total_choises[i] += self.last_choice[i]
                    self.total_recommendations.append(top_rec)
                    self._norm_counter += 1
                    # Через каждые 5 ответов веса 
                    # регуляризуются гребневой регрессией
                    if self._norm_counter == 5:
                        self._ridge.fit(self.total_recommendations, \
                            self.total_choises)
                        self.weights = self._ridge.predict( \
                            self.total_recommendations)
                        self.total_recommendations = []
                        self.total_choises = [0, 0, 0, 0, 0]
                        self._norm_counter = 0
                    #
                    self.calculate_weights()
                    #
                    rec = self.generate_recommendation(\
                        self.students[student_id])
                    print('Рекомендуемые задания')
                    for pair in rec[:HANDLER_SHOWN]:
                        print(pair[0])
    #
#
if __name__ == '__main__':
    system = TestSystem()
    # print(system.max_difficulty_handler(system.students['46'])[:3])
    # print(system.tags_handler(system.students['46'])[:3])
    # print(system.completeness_handler(system.students['46'])[:3])
    # print(system.interest_handler(system.students['46'])[:3])
    # print(system.collaboration_handler(system.students['46']))
    
    system.start_REPL()
    '''
    chosen = system.students['46']
    # print(chosen.completed_exercises())
    print(len(chosen.uncompleted_exercises()))
    #
    th = system.themes['5']
    tags = chosen.completed_tags(th)
    untags = chosen.uncompleted_tags(th)
    print(tags)
    print(untags)
    #
    print(chosen.exercise_completeness(th))
    print(chosen.reward_completeness(th))
    '''
#
