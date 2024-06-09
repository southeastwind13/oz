from openai import OpenAI
import json

system_prompts = {
    0: "You are a helpful assistant that provides direct " + \
       "and straightforward answers that are as short as possible. " + \
       "You never end with caveats such as 'It is important to remember...'.",
    1:"You are an assistance that return only JSON object. " + \
      "with the requested information.",
    2:"You are a helpful assistant with " + \
      "expert-level emotional intelligence. You reply only" + \
      "with 1, 0, or -1, with 1 meaning positive sentiment," + \
      "-1 meaning negative sentiment, and 0 meaning neutral." 
}

def get_response(completion:any) -> None:
    '''
    Get string response from ChatGPT response.
    '''
    response = completion.choices[0].message.content
    return response

def get_json_response(completion:any) -> None:
    '''
    Get dict response from ChatGPT response.
    '''
    response = str(completion.choices[0].message.content).replace("\n", "")
    json_response = json.loads(response)
    return json_response

class ChatGptBasic:
    def __init__(self, api_key, system_prompt:str, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.system_prompt = system_prompt
        self.model = model

    def complete(self,user_prompt, temperature=0.0, max_tokens=200):
        
        completion = self.client.chat.completions.create(
            model=self.model,
            response_format= {"type": "json_object"},
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return completion


class ChatGptJson:
    '''
    ChatGPT that return only Json
    '''
    def __init__(self, api_key, system_prompt:str, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.system_prompt = system_prompt
        self.model = model

    def complete(self, user_prompt:str):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
            max_tokens=200
        )

        return completion

class ChatGptStructureToUnstructure:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def complete(self, user_prompt:str):

        system_prompt = '''You are assistant that writes concise, detailed, and 
        factual quarterly earning reports given structured data'''

        prompt = f"""Please conver the following JSON document endlossed in 
        triple backticks into a quarterly earnings report suitable for 
        shareholder. \n\n

        ```
        {user_prompt}
        ```
        """


        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=200
        )

        return completion


class AssistantBot:
    '''
    Able to remember history
    '''
    def __init__(self, api_key, system_prompt:str, model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.message = [{"role": "system", "content": system_prompt},]
        self.model = model

    def _complete_by_messages(self, message:list):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=message,
            temperature=0.0,
            max_tokens=200
        )
        return completion

    def complete(self, user_prompt):
        self.message.append(
            {"role": "user", "content": user_prompt}
        )

        completion = self._complete_by_messages(self.message)
        content = completion.choices[0].message.content

        # Remember history
        self.message.append({
            "role": "assistant", "content": content
        })

        return(content)
    

class ChatGptSentiment:
    def __init__(self, api_key, system_prompt:str, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.system_prompt = system_prompt
        self.model = model

    def complete(self,prompt, temperature=0.0, max_tokens=3):

        user_prompt = f"""Please assign a sentiment value \
        for the following text:
        
        ```
        {prompt}
        ```
        """
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompts[2]},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return completion
    

class ChatGptSummarize:
    def __init__(self, api_key,  model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def complete(self,prompt, temperature=0.0, max_tokens=200):

        user_prompt = f"""Can you provide a comprehensive summary of the given text? The summary should cover all the key points and main ideas presented in the original text, while also condensing the information into a concise and easy-to-understand format.Additionally, you must only answer and communicate in the language used by the user.
        
        ```
        {prompt}
        ```
        """
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return completion


class ChatGptWithContext:
    def __init__(self, api_key,  model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def complete(self,prompt,context:str, temperature=0.0, max_tokens=200):

        user_prompt = f"""Please answer the following question:
    
        Question:
        
        ```{prompt}```
        
        Use the following context to find the answer:
        
        ```{context}```
        """
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        return completion