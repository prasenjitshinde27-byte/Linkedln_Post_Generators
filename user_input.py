#Allowed Options. 
VALID_TONES = [
    "Professional", 
    "Inspirational", 
    "Humorous", 
    "Funny", 
    "Angry", 
    "Sad"
]

VALID_LENGHTS = [
    "Short (100–150 words)", 
    "Medium (200–300 words)", 
    "Long (400–500 words)"
]

VALID_FRAMEWORKS = [
    "AIDA (Attention, Interest, Desire, Action)",
    "PAS (Problem, Agitate, Solution)",
    "Storytelling",
    "Listicle",
    "How-to / Tips",
    "None",
]






#Individual function to get user input
def get_topic():
    while True:
        topic = input('Enter your topic: ').strip()
        if topic: #agar topic variable mai agar koi topic aaya hai toh function ko return krdo
            return topic
        else:
            print("Topic cannot be empty. Please enter a valid topic.")


def get_tone():
    for index, value in enumerate(VALID_TONES):
        print(f"{index+1} -> {value}")

    while True:
        choice = int(input('Enter tone number: '))
        if choice:
            if 0 <= choice <= len(VALID_TONES):
                return VALID_TONES[choice-1]
            else:
                print("Invalid choice. Please enter a number corresponding to the tones listed.")
        else:
            print("Invalid input. Please enter a number.")


def get_target_audience():
    while True:
        audience = input('Enter your target audience: ').strip()
        if audience: #agar topic variable mai agar koi topic aaya hai toh function ko return krdo
            return audience
        else:
            print("Target audience cannot be empty. Please enter a valid target audience.")


def get_post_length():
    for index, value in enumerate(VALID_LENGHTS):
        print(f"{index+1} -> {value}")

    while True:
        choice = int(input('Enter post length number: '))
        if choice:
            if 0 <= choice < len(VALID_LENGHTS):
                return VALID_LENGHTS[choice-1]
            else:
                print("Invalid choice. Please enter a number corresponding to the post lengths listed.")
        else:
            print("Invalid input. Please enter a number.")

def get_framework():
    for index, value in enumerate(VALID_FRAMEWORKS):
        print(f"{index+1} -> {value}")

    while True:
        choice = int(input('Enter framework number: '))
        if choice:
            if 0 <= choice < len(VALID_FRAMEWORKS):
                return VALID_FRAMEWORKS[choice-1]
            else:
                print("Invalid choice. Please enter a number corresponding to the frameworks listed.")
        else:
            print("Invalid input. Please enter a number.")



def collect_inputs():
    topic     =   get_topic()
    tone      =   get_tone()
    audience  =   get_target_audience()
    length    =   get_post_length()
    framework =  get_framework()

    inputs = {
        "topic": topic,
        "tone": tone,
        "audience": audience,
        "length": length,
        "framework": framework
    }
    for key , value in inputs.items():
        print(f"{key} : {value}")

    return inputs

if __name__ == "__main__":
    collect_inputs()