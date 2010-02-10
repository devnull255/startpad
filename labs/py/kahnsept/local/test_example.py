from kahnsept import *

import interactive

if __name__ == '__main__':
    Entity('Test').add_prop(Text, 'title')

    Entity('Question').add_prop(Text, 'prompt')
    
    Entity('QuestionType').add_prop(Text)
    
    Entity('Score').add_prop(Number, 'amplitude')
    
    Entity('User').add_prop(Text, 'name')
    
    Entity('UserAnswer').add_prop(Text, 'data')
    UserAnswer.add_prop(Date)
    
    Entity('ScoringDimension').add_prop(Text)
    
    Entity('PossibleAnswer').add_prop(Text, 'data')
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
    
    world.entity_map = None
    
    interactive.interactive(ext_map=globals(), locals=world.scope, encoder=kahnsept.InteractiveEncoder)