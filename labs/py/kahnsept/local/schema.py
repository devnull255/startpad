"""
Kahnsept Schema - a simple language for specifying network data models

    Example:
    
    Entities:
    ---------
    Test
        title<Text>         // (Type (Text) is optional - uppercase props and Entity names, lower case are assumed Text props)
        Question(s)->       // (s) (represents a many-many relationship)

    Question
        prompt
        QuestionType        // No Relation specified -> many-to-one relationship
        PossibleAnswer(s)   // (s) indicates one-to-many relationship
        Test(s)/(s)         // (s) on both sides indicates a many-to-many relationship
        
    QuestionType
        Text

    PossibleAnswer
        data
        delta_score<N>      // Abbrev for <N> Number <T> Text <?> Boolean <D> Date ? 
    
    User
        name
        UserAnswer(s)
        Score(s)
        
    UserAnswer
        Question
        data
        Date

    Score
        User
        Test
        ScoringDimension
        amplitude<Number>

    ScoringDimension
        Text
    
    Relations: // Redundant with above - can define either inline, or separately here
    ----------
    Test(s)/Question(s)
    Test/Score(s)
    
    Question, PossibleAnswer(s)
    Question, UserAnswer(s)
    
    Question(s), QuestionType
    UserAnswer(s), PossibleAnswer
    
    User, Score(s)
    User, UserAnswer(s)
    
    Score(s), ScoringDimension
    PossibleAnswer(s), ScoringDimension
    
An example with relationship names:

    Entities:
    ---------
    Person
        name
        parent<Person(s)>/child(s)
        
        
    Relations:
    ----------
    parent<Person(s)>/child<Person(s)>
    
Another example:

    Entities:
    ---------
    Class
        name
        Student(s)
        Teacher
        Schedule
        
    Student
        name
        Class(s)
        
    Teacher
        name
        Class(s)
        
    Schedule
        start<Date>
        end<Date>
        days_of_week
        time_start<Time>  // BUG: Want Time to be "owned" - so can't be one-many - allow multiple Time with same values
        time_end<Time>
        
    Time
        hour<N>
        min<N>
"""