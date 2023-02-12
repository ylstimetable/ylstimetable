from django.db import models
from CustomUser.models import User

"""
참고한 코드: https://github.com/Pierre-Sassoulas/django-survey/
"""

# Post를 ForeignKey로 가지는 모델들: Question, Response
class Post(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    end_date = models.DateTimeField()
    visible = models.BooleanField(max_length=2, null=True)

    def __str__(self):
        return self.subject
    
# Question을 ForeignKey로 가지는 모델들: Answer
class Question(models.Model): 
    subject = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    
    # 선택지는 문자열로 저장되며 필요할때 그때그때 get_choices 활용하여 tuple 형태로 리턴해주면 됩니다. 
    choices = models.TextField(_("Choices"), blank=True, null=True, help_text=CHOICES_HELP_TEXT)
    
    def __str__(self): 
        return self.subject
    
    # 선택지를 tuple 형태로 리턴해줍니다. 
    def get_choices(self):
        """
        Parse the choices field and return a tuple formatted appropriately
        for the 'choices' argument of a form widget.
        """
        choices_list = []
        for choice in self.get_clean_choices():
            choices_list.append((slugify(choice, allow_unicode=True), choice))
        choices_tuple = tuple(choices_list)
        return choices_tuple
    
    # 선택지를 list 형태로 리턴해줍니다. 
    def get_clean_choices(self):
        """Return split and stripped list of choices with no null values."""
        if self.choices is None:
            return []
        choices_list = []
        for choice in self.choices.split(settings.CHOICES_SEPARATOR):
            choice = choice.strip()
            if choice:
                choices_list.append(choice)
        return choices_list

    
# Response를 ForeignKey로 가지는 모델들: Answer
class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    post = models.ForeignKey(Post, null=True, blank=True,
                                 on_delete=models.SET_NULL)
   
class Answer(models.Model): 
    question = models.ForeignKey(Question, on_delete=models.SET_NULL)
    response = models.ForeignKey(Response, on_delete=models.SET_NULL)
    created = models.DateTimeField(_("Creation date"), auto_now_add=True)
    
    body = models.TextField(_("Content"), blank=True, null=True)
    
    
    def __init__(self, *args, **kwargs):
        try:
            question = Question.objects.get(pk=kwargs["question_id"])
        except KeyError:
            question = kwargs.get("question")
        body = kwargs.get("body")
        if question and body:
            self.check_answer_body(question, body)
            self.validate()
        super().__init__(*args, **kwargs)
        
        
    # TODO: 이 Answer가 속해있는 question과 response가 같은 post에 속해있는지 확인해줄것
    def validate(self):
        None   
    
    def check_answer_body(self, question, body):
        choices = question.get_clean_choices()
        self.check_answer_for_select(choices, body)
            
    def check_answer_for_select(self, choices, body):
        answers = []
        if body:
            if body[0] == "[":
                for i, part in enumerate(body.split("'")):
                    if i % 2 == 1:
                        answers.append(part)
            else:
                answers = [body]
        for answer in answers:
            if answer not in choices:
                msg = f"Impossible answer '{body}'"
                msg += f" should be in {choices} "
                raise ValidationError(msg)

    def __str__(self):
        return f"'{self.question}' : '{self.body}'"
        
        
