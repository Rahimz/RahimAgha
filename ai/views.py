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
from django.db.models import Count, Case, When, IntegerField, Q, Sum
from django.utils.translation import gettext_lazy as _

from accounts.permissions import ai_access_required
from .forms import ChatForm, ChatModelForm, CreateChatModelForm
from .models import Chat, Message, ChatModel, FileTypeDetermine
from django.contrib.auth import get_user_model

User = get_user_model()

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
        page_title = _('ai test')
    )
    all_messages = None
    ai_message = None
    # Initialize the ChatOpenAI model
    model_name = "gpt-4o-mini"
    # model_name = "claude-3-opus"
    # base_url = "https://api.avalapis.ir/v1" # intranet side
    base_url="https://api.avalai.ir/v1" # outside
    
    llm = ChatOpenAI(
        model=model_name, base_url=base_url, api_key=API_KEY
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
    chats = Chat.objects.select_related('user').prefetch_related('messages').filter(user=request.user)
    context = dict(
        page_title = _('AI chat'),
        chats=chats,
    )
    all_messages = None
    ai_message = []
    chat=None
    ai_response = None   
    uploaded_file = ''
    last_message_id = None
     
    if chat_id:
        try:
            chat=chats.get(chat_id=chat_id)
            all_messages = chat.messages.all()
            
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
                    mime_type, x = mimetypes.guess_type(uploaded_file.name)
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
                chat.input_token += ai_response.usage_metadata["input_tokens"]
                chat.output_token += ai_response.usage_metadata["output_tokens"]
                chat.total_token += ai_response.usage_metadata["total_tokens"]
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
def EditPromptView(request, message_id):
    message = get_object_or_404(Message, id= message_id)
    chat = message.chat
    print(':'* 30)
    print(message.id)
    message_ids = list(chat.messages.all().values_list('id', flat=True))
    print(message_ids)
    print(message_ids.index(message.id))
    # 1- deprecate all extended chat messages
    # 2- edit the selected message
    # 3- send to llm 
    return redirect('ai:ai_continue_chat', chat.chat_id)


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
        page_title = _('ai models list'),
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
        page_title = _('add ai model'),
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
        'page_title': _('AI Image Chat'),
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
    m_filter = request.GET.get('m-filter', '')
   
    models_list = ChatModel.objects.all().values_list('name', flat=True)
   
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
    chat_menu = chats
        
    # Apply model filter if applicable
    if m_filter and (m_filter in models_list):
        chats = chats.filter(model_name=m_filter)

    # Apply search filter if applicable
    if query:
        
        chats = chats.filter(
            Q(messages__content__icontains=query.strip()) |
            Q(name__icontains=query.strip()) |
            Q(model_name__icontains=query.strip())
        )
        
    statistics = chats.aggregate(
        input_sum=Sum('input_token'),
        output_sum=Sum('output_token'),
        total_sum=Sum('total_token'),
    )
    context = dict(        
        page_title= _('AI Chats list'),
        chats= chats,
        query=query,
        statistics=statistics,
        m_filter=m_filter,
        chat_menu=chat_menu,
    )
    return render(
        request,
        'ai/ai_chats_list.html',
        context
    )
    
@staff_member_required
def ChatReportView(request):
    users = User.objects.filter(profile__ai_access=True).annotate(
        input_token=Sum('chats__input_token'),
        output_token=Sum('chats__output_token'),
        total_token=Sum('chats__total_token')
    )
    statistics = Chat.objects.all().aggregate(
        input_sum=Sum('input_token'),
        output_sum=Sum('output_token'),
        total_sum=Sum('total_token'),
    )
    context = dict(        
        page_title= _('AI Chat Reports'),
        users=users,
        statistics=statistics,
        
    )
    return render(
        request,
        'ai/ai_chats_reports.html',
        context
    )
    
    


def generate_and_update_chat_name_with_llm(chat_id: str):
    """
    Generates a descriptive name for a chat using an LLM and updates the Chat object.

    This function fetches the entire message history for a given chat,
    sends it to the LLM with a prompt to create a title, and saves the
    resulting title to the chat's 'name' field. This operation is not
    recorded in the message history.

    Args:
        chat_id (str): The chat_id of the Chat instance to be updated.

    Returns:
        str: The generated chat name if successful, otherwise None.
    """
    try:
        chat = Chat.objects.get(chat_id=chat_id)

        # Only generate a name if one doesn't already exist to save API calls.
        # You can remove this check if you want to regenerate the name every time.
        if chat.name:
            return chat.name

        # update name based on first 4 messages
        messages = chat.messages.all().order_by('created')[:4]

        # If there are no messages, we can't generate a name.
        if not messages:
            return None

        # 1. Format the existing conversation history
        chat_history = []
        for message in messages:
            chat_history.append({"role": message.role, "content": message.content})

        # 2. Add the special prompt to generate the title
        # This prompt is engineered to get a clean, direct response.
        title_generation_prompt = (
            "Based on the conversation history above, generate a short, descriptive title for this chat. "
            "The title must be 100 characters or less. "
            "IMPORTANT: Respond with ONLY the title itself, without any extra text, "
            "explanations, or quotation marks. For example, if the topic is 'Planning a trip to Paris', "
            "your entire response should be 'Planning a trip to Paris'."
        )
        chat_history.append({"role": "user", "content": title_generation_prompt})

        # 3. Initialize and call the LLM
        # Use the same model associated with the chat for consistency
        llm = ChatOpenAI(
            model=chat.model_name,
            base_url="https://api.avalai.ir/v1",
            api_key=API_KEY,
            temperature=0.2 # Use a lower temperature for more predictable, factual titles
        )

        response = llm.invoke(chat_history)

        if response and response.content:
            # 4. Clean the response and save it
            # The prompt asks for no quotes, but we clean them just in case.
            raw_title = response.content
            cleaned_title = raw_title.strip().strip('"\'')

            # Enforce the max_length constraint
            final_title = cleaned_title[:100]

            chat.name = final_title
            fields_to_update = ['name']
            # --- CHANGE 2: Track and update token usage ---
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                input_tokens = response.usage_metadata.get("input_tokens", 0)
                output_tokens = response.usage_metadata.get("output_tokens", 0)
                total_tokens = response.usage_metadata.get("total_tokens", 0)

                chat.input_token += input_tokens
                chat.output_token += output_tokens
                chat.total_token += total_tokens

                fields_to_update.extend(['input_token', 'output_token', 'total_token'])
                print(f"Adding {total_tokens} tokens to chat {chat_id} for name generation.")
            
            chat.save(update_fields=fields_to_update)

            print(f"Generated and saved name for chat {chat_id}: '{final_title}'")
            return final_title

    except Chat.DoesNotExist:
        print(f"Error: Chat with chat_id '{chat_id}' not found.")
        return None
    except Exception as e:
        # Handle potential API errors or other issues
        print(f"An error occurred while generating chat name for {chat_id}: {e}")
        return None

    return None


@ai_access_required
@login_required
def update_chat_name(request, chat_id):
    generate_and_update_chat_name_with_llm(chat_id)
    return redirect(request.META['HTTP_REFERER'])