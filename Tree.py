from difflib import SequenceMatcher
from operator import itemgetter


class ParentNode:
    def __init__(self, question, answers):
        self.question = question
        self.answers = answers

    def ask_question(self):
        print(f"Can you give me an answer to this question:\n {self.question}")

    def get_correctness_list(self, answer):
        correctness_list = []
        for real_answer in self.answers:
            correctness = self.get_correctness_in_percents(answer, real_answer.answer)
            correctness_list.append(correctness)
        return sorted(list(enumerate(correctness_list)), key=itemgetter(1), reverse=True)

    @staticmethod
    def get_correctness_in_percents(first, second):
        first.replace(" ", "")
        second.replace(" ", "")
        return SequenceMatcher(None, first, second).ratio()


class InnerNode(ParentNode):
    def __init__(self, question, answers, answer, is_correct):
        super().__init__(question, answers)
        self.answer = answer
        self.is_correct = is_correct


class Tree:
    match_percents = 0.7

    def __init__(self, parent_node):
        self.parent_node = parent_node
        self.correct_counter = 0
        self.absolute_counter = 0

    def ask_a_user(self):
        current_node = self.parent_node
        while current_node is not None:
            if current_node.question is None:
                print("There is a bottom of the tree / game is over!")
                break
            self.absolute_counter += 1
            current_node.ask_question()
            entered_answer = input("Answer: ")
            correctness_list = current_node.get_correctness_list(entered_answer)
            available_correctness_list = [item for item in correctness_list if item[1] >= self.match_percents]
            for item in available_correctness_list:
                if item[1] == 1.0:
                    current_node = current_node.answers[item[0]]
                    self.correct_counter += current_node.is_correct
                    break
                else:
                    decision = input(f"Is an answer {current_node.answers[item[0]].answer} exactly what you meant to answer?: ")
                    if decision == "Yes":
                        current_node = current_node.answers[item[0]]
                        self.correct_counter += current_node.is_correct
                        break
            else:
                current_node = current_node.answers[0] if len(current_node.answers) != 0 else None
        print(f"Accuracy: {self.correct_counter / self.absolute_counter}")

    def ask_a_tree(self):
        pass

    @staticmethod
    def injector():
        el_1 = InnerNode(None, None, "Молоко", True)
        el_2 = InnerNode("Что нужно выпить, чтобы нейтрализовать остроту от чили?",
                         [el_1, ],
                         "Чили",
                         True)
        el_3 = InnerNode(None,
                         None,
                         "Лук",
                         False)
        el_4 = InnerNode("Любимая пряность в Мексике?",
                         [el_2, el_3],
                         "Мексика",
                         True)
        el_5 = InnerNode("Какая страна является родиной тыквы?",
                         [el_4, ],
                         "Тыква",
                         True)
        el_6 = InnerNode("Что скрестили селекционеры с арбузом, чтобы получить кавбуз?",
                         [el_5, ],
                         "Арбуз",
                         True)
        el_7 = InnerNode("Какая ягода имеет в себе такое же содержание воды, что и дыня?",
                         [el_6, ],
                         "Дыня",
                         True)
        el_8 = InnerNode(
            "Самый дорогой фрукт, выращиваемый в Японии, который был продан на аукционе за 23500 долларов?",
            [el_7, ],
            "Япония",
            True)
        el_9 = InnerNode("В какой стране была выращена самая крупная груша?",
                         [el_8, ],
                         "Груша",
                         True)
        el_10 = InnerNode("Что напоминают плоды гуавы?",
                          [el_9, ],
                          "Гуава",
                          True)
        el_11 = InnerNode(None,
                          None,
                          "Лимон",
                          True)
        el_12 = ParentNode("Чемпионом по содержанию витамина С является?",
                           [el_10, el_11])
        return Tree(el_12)


if __name__ == "__main__":
    pass
