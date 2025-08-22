from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
import requests

from langchain_openai import ChatOpenAI

from accounts.permissions import ai_access_required
from .forms import ChatForm, ChatModelForm, CreateChatModelForm
from .models import Chat, Message, ChatModel

API_KEY = settings.AVAL_API_KEY

@staff_member_required
def AiView(request):
    context = dict(
        page_title = 'ai'
    )
    all_messages = None
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
            # Initialize all_messages list with system and user prompts
            all_messages = [        
                {"role": "user", "content": cd['prompt']},
            ]
            # Initialize all_messages list with system and user prompts
            # all_messages = [        
            #     {"role": "user", "content": "in less than 30 words define django rest framework serializer"},
            # ]
            
            # ai_message = llm.invoke(all_messages)
            form = ChatForm()
    else: 
        form = ChatForm()
    context.update(
        model_name=model_name,
        all_messages=all_messages,
        ai_message=ai_message,
        form=form
    )
    return render(
        request,
        'ai/ai_home.html',
        context
    )

@login_required
@ai_access_required
def AiCreateNewChatView(request, chat_id=None):
    context = dict(
        page_title = 'create ai chat',
        chats=Chat.objects.filter(user=request.user).order_by('-id'),
    )
    all_messages = None
    ai_message = []
    chat=None
    ai_response = None   
    uploaded_file = ''
    last_message_id = None
     
    if chat_id:
        try:
            chat=get_object_or_404(Chat, chat_id=chat_id, user=request.user)
            all_messages = Message.objects.filter(chat=chat).order_by('created')
            for item in all_messages:
                ai_message.append({"role": item.role, "content": item.content})            
            last_message_id = all_messages.last().id
        except:
            messages.warning(request, 'Chat not found')
            return redirect('ai:ai_create')
            
    form_class = ChatForm if chat else ChatModelForm
    
    # Initialize the ChatOpenAI model
    model_name = "gpt-4o-mini" if not chat else chat.model_name
    # model_name = "claude-3-opus"
    
    llm = ChatOpenAI(
        model=model_name, base_url="https://api.avalai.ir/v1", api_key=API_KEY
    )
    
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            uploaded_file = cd['file']
            
            # Read the file content
            file_content = uploaded_file.read().decode('utf-8') if uploaded_file else ''
            # Initialize all_messages list with system and user prompts
            prompt = {"role": "user", "content": f"{cd['prompt']}\n{file_content if file_content else ''}"}
            
            # Make a chat body if it is not exists
            if chat:
                pass
            else:
                model_name = cd['model'].name
                chat = Chat.objects.create(
                    user=request.user,
                    chat_id='working',
                    model_name=model_name,
                    input_token=0,
                    output_token=0,
                    total_token=0,
                )
                chat_model = ChatModel.objects.get(name=model_name)
                chat_model.usage_count += 1
                chat_model.save(update_fields=['usage_count'])
                print('.. create chat body new')
            
            # jsut for record
            new_message = Message.objects.create(
                chat=chat,
                role='user',
                content=cd['prompt'],
                file = cd['file'],
                file_type=cd['file_type'],
            )
            print('.. add prompt')
                
            ai_message.append(prompt)
            
            try:
                
                ai_response = llm.invoke(ai_message)
                pass
            except Exception as e:
                print(str(e))
            
            # ai_message = llm.invoke(all_messages)
            
            if ai_response:
                print('.. get ai response')
                chat.chat_id = ai_response.id
                chat.input_token=ai_response.usage_metadata["input_tokens"]
                chat.output_token=ai_response.usage_metadata["output_tokens"]
                chat.total_token=ai_response.usage_metadata["total_tokens"]
                chat.save()
                
                prompt_content = ai_response.content
                answer_message = Message.objects.create(
                    chat=chat,
                    role='assistant',
                    content=prompt_content,
                )
                messages.success(request, 'new chat created')
                
                return redirect('ai:ai_continue_chat', chat.chat_id)
            
    else: 
        form = form_class()
    # for index,item in enumerate(ai_message):
    #     print(f"{index}:{item}")
    context.update(
        model_name=model_name,
        all_messages=all_messages,
        ai_message=ai_message,
        form=form,
        chat=chat,
        last_message_id=last_message_id,
        mainNavSection='ai',
    )
    return render(
        request,
        'ai/ai_chat.html',
        context
    )

@staff_member_required
def AiModelsListView(request):
    url = "https://api.avalai.ir/v1/models"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()['data']
    sorted_data = sorted(data, key=lambda item: (item.get('min_tier'), item.get('owned_by', '')))
    
    context = dict(
        page_title = 'ai models list',
        models_added=ChatModel.objects.all().values_list('name', flat=True),
        sorted_data=sorted_data,
    )
    return render(
        request,
        'ai/ai_models_list.html',
        context
    )    

@staff_member_required
def AiModelAddView(request):
    if request.method == 'POST':
        form = CreateChatModelForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New model added')
            return redirect('ai:ai_models_list')
        else:
            messages.warning(request, 'Model does not added, check the form')            
            print(form.errors)
            return redirect('ai:ai_models_list')
    else:
        form = CreateChatModelForm()
    
    context = dict(
        page_title = 'add ai model',
        form=form,
    )
    return render(
        request,
        'ai/ai_model_add.html',
        context
    )   
