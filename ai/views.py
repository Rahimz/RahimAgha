from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.contrib import messages

from langchain_openai import ChatOpenAI

from .forms import ChatForm
from .models import Chat, Message

API_KEY = settings.AVAL_API_KEY

@staff_member_required
def AiView(request):
    context = dict(
        page_title = 'ai'
    )
    ai_messages = None
    ai_message = None
    # Initialize the ChatOpenAI model
    model_name = "gpt-4o-mini"
    # model_name = "claude-3-opus"
    llm = ChatOpenAI(
        model=model_name, base_url="https://api.avalai.ir/v1", api_key=API_KEY
    )
    if request.method == 'POST':
        form = ChatForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Initialize ai_messages list with system and user prompts
            ai_messages = [        
                {"role": "user", "content": cd['prompt']},
            ]
            # Initialize ai_messages list with system and user prompts
            # ai_messages = [        
            #     {"role": "user", "content": "in less than 30 words define django rest framework serializer"},
            # ]
            
            # ai_message = llm.invoke(ai_messages)
            form = ChatForm()
    else: 
        form = ChatForm()
    context.update(
        model_name=model_name,
        ai_messages=ai_messages,
        ai_message=ai_message,
        form=form
    )
    return render(
        request,
        'ai/ai_home.html',
        context
    )


def AiCreateNewChatView(request, chat_id=None):
    context = dict(
        page_title = 'create ai chat',
        chats=Chat.objects.all().order_by('-id'),
    )
    ai_messages = None
    ai_message = None
    chat=None
    if chat_id:
        try:
            chat=get_object_or_404(Chat, chat_id=chat_id)
            ai_messages = Message.objects.filter(chat=chat)
        except:
            pass
    
    
    # Initialize the ChatOpenAI model
    model_name = "gpt-4o-mini"
    # model_name = "claude-3-opus"
    
    llm = ChatOpenAI(
        model=model_name, base_url="https://api.avalai.ir/v1", api_key=API_KEY
    )
    
    if request.method == 'POST':
        form = ChatForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Initialize ai_messages list with system and user prompts
            ai_messages = [        
                {"role": "user", "content": cd['prompt']},
            ]
            chat = Chat.objects.create(
                chat_id='working',
                model_name=model_name,
                input_token=0,
                output_token=0,
                total_token=0,
            )
            print('.. create chat body')
            message = Message.objects.create(
                chat=chat,
                role='user',
                content=cd['prompt']
            )
            print('.. create first chat')
            try:
                ai_message = llm.invoke(ai_messages)
                pass
            except Exception as e:
                print(str(e))
            
            # ai_message = llm.invoke(ai_messages)
            
            if ai_message:
                print('.. get ai response')
                chat.chat_id = ai_message.id
                chat.input_token=ai_message.usage_metadata["input_tokens"]
                chat.output_token=ai_message.usage_metadata["output_tokens"]
                chat.total_token=ai_message.usage_metadata["total_tokens"]
                chat.save()
                
                prompt_content = ai_message.content
                answer_message = Message.objects.create(
                    chat=chat,
                    role='assistant',
                    content=prompt_content,
                )
                messages.success(request, 'new chat created')
                
                return redirect('ai:ai_continue_chat', chat.chat_id)
            
    else: 
        form = ChatForm()
    context.update(
        model_name=model_name,
        ai_messages=ai_messages,
        ai_message=ai_message,
        form=form,
        chat=chat,
    )
    return render(
        request,
        'ai/ai_chat.html',
        context
    )
    
    



