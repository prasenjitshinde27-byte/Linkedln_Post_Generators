#Load all the 3 files
from config         import get_model       #File 1
from user_input  import collect_inputs  #File 2
from prompt_builder import generate_post   #File 3

def save(post, topic):  #AAPKI POST KO .txt FORMAT MAI SAVE KAREGA
    import re
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', topic.strip())
    filename = f"LINKDIN_POST_{safe_name}.txt"
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(post)

    return filename

def run():
    """
    Main Pipeline
    sara execution yaha se control hoga
    """
    
    #Step1: API Setup
    try:
        model = get_model()
    
    except Exception as e:
        print(e)

    #Step2: Collect Inputs
    inputs = collect_inputs()

    #Step3: Generate Post
    try:
        post = generate_post(model, inputs)
    except Exception as e:
        print(e)

    #Step4: Display the post
    print(post)

    #Step5: Save the post in format of .txt file
    filename = save(post,inputs['topic'])
    print('File saved successfully: ',filename )

if __name__ == "__main__":
    run()