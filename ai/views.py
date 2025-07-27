from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from langchain_openai import ChatOpenAI

API_KEY = settings.AVAL_API_KEY

@staff_member_required
def AiView(request):
    context = dict(
        page_title = 'ai'
    )
    
    # Initialize the ChatOpenAI model
    model_name = "gpt-4o-mini"
    llm = ChatOpenAI(
        model=model_name, base_url="https://api.avalai.ir/v1", api_key=API_KEY
    )

    # Initialize messages list with system and user prompts
    messages = [        
        {"role": "user", "content": "in less than 100 words define django rest framework serializer"},
    ]
    
    ai_message = llm.invoke(messages)
    
    context.update(
        model_name=model_name,
        messages=messages,
        ai_message=ai_message
    )
    return render(
        request,
        'ai/ai_home.html',
        context
    )






