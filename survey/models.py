from django.db import models
from CustomUser.models import User

from django.urls import reverse
from django.utils.text import slugify


"""
참고한 코드: https://github.com/Pierre-Sassoulas/django-survey/
"""

def validate_choices(choices):
    """Verifies that there is at least two choices in choices
    :param String choices: The string representing the user choices.
    """
    values = choices.split(',')
    empty = 0
    for value in values:
        if value.replace(" ", "") == "":
            empty += 1
    if len(values) < 2 + empty:
        msg = "The selected field requires an associated list of choices."
        msg += " Choices must contain more than one item."
        raise ValidationError(msg)

        
        
"""
Models starts here!
"""

# Post를 ForeignKey로 가지는 모델들: Question, Response
class Post(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    # TODO: DateTimeField가 말썽을 부려서 무식한 방법을 썼습니다... 이부분 수정할때까지 해를 넘기는 설문은 만들지 말아주세요. 
    end_month = models.CharField(max_length=2, null=True)
    end_day =models.CharField(max_length=2, null=True)
    visible = models.BooleanField(max_length=2, null=True)
    
    def get_absolute_url(self):
        return reverse("survey-detail", kwargs={"id": self.pk})

    def __str__(self):
        return self.subject
    
    
# Question을 ForeignKey로 가지는 모델들: Answer
class Question(models.Model): 
    subject = models.CharField(max_length=200)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    
    # 선택지는 문자열로 저장되며 필요할때 그때그때 get_choices 활용하여 tuple 형태로 리턴해주면 됩니다. 
    choices = models.TextField()
    
    
    def save(self, *args, **kwargs):
        validate_choices(self.choices)
        super().save(*args, **kwargs)
    
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
        return tuple(self.get_clean_choices())
        #return choices_tuple
    
    # 선택지를 list 형태로 리턴해줍니다. 
    def get_clean_choices(self):
        """Return split and stripped list of choices with no null values."""
        if self.choices is None:
            return []
        choices_list = []
        for choice in self.choices.split(','):
            choice = choice.strip()
            if choice:
                choices_list.append(choice)
        return choices_list

    def __str__(self):
        msg = f"Question '{self.content}' "
        msg += f"{self.get_clean_choices()}"
        return msg
    
    
# Response를 ForeignKey로 가지는 모델들: Answer
class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.SET_NULL)
    
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        msg = f"Response to {self.post} by {self.author}"
        msg += f" on {self.created}"
        return msg
    
   
class Answer(models.Model): 
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    response = models.ForeignKey(Response, on_delete=models.SET_NULL, null=True)
    
    body = models.TextField()
    
    
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
        
        
