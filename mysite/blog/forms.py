from django import forms

from .models import Post, Comment, Ingredients

class PostForm(forms.ModelForm):
	
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
    	fields = ('name', )


