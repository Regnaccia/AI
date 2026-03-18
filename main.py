from models.Project import BaseProject
from core.router import route
if __name__ == "__main__":
    pj = BaseProject()
    pj.save_to_disk()
    route(pj)
    


