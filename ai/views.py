from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
import requests
import base64
import mimetypes
from pathlib import Path
import datetime
from langchain_openai import ChatOpenAI
from openai import OpenAI
from django.core.files.base import ContentFile
import random
from django.db.models import Count, Case, When, IntegerField, Q

from accounts.permissions import ai_access_required
from .forms import ChatForm, ChatModelForm, CreateChatModelForm
from .models import Chat, Message, ChatModel, FileTypeDetermine

API_KEY = settings.AVAL_API_KEY


def generate_unique_random_number():
    while True:
        # Generate a random number between 1 and 9999999 (7 digits)
        random_number = random.randint(1, 9999999)
        
        # Check if the number is unique in the database
        if not Chat.objects.filter(chat_id=f"working-{random_number}").exists():
            return random_number


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
            
            # if there is no file it returns NA
            file_type = FileTypeDetermine(uploaded_file)
            
            # This list will hold the parts of our message (text and/or image)
            message_content_parts = [
                {"type": "text", "text": cd['prompt']}
            ]
            
            # Read the file content
            if file_type == Message.FileChoices.DOC:
                # just read text files
                file_content = uploaded_file.read().decode('utf-8') if uploaded_file else ''
                # Initialize all_messages list with system and user prompts
                prompt = {"role": "user", "content": f"{cd['prompt']}\n{file_content if file_content else ''}"}
            elif file_type == Message.FileChoices.IMAGE:
                try:
                    # just work with image for now
                    # Get the MIME type (e.g., 'image/png', 'application/pdf')
                    mime_type, _ = mimetypes.guess_type(uploaded_file.name)
                    if not mime_type:
                        # Provide a fallback if MIME type can't be guessed
                        mime_type = "application/octet-stream"

                    # Read binary content and encode to Base64
                    file_content_bytes = uploaded_file.read()
                    base64_encoded_content = base64.b64encode(file_content_bytes).decode('utf-8')

                    data_url = f"data:{mime_type};base64,{base64_encoded_content}"

                    # Add the image/file part to our message content
                    message_content_parts.append({
                        "type": "image_url",
                        "image_url": {"url": data_url}
                    })

                    # IMPORTANT: Reset file pointer so Django can save it
                    uploaded_file.seek(0)
                except Exception as e:
                    print(f"Error encoding file for LLM: {e}")
                    # Optionally, add an error message to the prompt
                    message_content_parts[0]['text'] += "\n\n[System: Error processing uploaded file.]"
            else:
                file_content = ''
                if file_type:
                    messages.warning(request, f'File type is {file_type}, the content is not read')
                    
                    # try to load the file content as a link
                    # Encode the file for the API call
                    
                # # Initialize all_messages list with system and user prompts
                # prompt = {"role": "user", "content": f"{cd['prompt']}\n{file_content if file_content else ''}"}
            # The final prompt object for the LLM
            prompt = {"role": "user", "content": message_content_parts}

            
            # Make a chat body if it is not exists
            if chat:
                pass
            else:
                model_name = cd['model'].name
                chat = Chat.objects.create(
                    user=request.user,
                    chat_id=f"working-{generate_unique_random_number()}",
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
                # file_type=cd['file_type'],
                file_type=file_type,
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



def generate_image(prompt, chat):
    # client = OpenAI(base_url="https://api.avalai.ir/v1/images/generations/", api_key=API_KEY)
    # client = OpenAI(base_url="https://api.avalapis.ir/v1/", api_key=API_KEY) # iran access
    client = OpenAI(base_url="https://api.avalai.ir/v1/", api_key=API_KEY)
    response = None
    image_url = None
    error = ''
    try:
        response = client.images.generate(
        # response = client.chat.completions.create( # for google flash
            model=chat.model_name,
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
    except Exception as e:
        error = str(e)
    
    if response:
        image_url = response.data[0].url
    
    # Replace with actual API call to generate image
    return {"url": image_url, "error": error}

@login_required
@ai_access_required
def AiImageView(request, chat_id=None):
    context = {
        'page_title': 'AI Chat',
        'chats': Chat.objects.filter(user=request.user).order_by('-id'),
    }

    all_messages = None
    ai_message = []
    chat = None
    model_name = "dall-e-3"  # Default model for image generation

    if chat_id:
        chat = get_object_or_404(Chat, chat_id=chat_id, user=request.user)
        all_messages = Message.objects.filter(chat=chat).order_by('created')
        for item in all_messages:
            ai_message.append({"role": item.role, "content": item.content})
    else:
        # Create a new chat instance for new chats
        chat = Chat.objects.create(
            user=request.user,
            chat_id=f"working-{generate_unique_random_number()}",
            model_name=model_name,  # Default model for image generation
            input_token=0,
            output_token=0,
            total_token=0,
        )
    # Check if this is a new chat or an existing one
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        model_name = request.POST.get('model', model_name)
        if chat.model_name != model_name:
            chat.model_name = model_name
            chat.save(update_fields=['model_name']) 
            
        if prompt:
            # Generate an image based on the prompt
            response = generate_image(prompt, chat)  # Your method to generate image            
            image_url = response['url']
            error = response["error"]
            # print(error)
            if image_url:
                # Download the image and save it to the database
                image_response = requests.get(image_url) if image_url else None
            
                if image_response.status_code == 200:
                    # Generate a timestamp for the filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"generated_image_{timestamp}.png"

                    # Save the image to Message as a FileField
                    message = Message.objects.create(
                        chat=chat,
                        role='assistant',
                        content=prompt,
                    )
                    message.file.save(filename, ContentFile(image_response.content)) 
                    message.file_type = Message.FileChoices.IMAGE
                    message.save()

                    messages.success(request, 'Image generated and saved successfully.')
            if error:
                print(error)
                # Save the image to Message as a FileField
                message = Message.objects.create(
                    chat=chat,
                    role='assistant',
                    content=prompt,
                    error=error,
                )
                messages.warning(request, 'Image is not generated.')
            # Redirect or render with success message
            return redirect('ai:ai_image_continue_chat', chat.chat_id)  # Adjust according to your URL structure

    else:
        # If it's a GET request, show the form or existing chat
        form = ChatModelForm()
        # form.fields['model'].queryset = ChatModel.objects.filter(model_type='image')
        context['form'] = form
        context['all_messages'] = all_messages
        context['ai_message'] = ai_message
        context['chat'] = chat

    return render(
        request, 
        'ai/ai_chat.html', 
        context
        )

@login_required
def ChatListView(request):
    query = request.GET.get('q')
    
    chats = Chat.objects.filter(user=request.user).prefetch_related('messages').annotate(
        total_messages=Count('messages'),
        user_messages=Count(Case(
            When(messages__role='user', then=1),
            output_field=IntegerField(),
        )),
        assistant_messages=Count(Case(
            When(messages__role='assistant', then=1),
            output_field=IntegerField(),
        )),
    ).order_by('-id')
    if query:
        chats = chats.filter(messages__content__icontains=query.strip())
    
    context = dict(        
        page_title= 'AI Chats list',
        chats= chats,
        query=query,
    )
    return render(
        request,
        'ai/ai_chats_list.html',
        context
    )