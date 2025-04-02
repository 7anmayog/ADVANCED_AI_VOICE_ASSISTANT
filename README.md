# ADVANCED_AI_VOICE_ASSISTANT

1.FIRST OF ALL ITS TOTALLY FREE NO CREDITS ARE REQUIRED FOR API USAGE AND BILLING IT'S HIGHLY RECOMMENDED TO USE PYTHON VERSION 3.10.10 IN VSCODE BEACAUSE ALL THE PACKAGES AND DEPENCIES ARE SUITABLE FOR THE PYTHON VERSION 3.10.10  . AND YOU NEED TO RUN A COMMAND IN YOUR TERMINAL TO INSTALL PACKAGES YOU CAN GET THE PACKAGES IN REQUIREMENTS.TXT FILE . THE COMMAND IS :   pip install -r .\requirements.txt        .

2.YOU CAN EDIT SOME INFORMATION THAT ARE NECESSARY TO DO , YOU MUST EDIT .env FILE FOR BETTER EXPERIENCE AND FOR API INTEGRATION .
   OPEN .env FILE AND CHANGE THE FOLLOWING THINGS ACCORDING TO YOU :
                    CohereAPIKey = ****************************************
                    Username = ********
                    Assistantname = *******
                    GroqAPIKey = ******************************************
                    InputLanguage = en
                    AssistantVoice = en-CA-LiamNeural
                    HuggingFaceAPIKey = ************************************
  
  YOU CAN CHANGE THE INPUT LANGUAGE IF YOU WANT BUT IT'S RECOMMENDED THAT YOU SHOULD SELECT EN OR ENGLISH LANGUAGE FOR BETTER EXP.
  AND YOU CAN ALSO CHANGE ASSISTANT VOICE IF YOU WANT , YOU CAN SELECT THE ASSIATANT VOICE FROM THE FILE NAMED "AI_VOICES" . (I LIKE THIS ENGLISH CANADIAN MALE VOICE)  .
  YOU CAN GET ALL THREE API KEYS FROM THEIR OFFICIAL WEBSITES AND PUT IT IN .env FILE.

3.THIS AI CAN PERFORM TASKS LIKE :
          I. Answer questions: I can provide answers to your questions on topics such as history, science, technology, entertainment, and more.
          II. Generate text: I can generate text based on a prompt or topic, and can even help with writing tasks such as proofreading and editing.
          III. Translate text: I can translate text from one language to another, including popular languages such as Spanish, French, German, Chinese, and many more.
          IV. Summarize content: I can summarize long pieces of text, such as articles or documents, into shorter, more digestible versions.
          V. Offer suggestions: I can offer suggestions for things like gift ideas, travel destinations, books to read, and more.
          VI. Chat and converse: I can have a conversation with you, answering your questions and engaging in discussions on topics that interest you.
          VII. Provide definitions: I can define words and phrases, and explain complex concepts in simple terms.
          VIII. Generate ideas: I can generate ideas for creative projects, such as writing prompts, art ideas, or even business ideas.
          IX. Assist with language learning: I can help with language learning by providing grammar explanations, vocabulary practice, and conversation exercises.
          X. Play games: I can play simple text-based games with you, such as 20 Questions, Hangman, or Word Jumble.
          AND ETC
          
4.IT ONLY SPEAK THE TEXT UNTIL ITS 10 SENTENCES OR 500 CHARACTERS . I MADE THIS FUNCTION TO AVOID THE AI BEING IRRITATING HOWEVER YOU CAN CHANGE IT IN TextToSpeech.py FILE,
    JUST OPEN THE FILE AND JUST REMOVE THE LINE FROM 86 TO 92 AND WRITE THERE      TTS(Text, func)     IN THE SAME INDENTATION WHERE IF STATEMENT WAS WRITTEN AND YOU ARE GOOD TO GO .

5.IT CAN GENERATE IMAGES YOU HAVE TO JUST SAY SOMETHING LIKE GENERATE IMAGES OF WHITE CAT , THEN AFTER FEW SECONDS YOU SEE 4 IMAGES OF WHAT YOU WANTED ON YOU SCREEN AND THE IMAGES WILL BE SAVED ON THE DIRECTORY IN THE FOLDER NAMED "DATA" . I USED THE TEXT TO IMAGE MODEL NAMED STABLE-DIFFUSION FROM HUGGING FACE . BE CAREFUL WHILE GENERATING IMAGES BECAUSE IT MAY EXHAUST YOUR API KEY OF HUGGING FACE!  .


6.IT HAS REALTIME INFORMATION BUT NOT MINUTE TO MINUTE , I TRIED FIXING IT BUT I COULDN'T . BEST OF LUCK TO YOU FOLK.

7.I USED Chatlog.json FILE TO STORE CAHT HISTORY OR TO BE SAY IT'S MEMORY .

    ----THANK YOU----
