from kahnsept import *
from parse_date import *

import unittest
import datetime

class TestDateParse(unittest.TestCase):
    def test_dates(self):
        for test in ['01/01/09', '1/1/09', '1/1/2009', 'Jan 1, 09', 'Jan 1, 2009', 'January 1, 2009',
                     '2009-01-01', '1.1.09']:
            dt = parse_date(test)
            self.assertNotEqual(dt, None, test)
            if dt is not None:
                self.assertEqual(dt.date(), datetime.date(2009,1,1), test)
                
    def test_times(self):
        for test in ['1/1/09 13:17', '1/1/09 1:17 pm']:
            dt = parse_date(test)
            self.assertNotEqual(dt, None, test)
            if dt is not None:
                self.assertEqual(dt, datetime.datetime(2009,1,1,13,17))

class TestBasics(unittest.TestCase):
    def test_entity(self):
        e = Entity('Test')
        self.assertEqual(e.name, 'Test')
        
        e2 = Entity('Test')
        self.assert_(e is e2)
        
    def test_property(self):
        e = Entity('Test')
        
        p = e.add_prop(e, 'fred')
        self.assertNotEqual(e.get_prop('fred'), None)
        
    def test_single(self):
        e = Entity("Single")
        e.add_prop(Text)
        i = e.new()
        i.Text = "fred"
        self.assertEqual(len(i.Text), 4)
        
    def test_many(self):
        m = Entity('Many')
        m.add_prop(Text, card=Card.many)
        
        i = m.new()
        self.assertEqual(len(i.Text), 0)
        
        i.Text = "first"
        self.assertEqual(len(i.Text), 1)
        self.assertEqual(i.Text[0], "first")
        
        i.Text = "second"
        self.assertEqual(len(i.Text), 2)
        self.assert_("first" in i.Text)
        self.assert_("second" in i.Text)
        
    def test_instance(self):
        e = Entity('Test')
        i = e.new()
        
        self.assertEqual(i._entity, e)
        
    def test_relation(self):
        e1 = Entity('Test')
        e2 = Entity('Test2')
        r = Relation(e1, e2)
        
        self.assertEqual(r.names, ['Test2', 'Test'])
        self.assertEqual(r.cards, [Card.many_many, Card.many_many])
        
        self.assertNotEqual(e1.get_prop('Test2'), None)
        self.assertNotEqual(e2.get_prop('Test'), None)
        
        i1 = e1.new()
        i2 = e2.new()
        
        i1.Test2 = i2
        
        self.assertEqual(i1.Test2[0], i2)
        self.assertEqual(i2.Test[0], i1)

class TestRelations(unittest.TestCase):
    def test_x(self):
        pass
        
class TestBuiltins(unittest.TestCase):
    def test_builtin(self):
        e = Entity('Test')
        e.add_prop(Number)
        e.add_prop(Text)
        e.add_prop(Boolean)
        e.add_prop(Date)
        
        e.Number = 1
        self.assertEqual(e.Number, 1)
        
        e.Text = "hello"
        self.assertEqual(e.Text, "hello")
        
        e.Boolean = True
        self.assertEqual(e.Boolean, True)
        
        e.Date = now = datetime.datetime.now()
        self.assertEqual(e.Date, now)
        
class TestCoercion(unittest.TestCase):
    def test_pass(self):
        e = Entity('Test')
        e.add_prop(Number)
        e.add_prop(Text)
        e.add_prop(Boolean)
        e.add_prop(Date)
        e.add_prop(e, 'parent')
        
        i = e.new()
        i2 = e.new()
        i.Number = "7"
        i.Text = 1
        i.Boolean = 1
        i.Date = "1/1/2009"
        i.parent = i2
        self.assertEqual(i.Number, 7)
        self.assertEqual(i.Text, "1")
        self.assertEqual(i.Boolean, True)
        self.assertEqual(i.Date.date(), datetime.date(2009,1,1))
        self.assertEqual(i.parent[0], i2)
        
    def test_fail(self):
        e = Entity('Test')
        e.add_prop(Number)
        i = e.new()
        
        def throws():
            i.Number = "a"
            
        self.assertRaises(Exception, throws)
        
class TestSample(unittest.TestCase):
    def test_sample(self):
        Test = Entity('Test')
        Question = Entity('Question')
        QuestionType = Entity('QuestionType')
        Score = Entity('Score')
        User = Entity('User')
        UserAnswer = Entity('UserAnswer')
        ScoringDimension = Entity('ScoringDimension')
        PossibleAnswer = Entity('PossibleAnswer')
        
        Test.add_prop(Text, 'title')
        User.add_prop(Text, 'name')
        Question.add_prop(Text, 'prompt')
        QuestionType.add_prop(Text)
        Score.add_prop(Number, 'amplitude')
        ScoringDimension.add_prop(Text)
        UserAnswer.add_prop(Text, 'data')
        UserAnswer.add_prop(Date)
        PossibleAnswer.add_prop(Text, 'data')
        PossibleAnswer.add_prop(Number, 'delta_score')
        
        Relation(Test, Question, Card.many_many)
        Relation(Test, Score, Card.one_many)
        
        Relation(Question, PossibleAnswer, Card.one_many)
        Relation(Question, UserAnswer, Card.one_many)
        
        Relation(QuestionType, Question, Card.one_many)

        Relation(PossibleAnswer, UserAnswer, Card.one_many)
        
        Relation(User, Score, Card.one_many)
        Relation(User, UserAnswer, Card.one_many)
        
        Relation(ScoringDimension, Score, Card.one_many)
        Relation(ScoringDimension, PossibleAnswer, Card.one_many)
        
        t = Test.new()
        t.title = "First Test"
        
        qt = QuestionType.new()
        qt.Text = "multiple_choice"
        
        q = Question.new()
        q.QuestionType = qt
        q.prompt = "What is your favorite color?"
        
        sd = ScoringDimension.new()
        sd.Text = "heat"
        
        for color,score in [('red', 2), ('blue', -1), ('yellow', 1)]:
            pa = PossibleAnswer.new()
            pa.ScoringDimension = sd
            pa.data = color
            pa.delta_score = score
            q.PossibleAnswer.add(pa)
            
        u = User.new()
        u.name = "Fred"
        
        ua = UserAnswer.new()
        ua.User = u
        ua.Question = q
        ua.data = "blue"
        ua.Date = "12/25/09"
        
        s = Score.new()
        s.Test = t
        s.User = u
        
        raw_score = 0
        for uaT in u.UserAnswer:
            for pa in uaT.Question.PossibleAnswer:
                if pa.data == uaT.data:
                    raw_score += pa.delta_score

        s.amplitude = raw_score
        
        self.assertEqual(s.amplitude, -1)

if __name__ == '__main__':
    unittest.main()