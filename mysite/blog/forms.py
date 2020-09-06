from django import forms

from .models import Post, Comment, Ingredients

class PostForm(forms.ModelForm):
    choices = [(ingredient.pk, ingredient.name) for ingredient in Ingredients.objects.all()]
    recipes = forms.MultipleChoiceField(required=False, choices=choices)
	
    class Meta:
        model = Post
        fields = ('title', 'cooking_method', 'ingredients', 'image' )

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'cooking_method',)

class IngredientForm(forms.ModelForm):

    class Meta:
    	model = Ingredients
    	fields = ('name','quantity')


