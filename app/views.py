from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
import json,requests,os
from watson_developer_cloud import VisualRecognitionV3
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def land(request):
	return render(request, 'land.html')

def index(request):
	if request.method == 'POST':
		form = ImageForm(request.POST, request.FILES)
		if form.is_valid():
			obj=form.save()
			return redirect('result',obj.id)
	else:
		form = ImageForm()
	return render(request, 'index.html', {'form' : form})


def result(request,id):
	authenticator = IAMAuthenticator('0gtx_JpZ7asvTN5qh8fQBsaWefHqOE15Z0DZvN8BrZKV')
	text_to_speech = TextToSpeechV1(authenticator=authenticator)

	visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='tUr8iCtLPxhe-ZxzCc1lMttk0MiVfpBudbwQOzQtBMOR')
	obj=Image.objects.get(id=id)
	print(obj.image)

	with open('media/'+str(obj.image), 'rb') as images_file:
		classes = visual_recognition.classify(
		images_file,
		threshold='0',
		classifier_ids='default').get_result()

	nutrition = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search?api_key=CcOcS7GaR1IkCaPsbFRgy95DBKw77LIGzZTyoIDd&query='+classes['images'][0]['classifiers'][0]['classes'][0]['class']).json()

	text_to_speech.set_service_url('https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/13febd73-d584-44ee-9407-f08f768e7773')

	os.remove("static/audio/now.wav")

	with open('static/audio/now.wav', 'wb') as audio_file:
		audio_file.write(text_to_speech.synthesize("That's a good looking "+classes['images'][0]['classifiers'][0]['classes'][0]['class'],voice='en-US_AllisonV3Voice',accept='audio/wav').get_result().content)

	return render(request, 'result.html',{'image':obj,'nutrition':nutrition["foods"],'result':classes['images'][0]['classifiers'][0]['classes']})
