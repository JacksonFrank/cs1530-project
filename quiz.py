# Class that represents an instance of a quiz

from database_access.lctdb import LCTDB
import enum
import random

class QuizAnswer(enum.Enum):
    english = 0
    mandarin = 1

class Quiz:

    def __init__(self, level: int):
        self.quiz_questions = []
        self.level = level
        db_connection = LCTDB()
        quiz_data = db_connection.getQuizQuestions(level)
        for pair in quiz_data:
            self.quiz_questions.append(QuizQuestion(pair[0], pair[1], 3, QuizAnswer(random.randint(0, 1))))
        db_connection.closeCon()
    
    # returns the number of questions left of the current quiz
    def questionsLeft(self):
        return len(self.quiz_questions)
    
    # returns a QuizQuestion object
    # also removes this question from the existing list of questions
    def popQuizQuestion(self):
        return self.quiz_questions.pop(0)
    
    # saves that this quiz was completed in the database
    def quizCompleted(self, username: str):
        db_connection = LCTDB()
        db_connection.quizCompleted(username, self.level)
        db_connection.closeCon()


class QuizQuestion:

    # creates the question
    # randomly retrieves the specificed number of random answers to function as wrong answers
    def __init__(self, english_tr: str, mandarin_tr: str, wrong_ans_num: int, answer_type: QuizAnswer):
        self.english_tr = english_tr
        self.mandarin_tr = mandarin_tr
        self.answer_type = answer_type
        self.wrong_answers = []

        db_connection = LCTDB()
        result_data = None

        if (answer_type == QuizAnswer.english):
            result_data = db_connection.getRandomAnswers(True, english_tr, wrong_ans_num)
        elif (answer_type == QuizAnswer.mandarin):
            result_data = db_connection.getRandomAnswers(False, mandarin_tr, wrong_ans_num)

        db_connection.closeCon()
        
        for result in result_data:
            self.wrong_answers.append(result[0])
    
    # gets the question translation portion
    def getQuestion(self):
        if (self.answer_type == QuizAnswer.english):
            return self.mandarin_tr
        elif (self.answer_type == QuizAnswer.mandarin):
            return self.english_tr
        return None

    # gets the correct answer translation for this question
    def getAnswer(self):
        if (self.answer_type == QuizAnswer.english):
            return self.english_tr
        elif (self.answer_type == QuizAnswer.mandarin):
            return self.mandarin_tr
        return None

    # gets wrong answers
    def getWrongAnswers(self):
        return self.wrong_answers      




        
