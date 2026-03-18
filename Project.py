from pathlib import Path
import json

class Project:
    def __init__(self):
        self.pj_id = self.get_project_id()
        self.status = "WAITING_USER_PROMPT"

    def get_project_id(self):
        file_path = Path(r"AI\pj1.txt")

        if file_path.exists():
            file = open(file_path,"rt")
            content = [i.strip() for i in file.readlines()]
            last = int(content[-1])
            file = open(file_path,"a")
            current_id = str(last + 1)
            content = "\n" + current_id
            file.write(content)
        else:
            print("creating file")
            file = open(file_path,"w")
            current_id = "0"
            file.write(current_id)

        return current_id

    def add_user_prompt(self,prompt):
        self.user_prompt = prompt

    def dump_json_to_file(self):
        d = json.dumps(vars(self))
        path = rf"AI\{self.pj_id}.json"
        with open(path,"w") as f:
            f.write(d)

    def dump_json(self):
        d = json.dumps(vars(self))
        print(d)


