from django import forms


class BibTeXImportForm(forms.Form):
    bibtex_text = forms.CharField(
        label="粘贴 BibTeX",
        required=False,
        widget=forms.Textarea(attrs={"rows": 14, "style": "width: 100%; font-family: monospace;"}),
        help_text="可以一次粘贴多条 BibTeX 记录。",
    )
    bibtex_file = forms.FileField(
        label="上传 BibTeX 文件",
        required=False,
        help_text="支持 .bib 或 .txt 文件。",
    )

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("bibtex_text") and not cleaned.get("bibtex_file"):
            raise forms.ValidationError("请粘贴 BibTeX 内容，或上传一个 BibTeX 文件。")
        return cleaned
