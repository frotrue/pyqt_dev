from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def get_gpt_response(prompt):


    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": """
당신은 건축물 관리사입니다. YOLO의 추론결과를 보고 건축물의 위험도 및 추후 조치를 분석해주세요. 입력 형식은 다음과 같습니다.
{
classname: n
classname: n
}
총 4개의 클래스가 있으며 다음과 같습니다. crack, corrosion, ExposedRebars, spalling.
가중치를 부여할때 ExposedRebars > spalling > crack > corrosion 순으로 위험도가 높다고 판단하고 가중치를 부여합니다.
각 클래스는 정확도가 0.5 이상일 경우 해당 결함이 존재한다고 판단합니다.
0.8 이상부터 심각한 결함으로 봅니다.
위의 결과를 총합하여 다음과 같은 형식의 답변을 제공합니다.
{
위험도 : n% 
조치사항 : 
}
예시 답변은 다음과 같습니다.
{
위험도 : 70%
조치사항 : 빠른 시일내로 전문가의 진단을 받아야 합니다.
}
prompt의 내용이 비어 있다면 아무것도 감지되지 않은 상태입니다.
"""},
            {"role": "user", "content": f"{prompt}"}
        ],
        max_completion_tokens=500,
        temperature=0.1,

    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content
#
# get_gpt_response("""spalling: 0.51
# ExposedRebars: 0.35""")