import mistune

from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=10,
        widget=forms.widgets.Input(
            attrs={'style':"background-color: #ffffff;border-radius: 40px;font-size:15px; border:1px solid #BFBFBF;height: 30px;padding-left: 10px; ",'placeholder':'"少侠！请留下姓名！"' }
        )
    )

    content = forms.CharField(
        label="内容",
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={'style':"background-color: #ffffff;border-radius: 10px;border:1px solid #BFBFBF;min-height: 100px;width: 100%;padding-left: 10px;" }
        )
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('内容长度怎么能这么短呢！！')
        content = mistune.markdown(content)
        return content

    class Meta:
        model = Comment
        fields = ['nickname', 'content']
