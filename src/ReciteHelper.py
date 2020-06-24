from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tts.v20190823 import tts_client, models
import json
import uuid
import time
import base64


class ReciteHelper:
    def __init__(self):
        self.input_file_path = "../input/input.txt"
        self.input_list = []
        self.auth_file_path = "./auth.json"
        self.auth_obj = None
        self.client = None
        self.output_file_dir = "../output/"

    def load_auth_file(self):
        print("** loading auth file")
        with open(self.auth_file_path, encoding="utf-8") as f:
            self.auth_obj = json.load(f)

    def load_input_file(self):
        print("** loading input file")
        with open(self.input_file_path, encoding="utf-8") as f:
            for i, line in enumerate(f.readlines()):
                line = line.strip()
                if line == "":
                    continue
                if len(line) > 100:
                    print(f"line [{i}] exceeds 100 unicode character limit!")
                    continue
                self.input_list.append(line)

    def run(self):
        self.load_input_file()
        self.auth()
        for i, line in enumerate(self.input_list):
            time.sleep(0.1)
            wav_file_path = f"{self.output_file_dir}{i}_{line[:10]}.mp3"
            self.str_to_wav_file(line, wav_file_path)

    def str_to_wav_file(self, my_str, wav_file_path):
        print(wav_file_path)
        request = models.TextToVoiceRequest()
        params = {
            "Text": my_str,
            "SessionId": uuid.uuid1().hex,
            "ModelType": 1,
            "VoiceType": 1002,
            "Codec": "mp3"
        }
        request.from_json_string(json.dumps(params))
        response = self.client.TextToVoice(request)
        response = json.loads(response.to_json_string())

        with open(wav_file_path, "wb") as f:
            f.write(base64.b64decode(response["Audio"]))

    def auth(self):
        self.load_auth_file()
        cred = credential.Credential(
            self.auth_obj["id"], self.auth_obj["key"])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tts.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tts_client.TtsClient(
            cred, "ap-beijing", clientProfile)
        self.client = client


if __name__ == "__main__":
    rh = ReciteHelper()
    rh.run()
