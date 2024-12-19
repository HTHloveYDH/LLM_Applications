from poe_api_wrapper import AsyncPoeApi

tokens = {
'p-b': "k2gzscfNUU8ymk1ErjEgZg%3D%3D",
'p-lat': "h6cCyOF92GMejQnkZHuTpq%2B5JoARdYhCSSCAgjREyw%3D%3D",
}


import json
import time
from poe_api_wrapper import PoeApi

def read_json_file(file_path):
    """读取JSON文件"""
    try:
        with open(file_path, 'r') as f:
            return f.read()  # 直接返回原始文本内容
    except Exception as e:
        raise Exception(f"Failed to read JSON file {file_path}: {e}")

def main():
    max_retries = 3
    retry_delay = 60  # 60秒等待时间
    
    for attempt in range(max_retries):
        try:
            client = PoeApi(tokens)
            
            prompt = """你是一名专业的视觉标注工程师,并具有很强的空间理解能力,请你根据我发给你的标注前的图片,
                    标注产生的json文件,标注后的结果图对标注工作进行检查,要求关键点标注信息是否符合标准要求,
                    位置是否大概正确,标注数量是否满足要求,矩形框内的人体关键点是否该标注的地方有标注。
                    具体需要标注的keypoints如下:\n"""
                    
            KEYPOINTS = ['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear',
                    'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist',
                     'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee']

            # 文件路径
            files = [
                '/home/amos/poe-api-wrapper/check/pre_label.png',
                '/home/amos/poe-api-wrapper/check/post_label.png'
            ]
            label_json_file = "/home/amos/poe-api-wrapper/check/label.json"      # 标注文件的内容
            response_templet_json_file = "/home/amos/poe-api-wrapper/response_templet.json"  #回复模板
            try:
                # 读取JSON文件的原始内容
                label_json_content = read_json_file(label_json_file)       
                response_templet_content = read_json_file(response_templet_json_file)
                # 构建消息
                message = prompt
                message += str(KEYPOINTS) + "\n\n"
                message += "请检查我上传的两张图片和一个json文件，第一张是标注前的图片，第二张是标注后的图片。\n"
                message += "以下是标注文件内容：\n"
                message += label_json_content  # 直接添加JSON文件的原始内容
                message += "\n"
                message += "以下是回复模板,检查结果要严格按照本模板格式，不要有多余的回答内容\n"
                message += response_templet_content
                
                # 发送消息和文件
                for chunk in client.send_message(bot="Claude-3.5-Sonnet", message=message,file_path=files):
                    print(chunk["response"], end='', flush=True)
                break
                
            except Exception as e:
                print(f"Error during process: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise Exception("Maximum retries reached")
                    
        except RuntimeError as e:
            if "Rate limit exceeded" in str(e):
                if attempt < max_retries - 1:
                    print(f"Rate limit exceeded, waiting {retry_delay} seconds before retry...")
                    time.sleep(retry_delay)
                    continue
                else:
                    print("Maximum retries reached")
                    raise
            else:
                raise

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Program terminated with error: {e}")