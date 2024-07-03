import requests
import json


vllm_host = "http://localhost:8000"
url = f"{vllm_host}/generate"



def chat(messages):
    # headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": messages,
        "stream": True,
        "src_lang": "Auto",
        "tgt_lang": "Korean"
    }

    r = requests.post(url, json=data, stream=True)
    
    return r



# messages= """
# 尊敬的王经理，

# 您好！

# 我是XYZ公司的李华。我写这封邮件是想与您确认一下我们下周的会议安排。

# 首先，非常感谢您上周在我们公司会议室举办的研讨会。您分享的宝贵经验和建议对我们团队非常有帮助。

# 为了进一步推进项目进展，我们计划在下周三上午10点再次举行一次会议。会议地点仍然定在我们公司会议室。如果这个时间对您不方便，请告知我们您的空闲时间，我们将重新安排。

# 此外，请您提前准备好本次会议需要讨论的资料，尤其是关于市场分析和项目预算的部分。这将有助于我们更高效地进行讨论和决策。

# 如果您有任何问题或需要进一步的信息，请随时与我联系。

# 期待您的回复。

# 此致

# 敬礼！

# 李华
# XYZ公司
# 电子邮件: li.hua@xyz.com
# 电话: +86 123 4567 8900
# """


messages = """
FORT MEADE, Md. - After months of preparation and three days of elaborate and challenging cyber operations, the U.S. Military Academy has emerged as the champion of the sixth annual NSA Cyber Exercise (NCX).
 
The battle for the coveted NCX trophy included participants from the U.S. service academies and senior military colleges, who competed alongside individuals from multiple NSA professional development programs. A team from USCYBERCOM’s Cyber National Mission Force (CNMF) participated in a For Exhibition Only (FEO) status. All team members rose to the challenge, applying their technical, collaborative, and critical thinking skills to simulated scenarios they can expect to encounter throughout their cyber careers.
 
“Agility and adaptability have been and will continue to be keys to our success,” Maj Gen Mateo Martemucci, deputy chief of the Central Security Service said during his welcome message “Remain alert, focused, and trust your training. This is what we prepare for.”
 
The U.S. Air Force Academy placed second, while the University of North Georgia finished third, beating out the U.S. Coast Guard Academy, the U.S. Naval Academy, and the senior military colleges, including Norwich University, Texas A&M University, The Citadel, Virginia Military Institute, and Virginia Tech. NSA’s Cybersecurity Operations Development Program (CSODP took first amongst the development programs.
 
This year’s NCX was the first hybrid competition since the COVID-19 pandemic, allowing institutions to participate in person or virtually.
 
Teams engaged in offensive cyber activities against a fictional adversary that attacked a satellite downlink. Exercises focused on active attack and malware, software development, and cybersecurity policy. These, along with the final attack-and-defend cyber combat exercise, challenged participants to use their creativity and collaboration skills to prevail against complex cyber threats.
 
“The competition is more than a trophy,” said Kenneth Allison, associate director of the Hollingsworth Center for Ethical Leadership at Texas A&M University, whose team competed in this year’s contest. “The additional knowledge and exposure to real-world challenges, the opportunities to ask questions, build confidence, and meet people that you may work with in the future – that's what makes the NCX such a valuable part of our academic program.”

Martemucci awarded West Point’s cyber competition team members with the NCX trophy after edging out their competition in the tournament.
 
“Congratulations to the U.S. Military Academy,” Martemucci said during the closing ceremony. “We hope that this simulation not only deepened your understanding of the current threat environment, but also inspired you to continue to hone your skills and talents to help protect our Nation, whether in uniform, academia, government, or industry.”

This three-day, unclassified cyber competition is the culmination of the Agency’s effort to advance strategic goals by developing and testing the skills, teamwork, planning, and decision-making of future cybersecurity professionals.

 “The most exciting part for me is witnessing our future leaders put their skills to use,” said NCX Program Manager Kelley Welch. “Throughout the year, and especially during the competition, planting the seeds giving students firsthand insight into the vast cyber career opportunities within NSA’s mission, and how they can apply their passions and skills to help secure our Nation’s future.”
 
The final cyber combat exercise required participants to work collaboratively as they applied their cybersecurity knowledge to exploit and extract data from a physical device. Strong coordination, planning, communication, teamwork, and decision-making skills were essential to each team’s success.
 
 “I was a little intimidated at first because I assumed that we would only interact with our team members during the event,” said Joselyn Cordova-Flores, a junior at Norwich University and first-time NCX participant. “Instead, I had a chance to engage with people from NSA and different teams while working on other activities. The collaborative environment not only showed me that I have what it takes to be successful in this field, but also solidified NSA as my No. 1 career choice after graduation.”
 
Fostering connections across the cyber defense community in a conducive learning environment is what LT Ryan Quarry, instructor for the U.S. Coast Guard Academy, finds most rewarding about the NCX.
 
“This is a unique opportunity for students to network with their peers in other service academies, and other like-minded individuals who can help them reach their career goals,” he said. “In addition, the real-world scenarios give them immediate insight into their strengths and areas for development. These are two of many factors which make the NCX a premiere event for the U.S. Coast Guard Academy and a critical component of its cyber education programs.” 
"""


response = chat(messages)
print(response)

len_text = 0
len_text_prev = 0
for line in response.iter_content(chunk_size=4096):
    # print(line.decode('utf-8'))
    if len_text < len_text_prev:
        len_text = 0 
        print("\n")
    text = line.decode('utf-8')
    print(text[len_text:], end="", flush=True)
    len_text_prev = len_text
    len_text = len(text)

print("\n")

