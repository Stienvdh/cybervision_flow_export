import cybervision, database, json
from dotenv import load_dotenv

#Read data from json file
def getJson(filepath):
	with open(filepath, 'r') as f:
		json_content = json.loads(f.read())
		f.close()

	return json_content

def main_loop():
    cybervision.get_flows_since_yesterday()


if __name__ == "__main__":
    load_dotenv()
    main_loop()