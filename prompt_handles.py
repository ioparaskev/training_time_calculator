__author__ = 'ioparaskev'
import re
import logging


class Response(object):
    def __init__(self):
        self.p_ans = tuple()
        self.csens = 'off'
        self.ans_restrict = None
        self.regx = r''
        self.str_restriction = lambda x: False
        self.restrictions = dict(str_restr=False, regx=False)

    def set_restrictions(self, case_sensitive='on', possible_answers=tuple(),
                         answer_restrictions=None):
        self.case_sensitive = case_sensitive
        self.possible_answers = possible_answers
        self.answer_restriction = answer_restrictions

    @property
    def case_sensitive(self):
        return self.csens

    @case_sensitive.setter
    def case_sensitive(self, val):
        if val not in ('on', 'off'):
            raise ValueError('Only bool values allowed for case sensitive set!')
        self.csens = val

    @property
    def possible_answers(self):
        return self.p_ans

    @possible_answers.setter
    def possible_answers(self, val):
        self.p_ans = val

    @property
    def answer_restriction(self):
        return self.ans_restrict

    def enable_restriction(self, restriction_type, restriction_value):
        self.restrictions[restriction_type] = True
        if restriction_type == 'str_restr':
            self.str_restriction = restriction_value
        else:
            self.regx = restriction_value

    @staticmethod
    def get_usual_str_restriction_functions():
        return dict(alpha=lambda x: x.isalpha(),
                    num=lambda x: x.isnumeric(),
                    alphanum=lambda x: x.isalnum())

    @staticmethod
    def is_str_restriction(restriction):
        return restriction in Response.get_usual_str_restriction_functions().keys()

    def set_str_restriction(self, restriction):
        restrict_func = self.get_usual_str_restriction_functions()[restriction]
        self.restrictions_match_possible_answers(restriction=restrict_func)
        self.enable_restriction('str_restr', restrict_func)


    @answer_restriction.setter
    def answer_restriction(self, val):
        if not val:
            return

        if self.is_str_restriction(val):
            self.set_str_restriction(val)
        elif self.is_regex(val):
            regx = val.strip("regex:")
            self.restrictions_match_possible_answers(regex=regx)
            self.enable_restriction('regx', regx)
        else:
            raise NotImplementedError('Wrong restriction given\n'
                                      'Use --help to see possible restrictions')

        self.ans_restrict = True

    @staticmethod
    def is_regex(regex_keyword):
        starts_with_keyword = regex_keyword.find("regex:")
        if starts_with_keyword == -1:
            return False
        elif starts_with_keyword > 0:
            raise RuntimeError("To enter a regex you should enter "
                               "'regex:'[regex_expression]")
        return True

    def restrictions_match_possible_answers(self, restriction=None, regex=None):
        err = RuntimeError('Possible given answers do not match restriction!')
        if restriction:
            for answer in self.possible_answers:
                if not restriction(answer):
                    raise err
        elif regex:
            for answer in self.possible_answers:
                if not self.match_regex(answer):
                    raise err

    def match_possible_answers(self, answer):
        if self.case_sensitive == 'on':
            answer = answer.upper()
            answers = []
            for ans in self.possible_answers:
                answers.append(ans.upper())
            self.possible_answers = tuple(answers)

        if answer not in self.possible_answers:
            return False
        else:
            return True

    def match_regex(self, sentence):
        pattern = re.compile(self.regx)
        if pattern.match(sentence).group() == sentence:
            return True
        else:
            return False

    def match_answer_restriction(self, answer):
        if self.restrictions['str_restr'] and not self.str_restriction(answer):
            return False
        elif self.restrictions['regx'] and not self.match_regex(answer):
            return False
        else:
            return True

    def match_restrictions(self, answer):
        if self.possible_answers:
            return self.match_possible_answers(answer)

        if self.answer_restriction:
            return self.match_answer_restriction(answer)

        return True

    def get_prompt_response(self, question):
        answer = None
        for x in range(3):
            ans = input(question)
            if self.match_restrictions(ans):
                answer = ans
                break

        if not answer:
            raise RuntimeError('Wrong answer given 3 times\nExiting')
        else:
            return answer


class PromptWrapper(object):
    def __init__(self, question, case_sensitive='off', accepted_answers=tuple(),
                 answer_type_restriction=None):
        self.question = question
        self.case_sensitive = case_sensitive
        self.accepted_answers = accepted_answers
        self.answer_type_restriction = answer_type_restriction
        self.response = Response()

    def set_restrictions(self, case_sensitive='off', possible_answers=tuple(),
                         answer_restrictions=None):
        self.response.set_restrictions(case_sensitive, possible_answers,
                                       answer_restrictions)

    def get_prompt_answer(self):
        answer = None
        try:
            answer = self.response.get_prompt_response(self.question)
        except RuntimeError as error:
            logging.error(error)
        finally:
            return answer