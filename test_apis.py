import requests
import json
import threading
import time

api_key = "044d96d0a9150903ca5e80fc1a5da8e7"
latitude = "53.806683"
longitude = "-1.555033"

url = f"http://localhost:7071/api/get_data"

url2 = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"


response = requests.post(url, json={"city": "*"})
print(response.content)


# def ping_website():
#     for i in range(50):
#         reponse = requests.get("http://172.16.0.100:30002/validate")

# threads = []
# start_time = time.time()
# for i in range(4):
#     thread = threading.Thread(target=ping_website)
#     thread.start()
#     threads.append(thread)
# # Wait for all threads to finish
# for thread in threads:
#     thread.join()

# end_time = time.time()
# print(f"Time taken: {end_time - start_time} seconds")