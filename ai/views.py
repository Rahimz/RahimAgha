from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.contrib import messages

from langchain_openai import ChatOpenAI

from .forms import ChatForm, ChatModelForm
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


def AiCreateNewChatView(request, chat_id=None):
    context = dict(
        page_title = 'create ai chat',
        chats=Chat.objects.all().order_by('-id'),
    )
    all_messages = None
    ai_message = []
    chat=None
    ai_response = None   
    uploaded_file = ''
    last_message_id = None
     
    if chat_id:
        try:
            chat=get_object_or_404(Chat, chat_id=chat_id)
            all_messages = Message.objects.filter(chat=chat).order_by('created')
            for item in all_messages:
                ai_message.append({"role": item.role, "content": item.content})            
            last_message_id = all_messages.last().id
        except:
            pass
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
    for index,item in enumerate(ai_message):
        print(f"{index}:{item}")
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
    
    



