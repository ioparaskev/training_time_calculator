from prompt_handler import prompt_handles

__author__ = 'ioparaskev'

from unittest import TestCase, mock


def mock_input(func):
        def mock_input_builtin(*args):
            with mock.patch('builtins.input', return_value=args[-1]):
                return func(*args)
        return mock_input_builtin


class TestPromptWrapper(TestCase):
    def setUp(self):
        question = 'Test ?'
        self.prompt = prompt_handles.PromptWrapper(question)

    @mock_input
    def get_mocked_answer(self, mocked_ans):
        return self.prompt.get_prompt_answer()

    def test_wrong_restriction(self):
        with self.assertRaises(NotImplementedError):
            self.prompt.set_restrictions(answer_restrictions='test')

    def test_wrong_regex_restriction(self):
        with self.assertRaises(RuntimeError):
            self.prompt.set_restrictions(answer_restrictions='abc regex:')

    def test_wrong_case_sensitive_set(self):
        with self.assertRaises(ValueError):
            self.prompt.set_restrictions(case_sensitive='Test')

    def test_get_prompt_answer_not_approved(self):
        with self.assertRaises(RuntimeError):
            self.prompt.set_restrictions(possible_answers=('yes', 'no'))
            answer = self.get_mocked_answer('asd123')
            self.assertEqual(None, answer)

    def test_get_prompt_answer_approved(self):
        self.prompt.set_restrictions(possible_answers=('yes', 'no'))
        answer = self.get_mocked_answer('yes')
        self.assertEqual('yes', answer)

    def test_get_prompt_answer_anything(self):
        answer = self.get_mocked_answer('1')
        self.assertEqual('1', answer)

    def test_get_prompt_answer_only_nums_wrong(self):
        with self.assertRaises(RuntimeError):
            self.prompt.set_restrictions(answer_restrictions='num')
            answer = self.get_mocked_answer('tt')
            self.assertEqual(None, answer)

    def test_get_prompt_answer_only_nums_correct(self):
        self.prompt.set_restrictions(answer_restrictions='num')
        answer = self.get_mocked_answer('123')
        self.assertEqual('123', answer)

    def test_get_prompt_answer_only_alpha_wrong(self):
        with self.assertRaises(RuntimeError):
            self.prompt.set_restrictions(answer_restrictions='alpha')
            answer = self.get_mocked_answer('12asd')
            self.assertEqual(None, answer)

    def test_get_prompt_answer_only_alpha_correct(self):
        self.prompt.set_restrictions(answer_restrictions='alpha')
        answer = self.get_mocked_answer('asd')
        self.assertEqual('asd', answer)

    def test_get_prompt_answer_only_alphanumeric_wrong(self):
        with self.assertRaises(RuntimeError):
            self.prompt.set_restrictions(answer_restrictions='alphanum')
            answer = self.get_mocked_answer('12asd_')
            self.assertEqual(None, answer)

    def test_get_prompt_answer_only_alphanum_correct(self):
        self.prompt.set_restrictions(answer_restrictions='alphanum')
        answer = self.get_mocked_answer('asd123')
        self.assertEqual('asd123', answer)

    def test_get_prompt_answer_regex_wrong_answer(self):
        with self.assertRaises(RuntimeError):
            self.prompt.set_restrictions(answer_restrictions='regex:(\w+)')
            answer = self.get_mocked_answer('hey!!~')
            self.assertEqual(None, answer)

    def test_get_prompt_answer_regex_correct_answer(self):
        self.prompt.set_restrictions(answer_restrictions='regex:yes|no')
        answer = self.get_mocked_answer('yes')
        self.assertEqual('yes', answer)

    def test_get_prompt_answer_regex_correct_answer_2(self):
        self.prompt.set_restrictions(answer_restrictions='regex:(\w+)')
        answer = self.get_mocked_answer('yes')
        self.assertEqual('yes', answer)

    def test_string_restriction_no_match_possible_answers(self):
        with self.assertRaises(RuntimeError):
            self.prompt.set_restrictions(possible_answers=('yes!', 'no!'),
                                         answer_restrictions='alpha')

    def test_regex_restriction_no_match_possible_answers(self):
        with self.assertRaises(RuntimeError):
            self.prompt.set_restrictions(possible_answers=('yes!', 'no!'),
                                         answer_restrictions='regex:\w+')

    def test_prompt_answer_case_sensitive_ok(self):
        self.prompt.set_restrictions(case_sensitive='on',
                                     possible_answers=('Yes', 'No'))
        answer = self.get_mocked_answer('Yes')
        self.assertEqual('Yes', answer)